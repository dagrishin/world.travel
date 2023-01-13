from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from starlette.middleware.cors import CORSMiddleware

from src.attractions.router import attraction_router
from src.auth.router import auth_router
from src.config import settings
from src.travel.router import travel_router

# create instance of the app
app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(auth_router, )
main_api_router.include_router(travel_router, prefix="/travel", tags=["travel"])
main_api_router.include_router(attraction_router, prefix="/attraction", tags=["attraction"])
app.include_router(main_api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
