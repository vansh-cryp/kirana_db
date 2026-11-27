from datetime import date

from sqlalchemy.orm import Session
from model.leave import Leave


class LeaveRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, leave_id: int):
        return self.db.query(Leave).filter(Leave.id == leave_id).first()

    def find_all(self):
        return self.db.query(Leave).order_by(Leave.id.desc()).all()

    def find_by_employee(self, employee_id: int):
        return self.db.query(Leave).filter(
            Leave.employee_id == employee_id
        ).order_by(Leave.start_date.desc()).all()

    # Pending or approved leave that overlaps the given dates
    def find_overlapping(
        self, employee_id: int, start_date: date, end_date: date
    ):
        return self.db.query(Leave).filter(
            Leave.employee_id == employee_id,
            Leave.status.in_(["PENDING", "APPROVED"]),
            Leave.start_date <= end_date,
            Leave.end_date >= start_date
        ).first()

    # Also commits anything else pending on this session
    def save(self, leave: Leave):
        self.db.add(leave)
        self.db.commit()
        self.db.refresh(leave)
        return leave

    def delete(self, leave: Leave):
        self.db.delete(leave)
        self.db.commit()
