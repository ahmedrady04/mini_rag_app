import cohere
from ..LLMInterface import LLMInterface
from ..LLMEnum import CohereEnum, DocumentTypeEnum
import logging

class CoHereProvider(LLMInterface):
    def __init__(self,apikey:str,
                        default_input_max_characters:int=1000,
                        default_generation_output_max_tokens:int=1000,
                        default_temperature:float=0.1,
                                    ): 
        self.apikey=apikey
        self.default_input_max_characters=default_input_max_characters
        self.default_generation_output_max_tokens=default_generation_output_max_tokens
        self.default_temperature=default_temperature

        self.generation_model_id=None

        self.embedding_model_id=None
        self.embedding_size=None

        self.client=cohere.ClientV2(
            api_key=self.apikey,
        )

        self.logger=logging.getLogger(__name__)

    def set_generation_model(self,model_id:str):
        self.generation_model_id=model_id

    def set_embedding_model(self,model_id:str,embedding_size:int ):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size


    def process_text(self,text:str):
        if len(text)>self.default_input_max_characters:
            return text[:self.default_input_max_characters].strip()
        return text
    
    def genrate_text(self,prompt:str,chat_history:list=[],
                        max_output_tokens:int=None, temperature:float=None):
        
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model is not set.")   
            return None
        max_output_tokens=max_output_tokens if max_output_tokens else self.default_generation_output_max_tokens
        temperature=temperature if temperature else self.default_temperature

        
        responce=self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature,
            messages=self.process_text(prompt)
        )

        if not responce or not responce.text:
            self.logger.error("No response from Cohere chat generation.")
            return None
        
        
        return responce.text
    
    def embed_text(self,text:str,document_type:str=None):
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")   
            return None
        
        input_type=CohereEnum.DOCUMENT.value  
        if document_type==DocumentTypeEnum.QUERY.value:
            input_type=CohereEnum.QUERY.value
            
        

        responce=self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=["float"]
        )

        if not responce or not responce.embeddings or len(responce.embeddings)==0 or not responce.embeddings[0]:
            self.logger.error("No response from Cohere embedding.")
            return None
        
        return responce.embeddings.float[0]

    def construct_prompt(self,prompt:str,role:str):
        return{
            "role":role,
            "content":self.process_text(prompt)
        }

