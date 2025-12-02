from .provider import QdrandProvider
from .VectorDBEnum import VectorDBEnum
from controllers.BaseController import BaseController
class VectorDBProviderFactory:
    def __init__(self,config:dict):
        self.config=config
        self.base_controller=BaseController()


    def get_provider(self,provider:str):
        provider=provider.lower()
        if provider==VectorDBEnum.QDRANT.value:
            db_path=self.base_controller.get_database_path(
                db_name=self.config.QDRANT_DB_NAME
            )
            return QdrandProvider(
                db_path=db_path,
                distance_method=self.config.VECTORDB_DISTANCE_METHOD
            )
        return None





