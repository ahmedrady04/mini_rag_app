from .BaseController import BaseController
from models.db_schemes import Project
from models.db_schemes import DataChunk
from stores.llm.LLMEnum import DocumentTypeEnum

import json


class NlpController(BaseController):
    def __init__(self,vectordb_client,generation_client
                    ,embedding_client,template_parser):
        super().__init__()

        self.vectordb_client=vectordb_client
        self.generation_client=generation_client
        self.embedding_client=embedding_client
        self.template_parser=template_parser


    def create_collection_name(self,project_id:str):
        return f"collection_{project_id}".strip()
    

    def reset_vector_db_collection_info(self,project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_collection_info(self,project:Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info=self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info,default=lambda x:x.__dict__)
        )
    def index_into_vector_db(self,project:Project,
                                chuncks:list[DataChunk],
                                chuncks_ids:list[int],
                                do_reset:bool=False):\
        ## step1: get collection name                
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items

        texts=[
            chunk.chunk_text for chunk in chuncks
        ]
        metadata=[
            chunk.chunk_metadata for chunk in chuncks
        ]
        vectors=[
            self.embedding_client.embed_text(
                text=text,
                document_type=DocumentTypeEnum.DOCUMENT.value)

                for text in texts
            
        ]

        # step3: create collection if not exists
        _ = self.vectordb_client.create_collection(
            collection_name=collection_name,
            vector_size=self.embedding_client.embedding_size,
            do_reset=do_reset
        )

        # step4: insert items
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            vectors=vectors,
            metadata=metadata,
            record_ids=chuncks_ids,
        )
        return True

    def search_similar_documents(self,project:Project,text:str,limit:int=5):
        collection_name = self.create_collection_name(project_id=project.project_id)
        vector=self.embedding_client.embed_text(
            text=text,
            document_type=DocumentTypeEnum.QUERY.value
        )

        if not vector or len(vector) == 0:
            return False
        
        results=self.vectordb_client.search_by_vectors(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not results:
            return False

        return results
    

    def answer_rag_question(self,project:Project,query:str,limit:int=10):
        answer, full_prompt, chat_history = None, None, None

        # step1: retrieve related documents
        retrieved_documents=self.search_similar_documents(
            project=project,
            text=query,
            limit=limit
        )
        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        system_prompt= self.template_parser.get_template("rag","system_prompt")


        document_prompt= "\n".join([
        self.template_parser.get_template("rag","document_prompt",{
            "doc_num": idx + 1,
            "chunk_text":  self.generation_client.process_text(doc.text),
        })

        for idx, doc in enumerate(retrieved_documents)

        ])

        footer_prompt= self.template_parser.get_template("rag","footer_prompt",{
            "query":query
        })


        # step3: Construct Generation Client Prompts
        chat_history=[
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enum.SYSTEM.value
                )
        
        ]

        full_prompt= "\n\n".join([document_prompt,footer_prompt])

        # step4: Retrieve the Answer
        
        answer=self.generation_client.genrate_text(
            prompt=full_prompt,
            chat_history=chat_history,
            )
        return answer, full_prompt, chat_history

