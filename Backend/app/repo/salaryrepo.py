from sqlalchemy.orm import Session
from model.salary import Salary


class SalaryRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(Salary).order_by(Salary.id.desc()).all()

    def find_by_id(self, salary_id: int):
        return self.db.query(Salary).filter(Salary.id == salary_id).first()

    def find_by_employee(self, employee_id: int):
        return self.db.query(Salary).filter(
            Salary.employee_id == employee_id
        ).order_by(Salary.month.desc()).all()

    def find_by_employee_and_month(self, employee_id: int, month: str):
        return self.db.query(Salary).filter(
            Salary.employee_id == employee_id,
            Salary.month == month
        ).first()

    def save(self, salary: Salary):
        self.db.add(salary)
        self.db.commit()
        self.db.refresh(salary)
        return salary
