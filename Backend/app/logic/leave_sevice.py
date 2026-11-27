from exceptions import ConflictError, NotFoundError
from model.leave import Leave
from repo.employeerepo import EmployeeRepository
from repo.leavebalancerepo import LeaveBalanceRepository
from repo.leaverepo import LeaveRepository
from schemas import LeaveApply

PENDING = "PENDING"
APPROVED = "APPROVED"
REJECTED = "REJECTED"


class LeaveService:

    def __init__(
        self,
        repository: LeaveRepository,
        balance_repository: LeaveBalanceRepository,
        employee_repository: EmployeeRepository,
    ):
        self.repository = repository
        self.balance_repository = balance_repository
        self.employee_repository = employee_repository

    # Calendar days, start and end both included
    @staticmethod
    def _days(start_date, end_date) -> int:
        return (end_date - start_date).days + 1

    def _require_employee(self, employee_id: int):
        if not self.employee_repository.find_by_id(employee_id):
            raise NotFoundError("Employee not found")

    def _require_balance(self, employee_id: int):
        balance = self.balance_repository.find_by_employee(employee_id)

        if not balance:
            raise ValueError("Leave balance not set up for this employee")

        return balance

    # APPLY
    def apply_leave(self, employee_id: int, data: LeaveApply):
        self._require_employee(employee_id)

        if data.end_date < data.start_date:
            raise ValueError("End date cannot be before start date")

        if self.repository.find_overlapping(
            employee_id, data.start_date, data.end_date
        ):
            raise ConflictError("Leave overlaps with an existing request")

        balance = self._require_balance(employee_id)
        days = self._days(data.start_date, data.end_date)

        if days > balance.remaining_leaves:
            raise ValueError(
                f"Insufficient leave balance: {balance.remaining_leaves} "
                f"left, {days} requested"
            )

        leave = Leave(
            employee_id=employee_id,
            start_date=data.start_date,
            end_date=data.end_date,
            leave_type=data.leave_type,
            reason=data.reason,
            status=PENDING
        )

        return self.repository.save(leave)

    # GET ALL
    def get_all_leaves(self):
        return self.repository.find_all()

    # GET BY EMPLOYEE
    def get_employee_leaves(self, employee_id: int):
        self._require_employee(employee_id)
        return self.repository.find_by_employee(employee_id)

    # GET ONE
    def get_leave(self, leave_id: int):
        leave = self.repository.find_by_id(leave_id)

        if not leave:
            raise NotFoundError("Leave not found")

        return leave

    # APPROVE (deducts from balance)
    def approve_leave(self, leave_id: int):
        leave = self.get_leave(leave_id)

        if leave.status != PENDING:
            raise ValueError(
                f"Only pending leaves can be approved (status: {leave.status})"
            )

        balance = self._require_balance(leave.employee_id)
        days = self._days(leave.start_date, leave.end_date)

        if days > balance.remaining_leaves:
            raise ValueError(
                f"Insufficient leave balance: {balance.remaining_leaves} "
                f"left, {days} requested"
            )

        balance.used_leaves += days
        balance.remaining_leaves = balance.total_leaves - balance.used_leaves
        self.balance_repository.save(balance, commit=False)

        leave.status = APPROVED

        # One commit saves both the balance and the leave
        return self.repository.save(leave)

    # REJECT
    def reject_leave(self, leave_id: int):
        leave = self.get_leave(leave_id)

        if leave.status != PENDING:
            raise ValueError(
                f"Only pending leaves can be rejected (status: {leave.status})"
            )

        leave.status = REJECTED
        return self.repository.save(leave)

    # DELETE (gives days back if the leave was approved)
    def delete_leave(self, leave_id: int):
        leave = self.get_leave(leave_id)

        if leave.status == APPROVED:
            balance = self.balance_repository.find_by_employee(
                leave.employee_id
            )
            if balance:
                days = self._days(leave.start_date, leave.end_date)
                balance.used_leaves = max(balance.used_leaves - days, 0)
                balance.remaining_leaves = (
                    balance.total_leaves - balance.used_leaves
                )
                self.balance_repository.save(balance, commit=False)

        # One commit saves the balance change and the delete
        self.repository.delete(leave)

        return {"message": "Leave deleted", "leave_id": leave_id}
