from fastapi import FastAPI
import uvicorn

from Routers.PassengerRouter import passenger_router
from Routers.MaintenanceCrewRouter import maintenancne_crew_router
from Routers.AdminRouter import admin_router


app = FastAPI()

app.include_router(maintenancne_crew_router)
app.include_router(admin_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port="8000")
