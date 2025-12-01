from ..LLMInterface import LLMInterface
from openai import OpenAI
import logging
from ..LLMEnum import OpenAIEnum



class OpenAIProvider(LLMInterface):
    def __init__(self,apikey:str,api_url:str=None,
                        default_input_max_characters:int=1000,
                        default_generation_output_max_tokens:int=1000,
                        default_temperature:float=0.1,
                                    ): 
        self.apikey=apikey
        self.api_url=api_url
        self.default_input_max_characters=default_input_max_characters
        self.default_generation_output_max_tokens=default_generation_output_max_tokens
        self.default_temperature=default_temperature

        self.generation_model_id=None

        self.embedding_model_id=None
        self.embedding_size=None
        self.client=OpenAI(
            api_key=self.apikey,
            api_base=self.api_url
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
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model is not set.")   
            return None
        max_output_tokens=max_output_tokens if max_output_tokens else self.default_generation_output_max_tokens
        temperature=temperature if temperature else self.default_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt,role=OpenAIEnum.USER.value))
        
        responce=self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
        return responce.choices[0].message.content


def embed_text(self,text:str,document_type:str=None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")   
            return None
        if not responce or responce.data or len(responce.data)==0, or not responce.data[0].embedding:
            self.logger.error("Failed to get embedding from OpenAI.")
            return None
        
        responce=self.client.embeddings.create(
            input=text,
            model=self.embedding_model_id
        )
        return responce.data[0].embedding

def construct_prompt(self,prompt:str,role:str):
    return{
        "role":role,
        "content":self.process_text(prompt)
    }



