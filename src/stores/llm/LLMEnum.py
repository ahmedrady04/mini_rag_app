from enum import Enum

class LLMEnum(Enum):
    OPENAI="openai"
    COHERE="cohere"


class OpenAIEnum(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"


class CohereEnum(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="CHATBOT"

    DOCUMENT="search_document"
    QUERY="search_query"

class DocumentTypeEnum(Enum):
    DOCUMENT="document"
    QUERY="query"
