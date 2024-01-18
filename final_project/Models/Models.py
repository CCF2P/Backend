from pydantic import BaseModel, Field


class KeycloakToken(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    not_before_policy: int = Field(alias="not-before-policy")
    session_state: str
    scope: str


class AdminModel(BaseModel):
    pass


class PassengerModel(BaseModel):
    passport: int
    name: str


class TicketModel(BaseModel):
    flight_id: int
    passenger_id: int
    price: int
    departure_date: str
    date_sale: str


class MaintenanceCrewModel(BaseModel):
    id_number: int
    name: str


class AirplaneModel(BaseModel):
    id_number: int
    type: str
    condition: str
    maintenance_crew: int
    stage_id: int
