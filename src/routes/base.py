from fastapi import FastAPI ,APIRouter,Depends
import os
from helpers.config import get_settings ,Settings
base_router=APIRouter(
    prefix="/api/v1",
    tags=["api_v1"] ,
)

@base_router.get("/")
async def welcom(app_settings:Settings=Depends(get_settings)):
    app_name=app_settings.APP_NAME
    app_version=app_settings.VERSION
    app_file_types=app_settings.FILEE_ALLOWED_TYPES
    app_file_max_size=app_settings.FILE_MAX_SIZE

    return{
        "message":f"welcom to {app_name} version {app_version}"
    }