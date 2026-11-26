from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from database import Base

class Overtime(Base):
    __tablename__ = "overtime"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    extra_hours = Column(Float, nullable=False)
    overtime_rate = Column(Float, nullable=False)