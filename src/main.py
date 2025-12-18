from fastapi import FastAPI
from routes import base, data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import Settings, get_settings 
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker


app=FastAPI()


async def startup_span():
    settings:Settings = get_settings()
    
    postgres_conn=f"postgresql+asyncpg://{settings.POSTGRESS_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRESS_HOST}:{settings.POSTGRESS_PORT}/{settings.POSTGRES_MAIN_DATABASE}"

    app.db_engine=create_async_engine(postgres_conn)


    app.db_client =sessionmaker(
        app.db_engine,class_=AsyncSession, expire_on_commit=False
    )

    llm_provider_factory=LLMProviderFactory(config=settings)
    vectordb_provider_factory=VectorDBProviderFactory(config=settings)

#genrate LLM provider based on config

    app.generation_client=llm_provider_factory.get_provider(settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(settings.GENERATION_MODEL_ID)

#embedding LLM provider based on config
    app.embedding_client=llm_provider_factory.get_provider(settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(
                    model_id=settings.EMBEDDING_MODEL_ID,
                    embedding_size=settings.EMBEDDING_MODEL_SIZE
    )


#vector DB provider based on config
    vectordb_provider_factory=VectorDBProviderFactory(config=settings)
    app.vectordb_client=vectordb_provider_factory.create(settings.VECTOR_DB_BACKEND)
    app.vectordb_client.connect()


    app.template_parser=TemplateParser(
    language=settings.PRIMARY_LANG,
    default_language=settings.DEFAULT_LANG
    )

async def shutdown_span():
    app.db_engine.dispose()
    app.vectordb_client.disconnect()



# app.router.lifespan.on_startup.append(startup_span)
# app.router.lifespan.on_shutdown.append(shutdown_span)

app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)