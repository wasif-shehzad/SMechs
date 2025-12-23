from langchain_openai import OpenAIEmbeddings
from sqlalchemy.orm import Session
from app.schemas.content import ContentCreateRequest
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from app.core.config import settings
from app.utils.factory import vector_store
from langchain_openai import ChatOpenAI  
# from langchain.chains import create_retrieval_chain
from langchain_core.tools import Tool
from langchain.agents import create_agent
from app.services.content import retrieve_knowledge_base
from langgraph.store.memory import InMemoryStore
from langchain.messages import HumanMessage



class RetrievelAgentService:
    def __init__(self, db: Session):
        self.db = db
        # content_service = ContentService(db)
        self.tools = [retrieve_knowledge_base]
        # self.tools = [Tool(name="Retrieve Knowledge Base",func=content_service.retrieve_knowledge_base,description="Get the relevant data for user's query from vector store")]
        self.agent = None

    def get_agent(self):
        """Create and return a retrieval agent."""
        model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, openai_api_key=settings.OPENAI_API_KEY)
        # If desired, specify custom instructions
        prompt = (
            "You have access to a tool that retrieves context from a vector store.\n"
            "Use the tool to help answer user queries."
        )
        self.agent = create_agent(model, tools=self.tools, system_prompt=prompt)
        return True
    
    def answer_query(self, query: str, category: str):
        """Answer user query using the retrieval agent."""
        # agent = self.get_agent()
        if not self.agent:
            self.get_agent()
        response = self.agent.invoke({"messages": [HumanMessage(query)]})
        return response
    