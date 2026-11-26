from fastapi import APIRouter

router = APIRouter(prefix="/leaves", tags=["Leave Management"])


@router.post("/apply/{employee_id}")
def apply_leave(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/")
def get_all_leaves():
    return {"message": "Get all leaves"}


@router.get("/employee/{employee_id}")
def get_employee_leaves(employee_id: int):
    return {"employee_id": employee_id}


@router.get("/{leave_id}")
def get_leave(leave_id: int):
    return {"leave_id": leave_id}


@router.patch("/{leave_id}/approve")
def approve_leave(leave_id: int):
    return {"leave_id": leave_id}


@router.patch("/{leave_id}/reject")
def reject_leave(leave_id: int):
    return {"leave_id": leave_id}


@router.delete("/{leave_id}")
def delete_leave(leave_id: int):
    return {"leave_id": leave_id}