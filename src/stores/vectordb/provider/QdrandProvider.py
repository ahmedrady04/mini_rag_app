from ..VectorDBInterface import VectorDBInterface
from qdrant_client import QdrantClient, models
from ..VectorDBEnum import DistanceMethodEnum
from typing import List
import logging



class QdrandProvider(VectorDBInterface):
    
    def __init__(self,db_path:str, distance_method:str):
        self.db_path=db_path
        self.distance_method=distance_method
        self.client=None

        if distance_method not in ['Cosine','Euclidean','Dot']:
            raise ValueError("Invalid distance method. Choose from 'Cosine', 'Euclidean', 'Dot'.")
        if distance_method==DistanceMethodEnum.COSINE.value
            self.distance_metric="Cosine"
        elif distance_method==DistanceMethodEnum.EUCLIDEAN.value:
            self.distance_metric="Euclidean"
        elif distance_method==DistanceMethodEnum.DOT_PRODUCT.value:
            self.distance_metric="Dot"
        

        self.logger=logging.getLogger(__name__)



    def connect(self):
        self.client=QdrantClient(path=self.db_path,)

    def disconnect(self):
        if self.client:
            self.client.close()

    def is_colection_exists(self,collection_name:str)->bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self)->list:
        return self.client.get_collections()

    def get_collection_info(self,collection_name:str)->dict:

        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self,collection_name:str)->bool:
        if self.is_colection_exists(collection_name=collection_name):
          return self.client.delete_collection(collection_name=collection_name)
       

    def create_collection(self,collection_name:str,
                            vector_size:int,
                            do_reset:bool=False):
        if do_reset and self.is_colection_exists(collection_name=collection_name):
            _ = self.delete_collection(collection_name=collection_name)
        if not self.is_colection_exists(collection_name=collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=self.distance_methode)



    def insert_one(self,collection_name:str,
                        text:str,
                        vector:List,
                        metadata:dict=None,
                        record_id:str=None)->str:
        pass

    def insert_many(self,collection_name:str,
                        texts:List,
                        vectors:List,
                        metadatas:List=None,
                        record_ids:List=None,
                        batch_size:int=50):
        pass

    def search_by_vectors(self,collection_name:str,
                                query_vector:List,
                                limit:int=5):
            return self.client.search(
                collection_name=collection_name,
                query_vector=vector,
                limit=limit
            )
        