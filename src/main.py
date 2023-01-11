from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter

from src.attractions.router import attraction_router
from src.auth.router import auth_router
from src.travel.router import travel_router

# create instance of the app
app = FastAPI(title="world_travel")

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
main_api_router.include_router(travel_router, prefix="/travel", tags=["travel"])
main_api_router.include_router(attraction_router, prefix="/attraction", tags=["attraction"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
