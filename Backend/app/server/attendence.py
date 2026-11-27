from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database.database import get_db
from repo.attendancerepo import AttendanceRepository
from service.attendanceservice import AttendanceService

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


def get_attendance_service(db: Session = Depends(get_db)):
    repository = AttendanceRepository(db)
    return AttendanceService(repository)


@router.post("/check-in/{employee_id}")
def check_in(
    employee_id: int,
    service: AttendanceService = Depends(get_attendance_service)
):
    try:
        return service.check_in(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/check-out/{employee_id}")
def check_out(
    employee_id: int,
    service: AttendanceService = Depends(get_attendance_service)
):
    try:
        return service.check_out(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_all_attendance(
    service: AttendanceService = Depends(get_attendance_service)
):
    return service.get_all_attendance()


@router.get("/employee/{employee_id}")
def get_employee_attendance(
    employee_id: int,
    service: AttendanceService = Depends(get_attendance_service)
):
    try:
        return service.get_employee_attendance(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/date/{attendance_date}")
def get_attendance_by_date(
    attendance_date: date,
    service: AttendanceService = Depends(get_attendance_service)
):
    return service.get_attendance_by_date(attendance_date)