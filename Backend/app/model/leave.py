from sqlalchemy import Column, Integer, Date, String, ForeignKey, Text
from database import Base

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    leave_type = Column(String(50))
    status = Column(String(30), default="PENDING")
    reason = Column(Text)