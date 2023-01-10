from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter

from src.auth.router import auth_router

# create instance of the app
app = FastAPI(title="world_travel")

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
