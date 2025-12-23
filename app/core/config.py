from typing import Any, Dict, List, Optional, Union, ClassVar
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "SMechs API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    PORT: int
    DEBUG: bool
    ENV:str  = "production"
    TESTING: bool = True # Set to True for testing environment   
    # Security
    RELOAD: bool = True  # Enable auto-reload in development
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600
    ALGORITHM: ClassVar[str] = 'HS256'
    SECRET_KEY: str
    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str 
    POSTGRES_PORT: str
    
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_REGION: str
    PINECONE_INDEX_NAME: str
    
    
    
    
    DATABASE_URL: Optional[str] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
