from sqlalchemy import Column, Integer, Float, ForeignKey, String
from database import Base

class Salary(Base):
    __tablename__ = "salary"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    month = Column(String(20), nullable=False)

    fixed_salary = Column(Float, nullable=False)
    overtime_pay = Column(Float, default=0)
    bonus = Column(Float, default=0)
    deductions = Column(Float, default=0)
    net_salary = Column(Float, nullable=False)