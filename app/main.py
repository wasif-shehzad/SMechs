from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback
import os
from app.utils.error import CustomError, NotificationError

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="SMechs API",
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )
    # Set all CORS enabled origins
    origins = [
    "http://localhost:5173",
    ]
    app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Add custom exception handler
    @app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):
        tb = traceback.format_exc()
        file_path = traceback.extract_tb(exc.__traceback__)[-1].filename if exc.__traceback__ else "Unknown"
        folder = os.path.dirname(file_path)
        return JSONResponse(
            status_code=500,
            content={
                "error": str(exc),
                "file": file_path,
                "folder": folder,
                "traceback": tb
            },
        )
    @app.exception_handler(CustomError)
    async def custom_error_handler(request:Request, exc:CustomError):
        return JSONResponse(
                  status_code=exc.status_code if hasattr(exc, "status_code") else 400,
        content={
            "success": exc.success,
            "message": exc.message,
        },
        )
    @app.exception_handler(NotificationError)
    async def model_error_handler(request: Request, exc: NotificationError):
        return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": exc.success,
        },
        )
    return app


app = create_application()

@app.on_event("startup")
async def startup_event():
    print("Starting up the SMechs application...")
    # Create database tables
    Base.metadata.create_all(bind=engine)

        

if __name__ == "__main__":
    print("starting the SMechs API server")
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="info"
    )
