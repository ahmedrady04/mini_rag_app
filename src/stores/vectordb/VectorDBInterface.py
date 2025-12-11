from abc import ABC, abstractmethod
from typing import List

class VectorDBInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_colection_exists(self,collection_name:str)->bool:
        pass

    @abstractmethod
    def list_all_collections(self)->list:
        pass

    @abstractmethod
    def get_collection_info(self,collection_name:str)->dict:
        pass

    @abstractmethod
    def delete_collection(self,collection_name:str)->bool:
        pass

    @abstractmethod
    def create_collection(self,collection_name:str,
                            vector_size:int,
                            do_reset:bool=False):
        pass

    @abstractmethod
    def insert_one(self,collection_name:str,
                        text:str,
                        vector:List,
                        metadata:dict=None,
                        record_id:str=None)->str:
        pass

    @abstractmethod
    def insert_many(self,collection_name:str,
                        texts:List,
                        vectors:List,
                        metadatas:List=None,
                        record_ids:List=None,
                        batch_size:int=50):
        pass

    @abstractmethod
    def search_by_vectors(self,collection_name:str,
                                query_vector:List,
                                limit:int=5):
        pass
                                
