from enum import Enum

class VectorDBEnum(Enum):
    QDRANT="qdrant"
    MILVUS="milvus"
    WEAVIATE="weaviate"

class DistanceMethodEnum(Enum):
    COSINE="cosine"
    EUCLIDEAN="euclidean"
    DOT_PRODUCT="dot_product"
