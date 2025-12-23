from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
import enum
from app.schemas.content import UserRole


class Content(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)
    tags = Column(String(200), nullable=True)