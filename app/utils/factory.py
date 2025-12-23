from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
# from langchain_core.vectorstores import InMemoryVectorStore
from app.core.config import settings


# Initialize shared embeddings
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.OPENAI_API_KEY
)

vector_store = PineconeVectorStore(
    index_name=settings.PINECONE_INDEX_NAME,
    embedding=embeddings,
    pinecone_api_key=settings.PINECONE_API_KEY
)


# vector_store = InMemoryVectorStore(embeddings)