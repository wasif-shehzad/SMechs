from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.content import ContentCreateRequest, ContentCreateResponse
from app.services.content import ContentService
from app.services.retrievel_agent import RetrievelAgentService 
from app.db.session import get_db
from pypdf import PdfReader


router = APIRouter()


@router.post("/", response_model=ContentCreateResponse, status_code=status.HTTP_201_CREATED)
async def add(
        file: UploadFile = File(...),
        category: str = "general", 
        db: Session = Depends(get_db)
        ):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    reader = PdfReader(file.file)
    c_service = ContentService(db)
    content_response = await c_service.process_content(db, reader, category)
    return {"success": True}

@router.post("/chat", response_model=dict, status_code=status.HTTP_200_OK)
def chat(
        request: dict,
        db: Session = Depends(get_db)
        ):
    query = request.get("query")
    category = request.get("category", "general")
    if not query:
        raise HTTPException(status_code=400, detail="Query must be provided")
    
    agent = RetrievelAgentService(db)
    print("Answering query via agent..., ", query, category)
    answer = agent.answer_query(query, category)
    return answer
