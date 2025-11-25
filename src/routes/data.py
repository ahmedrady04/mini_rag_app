from fastapi import FastAPI ,APIRouter,Depends ,UploadFile ,status
from fastapi.responses import JSONResponse 
import os
from helpers.config import get_settings, Settings
from controllers import DataController
from controllers import ProjectController
from aiofile import async_open
from models import ResponseSignal
import logging

logger = logging.getLogger("uvicorn.error")



data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api/v1","data"],
)
@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,
                      app_setting :Settings=(Depends(get_settings))):



  #validate the file properties
  data_controller=DataController()
  is_valid ,result_signal =data_controller.validatje_uploaded_file(file=file)

  if not is_valid:
      return JSONResponse(
          status_code=status.HTTP_400_BAD_REQUEST,
          content={
              "status":"failed",
              "signal":result_signal
          }
      )

  project_dir_path=ProjectController().get_project_directory(project_id=project_id)
  file_path, file_id = data_controller.generate_unique_filepath(
        original_filename=file.filename,
        project_id=project_id
    )
  try:
    async with async_open(file_path,'wb') as out_file:
       while (chunk:=await file.read(app_setting.FILE_DEFAULT_CHUNK_SIZE)):
         await out_file.write(chunk)

  except Exception as e:

        logger.error(f"Error while uploadaing file : {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status":"failed",
                "signal":ResponseSignal.FILE_UPLOAD_FAILED.value,
                "error":str(e)
            }
        )


  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
        "status":"success",
        "signal":ResponseSignal.FILE_UPLOAD_SUCCESS.value,
        "file_id":file_id
    }
   )
