from .LLMEnum import LLMEnum
from stores.llm.providers.OpenAIProvider import OpenAIProvider
from stores.llm.providers.CoHereProvider import CoHereProvider

class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def get_provider(self, provider: str):
        provider = provider.lower()
        
        if provider == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                apikey=self.config.OPENAI_API_KEY,
                base_url=self.config.OPENAI_API_URL,  # ✅ Fixed: api_url → base_url
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_generation_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE,
            )
        
        if provider == LLMEnum.COHERE.value:
            return CoHereProvider(
                apikey=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                default_generation_output_max_tokens=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DAFAULT_TEMPERATURE,
            )
        
        return None
    
     