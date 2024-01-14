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


@admin_router.post("/passenger")
def add_passanger(
    passenger_data: PassengerModel,
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

    # Проверяем данные пассажира
    # Проверяем, чтобы паспорт состоял из 10 цифр
    if passenger_data.passport > 9999999999 or passenger_data < 1000000000:
        return JSONResponse(status_code=404, content={"message": "passenger's passport is not valid"})
    
    # Проверяем, чтобы имя пассажира не было пустым
    if passenger_data.name == "":
        return JSONResponse(status_code=404, content={"message": "passenger's name is empty"})
    
    # Добавляем пассажира
    psg = PASSENGER(
        passenger_passport_id=passenger_data.passport,
        name=passenger_data.name
    )
    db.add(psg)

    # Сохраняем изменения в базу данных
    db.commit()

    return {"message": "The passenger has been added successfully"}


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
    
    # Проверяем есть ли пассажир в базе данных
    passenger = db.query(PASSENGER)\
                  .filter((PASSENGER.passenger_passport_id == passenger_data.passport) &\
                          (PASSENGER.name == passenger_data.name))\
                  .first()
    if passenger is None:
        return JSONResponse(status_code=404, content={"message": "passenger is not found"})

    # Проверяем новые данные пассажира
    # Проверяем, чтобы паспорт состоял из 10 цифр
    if new_passenger_data.passport > 9999999999 or passenger_data < 1000000000:
        return JSONResponse(status_code=404, content={"message": "passenger's passport is not valid"})
    
    # Проверяем, чтобы имя пассажира не было пустым
    if new_passenger_data.name == "":
        return JSONResponse(status_code=404, content={"message": "passenger's name is empty"})
    
    # Обновляем данные
    passenger.name = new_passenger_data.name
    passenger.passenger_passport_id = new_passenger_data.passport

    # Сохраняем изменения в базу данных
    db.commit()

    return {"message": "The passenger's data has been updated successfully"}


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

    return {"message": "The passenger has been deleted successfully"}


@admin_router.get("/alltickets")
def get_all_tickets(
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Вытаскиваем список всех билетов из БД
    tickets = db.query(TICKET)\
                .all()
    
    data = dict()
    data["tickets"] = list()
    for t in tickets:
        d = dict()
        d["ticket_id"] = t.ticket_id
        d["flight"] = t.flight_id
        d["passport"] = t.passenger_id
        d["price"] = t.price
        d["departure_date"] = t.departure_date
        d["date_sale"] = t.date_sale
        data["tickets"].append(d)

    return json.loads(json.dumps(data, default=str))


@admin_router.post("/passengerTickets")
def get_all_tickets(
    passenger_data: PassengerModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Проверяем есть ли пассажир в базе данных
    passenger = db.query(PASSENGER)\
                  .filter((PASSENGER.passenger_passport_id == passenger_data.passport) &
                          (PASSENGER.name == passenger_data.name))\
                  .first()
    if passenger is None:
        return JSONResponse(status_code=404, content={"message": "passenger is not found"})

    # Вытаскиваем список всех билетов пассажира из БД
    tickets = db.query(TICKET)\
                .filter(TICKET.passenger_id == passenger_data.passport)\
                .all()
    
    data = dict()
    data["tickets"] = list()
    for t in tickets:
        d = dict()
        d["ticket_id"] = t.ticket_id
        d["flight"] = t.flight_id
        d["passport"] = t.passenger_id
        d["price"] = t.price
        d["departure_date"] = t.departure_date
        d["date_sale"] = t.date_sale
        data["tickets"].append(d)

    return json.loads(json.dumps(data, default=str))


@admin_router.delete("/deletePassengerTicket")
def get_all_tickets(
    passenger_data: PassengerModel,
    ticket_number: int,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Проверяем есть ли пассажир в базе данных
    passenger = db.query(PASSENGER)\
                  .filter((PASSENGER.passenger_passport_id == passenger_data.passport) &
                          (PASSENGER.name == passenger_data.name))\
                  .first()
    if passenger is None:
        return JSONResponse(status_code=404, content={"message": "passenger is not found"})

    # Вытаскиваем билет пассажира из БД
    ticket = db.query(TICKET)\
                .filter(TICKET.passenger_id == ticket_number)\
                .first()
    
    # Удаляем билет
    db.delete(ticket)
    db.commit()

    return {"message": "The passenger has been removed successfully"}
