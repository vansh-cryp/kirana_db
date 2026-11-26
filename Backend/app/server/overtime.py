from fastapi import APIRouter

router = APIRouter(prefix="/overtime", tags=["Overtime"])


@router.post("/")
def create_overtime():
    return {"message": "Create overtime record"}


@router.get("/")
def get_all_overtime():
    return {"message": "Get all overtime records"}


@router.get("/employee/{employee_id}")
def get_employee_overtime(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/hours/{employee_id}")
def get_overtime_hours(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/pay/{employee_id}")
def get_overtime_pay(employee_id: int):
    return {"employee_id": employee_id}