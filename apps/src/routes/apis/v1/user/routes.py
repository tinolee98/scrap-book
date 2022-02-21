from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import Field
from sqlalchemy.orm import Session

from src.sql.database import get_db
from src.service.user import UserService

rt = APIRouter(prefix='/apis/v1/user', tags=['/apis/v1/user'])

@rt.get('/{user_id}/book')
def user_books(db: Session = Depends(get_db), user_id: int = Field(...)):
    user = UserService.get_user_by_id(db, user_id)
    books = []
    for scrapbook in user.scrapbooks:
        books.append(scrapbook.book)
    return JSONResponse(content={"books": books})
