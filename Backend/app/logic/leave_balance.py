from exceptions import ConflictError, NotFoundError
from model.leave_balance import LeaveBalance
from repo.employeerepo import EmployeeRepository
from repo.leavebalancerepo import LeaveBalanceRepository


class LeaveBalanceService:

    def __init__(
        self,
        repository: LeaveBalanceRepository,
        employee_repository: EmployeeRepository,
    ):
        self.repository = repository
        self.employee_repository = employee_repository

    # CREATE
    def create_leave_balance(self, employee_id: int, total_leaves: int = 20):
        if not self.employee_repository.find_by_id(employee_id):
            raise NotFoundError("Employee not found")

        if self.repository.find_by_employee(employee_id):
            raise ConflictError("Leave balance already exists for employee")

        balance = LeaveBalance(
            employee_id=employee_id,
            total_leaves=total_leaves,
            used_leaves=0,
            remaining_leaves=total_leaves
        )

        return self.repository.save(balance)

    # GET
    def get_leave_balance(self, employee_id: int):
        balance = self.repository.find_by_employee(employee_id)

        if not balance:
            raise NotFoundError("Leave balance not found")

        return balance

    # ADJUST (adds `adjustment` days to the yearly total)
    def adjust_leave_balance(self, employee_id: int, adjustment: int):
        balance = self.get_leave_balance(employee_id)

        new_total = balance.total_leaves + adjustment

        if new_total < balance.used_leaves:
            raise ValueError("Total leaves cannot go below leaves already used")

        balance.total_leaves = new_total
        balance.remaining_leaves = new_total - balance.used_leaves

        return self.repository.save(balance)
