from exceptions import ConflictError, NotFoundError
from model.salary import Salary
from repo.attendancerepo import AttendanceRepository
from repo.employeerepo import EmployeeRepository
from repo.overtimerepo import OvertimeRepository
from repo.salaryrepo import SalaryRepository
from schemas import SalaryGenerate
from utils import parse_month

# Hours per day paid at the normal hourly rate.
# Anything above this is paid only through overtime records.
STANDARD_DAILY_HOURS = 8


class SalaryService:

    def __init__(
        self,
        repository: SalaryRepository,
        employee_repository: EmployeeRepository,
        attendance_repository: AttendanceRepository,
        overtime_repository: OvertimeRepository,
    ):
        self.repository = repository
        self.employee_repository = employee_repository
        self.attendance_repository = attendance_repository
        self.overtime_repository = overtime_repository

    def _require_employee(self, employee_id: int):
        employee = self.employee_repository.find_by_id(employee_id)

        if not employee:
            raise NotFoundError("Employee not found")

        return employee

    # GENERATE
    def generate_salary(self, employee_id: int, data: SalaryGenerate):
        employee = self._require_employee(employee_id)

        month, start, end = parse_month(data.month)

        if end < employee.joining_date:
            raise ValueError("Month is before the employee's joining date")

        if self.repository.find_by_employee_and_month(employee_id, month):
            raise ConflictError("Salary already generated for this month")

        # Normal pay: attendance hours (capped per day) x hourly salary
        attendance = self.attendance_repository.find_by_employee_and_range(
            employee_id, start, end
        )
        regular_hours = sum(
            min(a.working_hours or 0, STANDARD_DAILY_HOURS)
            for a in attendance
        )
        fixed_salary = round(regular_hours * employee.hourly_salary, 2)

        # Overtime pay: extra hours x rate for each record in the month
        overtime = self.overtime_repository.find_by_employee(
            employee_id, start, end
        )
        overtime_pay = round(
            sum(o.extra_hours * o.overtime_rate for o in overtime), 2
        )

        net_salary = round(
            fixed_salary + overtime_pay + data.bonus - data.deductions, 2
        )

        if net_salary < 0:
            raise ValueError("Deductions exceed total earnings")

        salary = Salary(
            employee_id=employee_id,
            month=month,
            fixed_salary=fixed_salary,
            overtime_pay=overtime_pay,
            bonus=data.bonus,
            deductions=data.deductions,
            net_salary=net_salary
        )

        return self.repository.save(salary)

    # GET ALL
    def get_all_salary(self):
        return self.repository.find_all()

    # GET BY EMPLOYEE
    def get_employee_salary(self, employee_id: int):
        self._require_employee(employee_id)
        return self.repository.find_by_employee(employee_id)

    # GET BY EMPLOYEE + MONTH
    def get_salary_by_month(self, employee_id: int, month: str):
        self._require_employee(employee_id)

        month, _, _ = parse_month(month)
        salary = self.repository.find_by_employee_and_month(employee_id, month)

        if not salary:
            raise NotFoundError("Salary not found for this month")

        return salary

    # GET ONE
    def get_salary(self, salary_id: int):
        salary = self.repository.find_by_id(salary_id)

        if not salary:
            raise NotFoundError("Salary not found")

        return salary
