from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from repositories.attendance_repository import AttendanceRepository
from services.attendance_service import AttendanceService

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


# Dependency injection
def get_attendance_service(db: Session = Depends(get_db)):
    repository = AttendanceRepository(db)
    return AttendanceService(repository)


# CHECK IN
@router.post("/check-in/{employee_id}")
def check_in(
    employee_id: int,
    service: AttendanceService = Depends(get_attendance_service)
):
    try:
        return service.check_in(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# CHECK OUT
@router.post("/check-out/{employee_id}")
def check_out(
    employee_id: int,
    service: AttendanceService = Depends(get_attendance_service)
):
    try:
        return service.check_out(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# GET ALL ATTENDANCE
@router.get("/")
def get_all_attendance(
    service: AttendanceService = Depends(get_attendance_service)
):
    return service.get_all_attendance()


# GET EMPLOYEE ATTENDANCE
@router.get("/employee/{employee_id}")
def get_employee_attendance(
    employee_id: int,
    service: AttendanceService = Depends(get_attendance_service)
):
    try:
        return service.get_employee_attendance(employee_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# GET ATTENDANCE BY DATE
@router.get("/date/{attendance_date}")
def get_attendance_by_date(
    attendance_date: date,
    service: AttendanceService = Depends(get_attendance_service)
):
    return service.get_attendance_by_date(attendance_date)