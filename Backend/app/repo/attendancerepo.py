from sqlalchemy.orm import Session
from model.attendance import Attendance
from model.employee import Employee
from datetime import date


class AttendanceRepository:

    def __init__(self, db: Session):
        self.db = db

    # Check whether employee exists
    def get_employee(self, employee_id: int):
        return self.db.query(Employee).filter(
            Employee.id == employee_id
        ).first()

    # Find attendance by employee and date
    def find_by_employee_and_date(
        self, employee_id: int, attendance_date: date
    ):
        return self.db.query(Attendance).filter(
            Attendance.employee_id == employee_id,
            Attendance.date == attendance_date
        ).first()

    # Save attendance
    def save(self, attendance: Attendance):
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    # Get all attendance
    def find_all(self):
        return self.db.query(Attendance).all()

    # Get attendance by employee
    def find_by_employee(self, employee_id: int):
        return self.db.query(Attendance).filter(
            Attendance.employee_id == employee_id
        ).order_by(Attendance.date.desc()).all()

    # Get attendance by date
    def find_by_date(self, attendance_date: date):
        return self.db.query(Attendance).filter(
            Attendance.date == attendance_date
        ).all()