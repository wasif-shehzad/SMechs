from pydantic import BaseModel, Field, validator
from typing import Optional, Dict
import re

# class HealthRequest(BaseModel):
  


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status of the service", example="ok")
    message: str = Field(..., description="Additional message about the service health", example="Service is running")
     