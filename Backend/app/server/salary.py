from fastapi import APIRouter

router = APIRouter(prefix="/salary", tags=["Salary"])


@router.post("/generate/{employee_id}")
def generate_salary(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/")
def get_all_salary():
    return {"message": "Get all salary records"}


@router.get("/employee/{employee_id}")
def get_employee_salary(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/employee/{employee_id}/month/{month}")
def get_salary_by_month(employee_id: int, month: str):
    return {
        "employee_id": employee_id,
        "month": month
    }


@router.get("/{salary_id}")
def get_salary(salary_id: int):
    return {"salary_id": salary_id}