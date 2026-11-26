from fastapi import APIRouter

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/check-in/{employee_id}")
def check_in(employee_id: int):
    return {"employee_id": employee_id}


@router.post("/check-out/{employee_id}")
def check_out(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/")
def get_all_attendance():
    return {"message": "Get all attendance records"}


@router.get("/employee/{employee_id}")
def get_employee_attendance(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/date/{attendance_date}")
def get_attendance_by_date(attendance_date: str):
    return {"date": attendance_date}