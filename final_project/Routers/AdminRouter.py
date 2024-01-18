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

admin_router = APIRouter(
    tags=["Administrator"]
)


def verify_admin(role) -> bool:
    if role == "admin":
        return True
    else:
        return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================== Менеджмент самолетов ==============================
@admin_router.post("/crewAirplane")
def get_crew_airplane(
    mt_crew_data: MaintenanceCrewModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
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


@admin_router.get("/airplane")
def get_all_ariplanes(
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Получаем список всех самолетов
    airplanes = db.query(AIRPLANE).all()
    
    data = dict()
    data["airplanes"] = list()
    for a in airplanes:
        d = dict()
        d["airplane_id"] = a.airplane_id
        d["type"] = a.type
        d["condition"] = a.condition
        d["maintenance_crew"] = a.maintenance_crew
        d["stage_id"] = a.stage_id
        data["airplanes"].append(d)

    return json.loads(json.dumps(data, default=str))


@admin_router.post("/addAirplane")
def add_airplane(
    airplane_data: AirplaneModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Проверяем, что id добавляемого самолета не существует
    airplane = db.query(AIRPLANE)\
                 .filter(AIRPLANE.airplane_id == airplane_data.id_number)\
                 .first()
    if airplane is not None:
        return JSONResponse(status_code=400, content="Airplane with current id number has already exist")
    
    # Проверяем, что тип самолета не пустой
    if airplane_data.type == "":
        return JSONResponse(status_code=400, content="The type of the airplane is unsatisfactory")

    # Проверяем, что condition добавляемого самолета <= 100 и > 0
    if airplane_data.condition <= 0 or airplane_data.condition > 100:
        return JSONResponse(status_code=400, content="The condition of the airplane is unsatisfactory")
    
    # Проверяем, что обслуживающая бригада назначеная на самолет существет
    crew = db.query(MAINTENANCE_CREW)\
             .filter(MAINTENANCE_CREW.maintenance_crew_id == airplane_data.maintenance_crew)\
             .first()
    if crew is None:
        return JSONResponse(status_code=400, content="Maintenance crew is not exist")
    
    # Добавляем самолет
    arp = AIRPLANE(
        airplane_id=airplane_data.id_number,
        type=airplane_data.type,
        condition=airplane_data.condition,
        maintenance_crew=airplane_data.maintenance_crew
    )
    db.add(arp)
    db.commit()

    return {"message": "Airplane has been successfully added"}


@admin_router.delete("/delAirplane")
def delete_airplane(
    airplane_data: AirplaneModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Проверяем, что удаляемый самолет есть в БД
    airplane = db.query(AIRPLANE)\
                 .filter(AIRPLANE.airplane_id == airplane_data.id_number)\
                 .first()
    if airplane is None:
        return JSONResponse(status_code=400, content="Airplane is not exist")
    
    db.delete(airplane)
    db.commit()

    return {"message": "Airplane has been successfully deleted"}
