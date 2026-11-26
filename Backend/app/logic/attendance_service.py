from datetime import datetime, date
from model.attendance import Attendance
from repo.attendancerepo import AttendanceRepository


class AttendanceService:

    def __init__(self, repository: AttendanceRepository):
        self.repository = repository

    # CHECK IN
    def check_in(self, employee_id: int):

        # Check employee exists
        employee = self.repository.get_employee(employee_id)

        if not employee:
            raise ValueError("Employee not found")

        today = date.today()

        # Check whether already checked in
        attendance = self.repository.find_by_employee_and_date(
            employee_id, today
        )

        if attendance:
            raise ValueError("Employee already checked in today")

        # Create attendance record
        attendance = Attendance(
            employee_id=employee_id,
            date=today,
            check_in=datetime.now().time()
        )

        return self.repository.save(attendance)

    # CHECK OUT
    def check_out(self, employee_id: int):

        today = date.today()

        # Find today's attendance
        attendance = self.repository.find_by_employee_and_date(
            employee_id, today
        )

        if not attendance:
            raise ValueError("Employee has not checked in today")

        if attendance.check_out:
            raise ValueError("Employee already checked out")

        current_time = datetime.now().time()

        # Calculate working hours
        check_in = datetime.combine(today, attendance.check_in)
        check_out = datetime.combine(today, current_time)

        working_hours = (
            check_out - check_in
        ).total_seconds() / 3600

        if working_hours < 0:
            raise ValueError("Invalid check-out time")

        attendance.check_out = current_time
        attendance.working_hours = round(working_hours, 2)

        return self.repository.save(attendance)

    # GET ALL ATTENDANCE
    def get_all_attendance(self):
        return self.repository.find_all()

    # GET EMPLOYEE ATTENDANCE
    def get_employee_attendance(self, employee_id: int):

        employee = self.repository.get_employee(employee_id)

        if not employee:
            raise ValueError("Employee not found")

        return self.repository.find_by_employee(employee_id)

    # GET ATTENDANCE BY DATE
    def get_attendance_by_date(self, attendance_date: date):

        return self.repository.find_by_date(attendance_date)