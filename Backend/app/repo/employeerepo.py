from sqlalchemy.orm import Session
from model.Employees import Employee


class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, employee_id: int):
        return self.db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

    def find_by_email(self, email: str):
        return self.db.query(Employee).filter(
            Employee.email == email
        ).first()

    def find_all(self):
        return self.db.query(Employee).order_by(Employee.id).all()

    def save(self, employee: Employee):
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee: Employee):
        self.db.delete(employee)
        self.db.commit()

    def rollback(self):
        self.db.rollback()
