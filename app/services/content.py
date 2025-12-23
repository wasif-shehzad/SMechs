from sqlalchemy.orm import Session
from app.schemas.content import ContentCreateRequest
import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
from app.utils.factory import vector_store
from langchain.tools import tool, ToolRuntime
from pypdf import PdfReader


class ContentService:
    def __init__(self, db: Session):
        self.db = db
        
    async def process_content(self, db: Session, document:PdfReader , category: str) :
        """Upload content."""
        if not document:
            raise ValueError("Data must be provided for creation.")
        chunks = self.create_chunks(document)
        return await self.ingest_to_pinecone(chunks, category)
    
    
    async def ingest_to_pinecone(self, chunks, namespace: str):
        print("Ingesting to pinecone...")
        # vector_store.add_texts is synchronous (returns a list); run it in a thread and await
        resp = await asyncio.to_thread(vector_store.add_texts, chunks, namespace=namespace)
        return resp
        
    def create_chunks(self, document: PdfReader):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""]
        )
        full_text = "".join([page.extract_text() for page in document.pages])
        print("Extracted text from PDF.", full_text[:100])
        print("Creating chunks...")
        chunks = text_splitter.split_text(full_text)
        print(f"Created {len(chunks)} chunks.")
        return chunks
    
    
@tool
def retrieve_knowledge_base( query: str, namespace: str = "general"):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=5, namespace=namespace)
    print(f"Retrieved {len(retrieved_docs)} documents from vector store.")
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    print("Serialized retrieved documents.")
    return serialized