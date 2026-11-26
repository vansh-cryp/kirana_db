from fastapi import APIRouter

router = APIRouter(
    prefix="/leave-balance",
    tags=["Leave Balance"]
)


@router.post("/{employee_id}")
def create_leave_balance(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/{employee_id}")
def get_leave_balance(employee_id: int):
    return {"employee_id": employee_id}


@router.patch("/{employee_id}/adjust")
def adjust_leave_balance(employee_id: int):
    return {"employee_id": employee_id}