from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale=1024*1024  # convert to MB

    
    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILEE_ALLOWED_TYPES:
            return False ,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False ,ResponseSignal.FILE_SIZE_EXCEEDED.value
        return True ,ResponseSignal.FILE_VALIDATED_SUCCESS.value  


    def generate_unique_filepath(self, original_filename: str, project_id: str) -> str:
        random_key=self.generate_random_string()
        project_path=ProjectController().get_project_directory(project_id=project_id)


        

        clean_filename=self.get_clean_filename(
            original_filename=original_filename
        )
    

        new_file_path=os.path.join(
            project_path,
            random_key + "_" + clean_filename
        )

        while os.path.exists(new_file_path):
            random_key=self.generate_random_string()
            new_file_path=os.path.join(
                project_path,
                random_key + "_" + clean_filename
            )

        return new_file_path,  random_key + "_" + clean_filename




    def get_clean_filename(self, original_filename: str) -> str:
        # Remove special characters except for dot and underscore
        clean_name = re.sub(r'[^a-zA-Z0-9._]', '_', original_filename)
        # replace spaces with underscores
        clean_name = clean_name.replace(' ', '_')
        return clean_name
 