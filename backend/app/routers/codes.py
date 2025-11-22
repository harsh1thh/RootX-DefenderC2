from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from app.services.code_service import code_service

router = APIRouter()

class CodeRequest(BaseModel):
    owner: Optional[str] = None
    ttl_seconds: int = Field(default=3600, gt=0)

class CodeResponse(BaseModel):
    central_id: str
    expires_at: str

@router.post("/codes", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    result = code_service.create_code(owner=request.owner, ttl_seconds=request.ttl_seconds)
    return result
