from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import Field
from sqlalchemy.orm import Session

from src.common.response import verify_token, error
from src.sql.database import get_db
from src.routes.apis.v1.auth.schemas import UserOut
from src.sql.models import User
from src.service.user import UserService

rt = APIRouter(prefix='/apis/v1/user', tags=['/apis/v1/user'])

@rt.get('/{user_id}/book')
def user_books(db: Session = Depends(get_db), user_id: int = Field(...)):
    user = UserService.get_user_by_id(db, user_id)
    books = []
    for scrapbook in user.scrapbooks:
        books.append(scrapbook.book)
    return JSONResponse(content={"books": books})

@rt.get('/me', description='로그인한 유저 정보 API', response_model=UserOut)
def me(user: User = Depends(verify_token)):
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error(40100))
    json_user = jsonable_encoder(user)
    return json_user