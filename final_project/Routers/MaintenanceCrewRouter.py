from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from Database.createDatabase import *
from Database.Schemas.schemas import *
from Models.Models import *

import json


# create tables
Base.metadata.create_all(bind=engine)

maintenancne_crew_router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance crew"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@maintenancne_crew_router.get("/")
def get():
    return "Hello"
