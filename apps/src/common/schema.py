from typing import Optional
from pydantic import BaseModel, Field

class OkError(BaseModel):
    ok: bool = Field(..., title="API 성공 여부", example=True)
    error: Optional[str] = Field(None, title="API 에러 내용", example="Fail to do API!")
    
    class config:
        orm_mode = True