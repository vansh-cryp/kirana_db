from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class LeaveBalance(Base):
    __tablename__ = "leave_balance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)

    total_leaves = Column(Integer, default=20)
    used_leaves = Column(Integer, default=0)
    remaining_leaves = Column(Integer, default=20)