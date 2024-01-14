from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from Database.createDatabase import *
from Database.Schemas.schemas import *
from Models.Models import *

import json


# create tables
Base.metadata.create_all(bind=engine)

passenger_router = APIRouter(
    tags=["Passenger"]
)


def verify_passenger(role) -> bool:
    if role == "passenger" or role == "admin":
        return True
    return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@passenger_router.post("/ticket")
def get_ticket(
    passenger_data: PassengerModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_passenger(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Проверяем есть ли пассажир в базе данных
    passenger = db.query(PASSENGER)\
                  .filter((PASSENGER.passenger_passport_id == passenger_data.passport) &\
                          (PASSENGER.name == passenger_data.name))\
                  .first()
    if passenger is None:
        return JSONResponse(status_code=404, content={"message": "passenger is not found"})
    
    # Находим билеты купленные пассажиром
    tickets = db.query(TICKET)\
                .filter(TICKET.passenger_id == passenger_data.passport)\
                .all()
    data = dict()
    data["tickets"] = list()
    for t in tickets:
        d = dict()
        d["ticket_id"] = t.ticket_id
        d["flight_id"] = t.flight_id
        d["passenger_id"] = t.passenger_id
        d["price"] = t.price
        d["departure_date"] = t.departure_date
        d["date_sale"] = t.date_sale
        data["tickets"].append(d)

    return json.loads(json.dumps(data, default=str))


@passenger_router.post("/buy")
def buy_ticket(
    ticket_data: TicketModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_passenger(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    
    # Создание билета для занесения в БД
    ticket = TICKET(
        flight_id=ticket_data.flight_id,
        passenger_id=ticket_data.passenger_id,
        price=ticket_data.price,
        departure_date=datetime.strptime(ticket_data.departure_date, '%Y-%m-%d %H:%M:%S.%f'),
        date_sale=datetime.strptime(ticket_data.date_sale, '%Y-%m-%d %H:%M:%S.%f')
    )
    db.add(ticket)
    db.commit()

    return {"message": "Билет успешно куплен"}


@passenger_router.delete("/ticket")
def delete_ticket(
    passenger_data: PassengerModel,
    ticket_number: int,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    # Проверка авторизации
    if not verify_passenger(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    # Проверяем есть ли пассажир в базе данных
    passenger = db.query(PASSENGER)\
                  .filter((PASSENGER.passenger_passport_id == passenger_data.passport) &\
                          (PASSENGER.name == passenger_data.name))\
                  .first()
    if passenger is None:
        return JSONResponse(status_code=404, content={"message": "passenger is not found"})
    
    # Проверяем есть ли купленый билет с заданым номером
    ticket = db.query(TICKET)\
               .filter((TICKET.ticket_id == ticket_number) &\
                       (TICKET.passenger_id == passenger_data.passport))\
               .first()
    if ticket is None:
        return JSONResponse(status_code=404, content={"message": "ticket is not found"})
    
    db.delete(ticket)
    db.commit()

    return {"message": "Билет успешно удален"}
