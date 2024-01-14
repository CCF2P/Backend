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


@admin_router.put("/passenger")
def update_passenger_data(
    passenger_data: PassengerModel,
    new_passenger_data: PassengerModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Проверяем новые данные пассажира
    # Проверяем, чтобы паспорт состоял из 10 цифр
    if passenger_data.passport > 9999999999 or passenger_data < 1000000000:
        return JSONResponse(status_code=404, content={"message": "passenger's passport is not valid"})
    
    # Проверяем, чтобы имя пассажира не было пустым
    if passenger_data.name == "":
        return JSONResponse(status_code=404, content={"message": "passenger's name is empty"})

    # Проверяем есть ли пассажир в базе данных
    passenger = db.query(PASSENGER)\
                  .filter((PASSENGER.passenger_passport_id == passenger_data.passport) &\
                          (PASSENGER.name == passenger_data.name))\
                  .first()
    if passenger is None:
        return JSONResponse(status_code=404, content={"message": "passenger is not found"})
    
    # Обновляем данные
    passenger.name = new_passenger_data.name
    passenger.passenger_passport_id = new_passenger_data.passport

    # Сохраняем изменения в базу данных
    db.commit()

    return {"message": "Данные пассажира успешно обновлены"}


@admin_router.delete("/delpassanger")
def delete_passanger(
    passenger_data: PassengerModel,
    new_passenger_data: PassengerModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Проверяем есть ли пассажир в базе данных
    passenger = db.query(PASSENGER)\
                  .filter((PASSENGER.passenger_passport_id == passenger_data.passport) &\
                          (PASSENGER.name == passenger_data.name))\
                  .first()
    if passenger is None:
        return JSONResponse(status_code=404, content={"message": "passenger is not found"})
    
    db.delete(passenger)
    db.commit()

    return {"message": "Пассажир успешно ужален"}
