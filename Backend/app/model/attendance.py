from sqlalchemy import Column, Integer, Date, Time, Float, ForeignKey
from database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(Date, nullable=False)
    check_in = Column(Time)
    check_out = Column(Time)
    working_hours = Column(Float)