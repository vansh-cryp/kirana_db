from sqlalchemy.orm import Session
from model.leave_balance import LeaveBalance


class LeaveBalanceRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_employee(self, employee_id: int):
        return self.db.query(LeaveBalance).filter(
            LeaveBalance.employee_id == employee_id
        ).first()

    # commit=False lets the caller save several rows in one transaction
    def save(self, balance: LeaveBalance, commit: bool = True):
        self.db.add(balance)
        if commit:
            self.db.commit()
            self.db.refresh(balance)
        return balance
