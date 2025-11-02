from fastapi import FastAPI ,APIRouter
import os

base_router=APIRouter(
    prefix="/api/v1",
    tags=["api_v1"] ,
)

@base_router.get("/")
async def welcom():
    app_name=os.getenv("APP_NAME")
    app_version=os.getenv("VERSION")

    return{
        "message":f"welcom to {app_name} version {app_version}"
    }