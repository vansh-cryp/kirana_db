from datetime import date
from typing import Optional

from sqlalchemy.orm import Session
from model.overtime import Overtime


class OvertimeRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_all(self):
        return self.db.query(Overtime).order_by(Overtime.date.desc()).all()

    # start_date / end_date are optional filters (inclusive)
    def find_by_employee(
        self,
        employee_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        query = self.db.query(Overtime).filter(
            Overtime.employee_id == employee_id
        )
        if start_date:
            query = query.filter(Overtime.date >= start_date)
        if end_date:
            query = query.filter(Overtime.date <= end_date)
        return query.order_by(Overtime.date.desc()).all()

    def save(self, overtime: Overtime):
        self.db.add(overtime)
        self.db.commit()
        self.db.refresh(overtime)
        return overtime
