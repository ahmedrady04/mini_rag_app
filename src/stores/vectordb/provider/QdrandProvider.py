from ..VectorDBInterface import VectorDBInterface
from qdrant_client import QdrantClient, models
from ..VectorDBEnum import DistanceMethodEnum
from models.db_schemes import RetrievedDocument
from typing import List
import logging



class QdrandProvider(VectorDBInterface):
    
    def __init__(self,db_path:str, distance_method:str):
        self.db_path=db_path
        self.distance_method=None
        self.client=None

        # Fix: Handle all distance methods and provide a default
        if distance_method == DistanceMethodEnum.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnum.DOT.value:
            self.distance_method = models.Distance.DOT
        elif distance_method == DistanceMethodEnum.EUCLIDEAN.value:
            self.distance_method = models.Distance.EUCLID
        else:
            # Default to COSINE if not specified or invalid
            self.distance_method = models.Distance.COSINE
            logging.warning(f"Unknown distance method '{distance_method}', defaulting to COSINE")
        self.logger=logging.getLogger(__name__)



    def connect(self):
        self.client=QdrantClient(path=self.db_path)

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
                    distance=self.distance_method)
            )


    def insert_one(self,collection_name:str,
                        text:str,
                        vector:List,
                        metadata:dict=None,
                        record_id:str=None)->str:
            
        if not self.is_colection_exists(collection_name=collection_name):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return False
        try:
            # FIXED: Use upsert instead of upload_records
            _=self.client.upsert(
                collection_name=collection_name,
                points=[models.PointStruct(
                    id=record_id,
                    vector=vector,
                    payload={
                        "text":text,
                        "metadata":metadata 
                    }
                )]
            )
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}")
            return False    
        return True
                    

    def insert_many(self,collection_name:str,
                        texts:List,
                        vectors:List,
                        metadata:List=None,
                        record_ids:List=None,
                        batch_size:int=50):
            
        if metadata is None:
            metadata=[None]*len(texts)
        if record_ids is None:
            record_ids=list(range(len(texts)))
        
        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_points = [
                models.PointStruct(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x], 
                        "metadata": batch_metadata[x]
                    }
                )
                for x in range(len(batch_texts))
            ]

            try:
                # FIXED: Use upsert instead of upload_records
                _ = self.client.upsert(
                    collection_name=collection_name,
                    points=batch_points,
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False
        return True

    def search_by_vectors(self, collection_name: str,
                    vector: List,
                    limit: int = 5):
        # FIXED: Use query_points instead of search
        results = self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit
        ).points
        
        if not results or len(results) == 0:
            return None
        
        return [
            RetrievedDocument(**{
                "text": result.payload["text"],
                "score": result.score,
            }) 
            for result in results
        ]