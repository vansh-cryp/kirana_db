from fastapi import APIRouter

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/")
def create_employee():
    return {"message": "Create employee"}


@router.get("/")
def get_all_employees():
    return {"message": "Get all employees"}


@router.get("/{employee_id}")
def get_employee(employee_id: int):
    return {"employee_id": employee_id}


@router.put("/{employee_id}")
def update_employee(employee_id: int):
    return {"employee_id": employee_id}


@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    return {"employee_id": employee_id}