from sqlalchemy.exc import IntegrityError

from exceptions import ConflictError, NotFoundError
from model.Employees import Employee
from repo.employeerepo import EmployeeRepository
from schemas import EmployeeCreate, EmployeeUpdate


class EmployeeService:

    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    # CREATE
    def create_employee(self, data: EmployeeCreate):
        if self.repository.find_by_email(data.email):
            raise ConflictError("Email already registered")

        employee = Employee(**data.model_dump())
        return self.repository.save(employee)

    # GET ALL
    def get_all_employees(self):
        return self.repository.find_all()

    # GET ONE
    def get_employee(self, employee_id: int):
        employee = self.repository.find_by_id(employee_id)

        if not employee:
            raise NotFoundError("Employee not found")

        return employee

    # UPDATE
    def update_employee(self, employee_id: int, data: EmployeeUpdate):
        employee = self.get_employee(employee_id)

        changes = data.model_dump(exclude_none=True)

        new_email = changes.get("email")
        if new_email and new_email != employee.email:
            if self.repository.find_by_email(new_email):
                raise ConflictError("Email already registered")

        for field, value in changes.items():
            setattr(employee, field, value)

        return self.repository.save(employee)

    # DELETE
    def delete_employee(self, employee_id: int):
        employee = self.get_employee(employee_id)

        try:
            self.repository.delete(employee)
        except IntegrityError:
            self.repository.rollback()
            raise ConflictError(
                "Employee has attendance, leave, overtime or salary records"
            )

        return {"message": "Employee deleted", "employee_id": employee_id}
