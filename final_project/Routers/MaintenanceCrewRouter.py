from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from Database.createDatabase import *
from Database.Schemas.schemas import *
from Models.Models import *
from Authorization.Authorization import KeycloakJWTBearerHandler, HTTPException

import json


# create tables
Base.metadata.create_all(bind=engine)

maintenancne_crew_router = APIRouter(
    tags=["Maintenance crew"]
)


def verify_crew(role) -> bool:
    if role == "maintenance" or role == "admin":
        return True
    else:
        return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@maintenancne_crew_router.post("/airplane")
def get_crew_airlanes(
    mt_crew_data: MaintenanceCrewModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_crew(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Проверяем сущетсвует ли текущая бригада
    crew =db.query(MAINTENANCE_CREW)\
            .filter(MAINTENANCE_CREW.maintenance_crew_id == mt_crew_data.id_number)\
            .first()
    if crew is None:
        return JSONResponse(status_code=404, content={"message": "crew is not found"})

    # Поиск самолетов, которые обслуживает текущая бригада
    airplanes = db.query(AIRPLANE)\
                  .filter(AIRPLANE.maintenance_crew == crew.maintenance_crew_id)\
                  .all()
    
    data = dict()
    data["airplanes"] = list()
    for a in airplanes:
        d = dict()
        d["airplane_id"] = a.airplane_id
        d["type"] = a.type
        d["condition"] = a.condition
        d["maintenance_crew"] = a.maintenance_crew
        data["airplanes"].append(d)

    return json.loads(json.dumps(data, default=str))


@maintenancne_crew_router.put("/fix")
def fix_airplane(
    airplane_data: AirplaneModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_crew(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Проверяем, существет ли ремонтируемый самолет
    airplane = db.query(AIRPLANE)\
                 .filter((airplane_data.id_number == AIRPLANE.airplane_id) &
                         (airplane_data.type == AIRPLANE.type) &
                         (airplane_data.condition == AIRPLANE.condition) &
                         (airplane_data.maintenance_crew == AIRPLANE.maintenance_crew) &
                         (airplane_data.stage_id == AIRPLANE.stage_id))\
                 .first()
    if airplane is None:
        return JSONResponse(status_code=400, content={"message": "airplane is not found"})
    
    # Чиним самолет
    airplane.condition = 100
    db.commit()

    return {"message": "The airplane has been successfully fixed"}


@maintenancne_crew_router.put("/stage")
def update_airplane_stage(
    airplane_data: AirplaneModel,
    new_stage: str,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
     # Проверка авторизации
    if not verify_crew(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Проверяем, что изменяемый самолет существет
    airplane = db.query(AIRPLANE)\
                 .filter((airplane_data.id_number == AIRPLANE.airplane_id) &
                         (airplane_data.type == AIRPLANE.type) &
                         (airplane_data.condition == AIRPLANE.condition) &
                         (airplane_data.maintenance_crew == AIRPLANE.maintenance_crew) &
                         (airplane_data.stage_id == AIRPLANE.stage_id))\
                 .first()
    if airplane is None:
        return JSONResponse(status_code=404, content={"message": "airplane is not found"})
    
    # Проверяем, что новое состояния есть в БД
    stage = db.query(STAGE)\
              .filter(STAGE.name == new_stage)\
              .first()
    if stage is None:
        return JSONResponse(status_code=404, content={"message": "new stage is not found"})
    
    # Изменяем состояние самолета
    airplane.stage_id = stage.stage_id
    db.commit()

    return {"message": "The stage of airplane has been successfully updated"}
