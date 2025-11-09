from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader as TxtLoader
from models.enums import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter



class ProcessController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()

        self.project_id=project_id
        self.project_pass=ProjectController().get_project_directory(project_id=project_id)

    def get_file_extension(self, file_id: str ):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self, file_id: str):
        file_path=os.path.join(
            self.project_pass,
            file_id
        )
        file_ext=self.get_file_extension(file_id=file_id).lower()

        if file_ext==ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_ext==ProcessingEnum.TXT.value:
            return TxtLoader(file_path, encoding='utf-8')
        else:
            return None
        
    def get_file_content(self, file_id:str):
            loader=self.get_file_loader(file_id)
            return loader.load()
    def process_file_content(self, file_content:list,file_id: str,
                              chunk_size:int=100, overlap_size:int=20):
            text_splitter=RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=overlap_size,
                length_function=len,
            )
            file_content_texts=[
                rec.page_content
                for rec in file_content
            ]
            file_metadata_texts=[
                rec.metadata 
                for rec in file_content
            ]

            chunks=text_splitter.create_documents(
                file_content_texts,
                metadatas=file_metadata_texts               
            )

            return chunks
