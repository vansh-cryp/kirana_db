from exceptions import NotFoundError
from model.overtime import Overtime
from repo.employeerepo import EmployeeRepository
from repo.overtimerepo import OvertimeRepository
from schemas import OvertimeCreate
from utils import parse_month

# Used when a record is created without an explicit rate
OVERTIME_MULTIPLIER = 1.5


class OvertimeService:

    def __init__(
        self,
        repository: OvertimeRepository,
        employee_repository: EmployeeRepository,
    ):
        self.repository = repository
        self.employee_repository = employee_repository

    def _require_employee(self, employee_id: int):
        employee = self.employee_repository.find_by_id(employee_id)

        if not employee:
            raise NotFoundError("Employee not found")

        return employee

    # Records for an employee, optionally limited to one month (YYYY-MM)
    def _records(self, employee_id: int, month: str = None):
        self._require_employee(employee_id)

        if month:
            month, start, end = parse_month(month)
            return month, self.repository.find_by_employee(
                employee_id, start, end
            )

        return None, self.repository.find_by_employee(employee_id)

    # CREATE
    def create_overtime(self, data: OvertimeCreate):
        employee = self._require_employee(data.employee_id)

        rate = data.overtime_rate
        if rate is None:
            rate = round(employee.hourly_salary * OVERTIME_MULTIPLIER, 2)

        overtime = Overtime(
            employee_id=data.employee_id,
            date=data.date,
            extra_hours=data.extra_hours,
            overtime_rate=rate
        )

        return self.repository.save(overtime)

    # GET ALL
    def get_all_overtime(self):
        return self.repository.find_all()

    # GET BY EMPLOYEE
    def get_employee_overtime(self, employee_id: int):
        self._require_employee(employee_id)
        return self.repository.find_by_employee(employee_id)

    # TOTAL HOURS
    def get_overtime_hours(self, employee_id: int, month: str = None):
        month, records = self._records(employee_id, month)

        return {
            "employee_id": employee_id,
            "month": month,
            "total_extra_hours": round(
                sum(r.extra_hours for r in records), 2
            )
        }

    # TOTAL PAY
    def get_overtime_pay(self, employee_id: int, month: str = None):
        month, records = self._records(employee_id, month)

        return {
            "employee_id": employee_id,
            "month": month,
            "total_extra_hours": round(
                sum(r.extra_hours for r in records), 2
            ),
            "total_overtime_pay": round(
                sum(r.extra_hours * r.overtime_rate for r in records), 2
            )
        }
