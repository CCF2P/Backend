from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


# Create a DeclarativeMeta instance
Base = declarative_base()


class MAINTENANCE_CREW(Base):
    __tablename__ = "maintenance_crew"
    maintenance_crew_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(100))


class AIRPLANE(Base):
    __tablename__ = "airplane"
    airplane_id = Column(
        Integer, 
        nullable=False,
        primary_key=True, 
        autoincrement=True
    )
    type = Column(String(100))
    condition = Column(Integer)
    maintenance_crew = Column(ForeignKey(MAINTENANCE_CREW.maintenance_crew_id))

class DESTINATION(Base):
    __tablename__ = "destination"
    destination_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    destination = Column(String(100))


class FLIGHT(Base):
    __tablename__ = "flight"
    flight_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    departure_time = Column(DateTime, nullable=False)
    destination_id = Column(ForeignKey(DESTINATION.destination_id))
    airplane_id = Column(ForeignKey(AIRPLANE.airplane_id))


class PASSENGER(Base):
    __tablename__ = "passenger"
    passenger_passport_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String(100))


class TICKET(Base):
    __tablename__ = "ticket"
    ticket_id = Column(
        Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True
    )
    flight_id = Column(ForeignKey(FLIGHT.flight_id))
    passenger_id = Column(ForeignKey(PASSENGER.passenger_passport_id))
    price = Column(Integer)
    departure_date = Column(DateTime)
    date_sale = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return f"{self.ticket_id} | {self.flight_id} | \
                {self.passenger_id} | {self.price} | \
                {self.departure_date} | {self.date_sale}"
