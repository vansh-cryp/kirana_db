from fastapi import FastAPI
from database import Base, engine
from models import *
from routers.attendance_router import router as attendance_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(attendance_router)