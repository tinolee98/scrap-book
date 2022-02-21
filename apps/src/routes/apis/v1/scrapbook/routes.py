from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.service.scrapbooks import ScrapbookService
from src.sql.models import User
from src.sql.database import get_db
from src.common.response import verify_token

rt = APIRouter(prefix='/apis/v1/scrapbook', tags=['/apis/v1/scrapbook'])

@rt.get('s/')
def get_scrapbooks(db: Session = Depends(get_db), user: User = Depends(verify_token)):
    scrapbooks = ScrapbookService.get_scrapbooks(db, user.id)
    res = JSONResponse(content={"scrapbooks": scrapbooks})
    return res