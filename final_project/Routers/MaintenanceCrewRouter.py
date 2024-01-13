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
        d["number"] = a.number
        d["maintenance_crew"] = a.maintenance_crew
        data["airplanes"].append(d)

    return json.loads(json.dumps(data, default=str))


@maintenancne_crew_router.post("/fix")
def fix_airplane(
    airplane_data: AirplaneModel,
    mt_crew_id: int,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_crew(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Проверяем текущая ли бригада отвечает за самолет
    airplane = db.query(AIRPLANE)\
                 .filter(AIRPLANE.airplane_id == airplane_data.id_number)\
                 .first()
    if airplane.maintenance_crew != mt_crew_id:
        return JSONResponse(status_code=400,
                            content={"message": "The current crew is not responsible for the selected airplane"})
    
    # Чиним самолет
    airplane.condition = 100
    db.commit()

    return {"message": "The airplane has been successfully fixed"}
