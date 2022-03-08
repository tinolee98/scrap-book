from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.common.response import error
from src.service.book import BookService
from src.service.scrapbooks import ScrapbookService
from src.sql.models import User, Scrapbook, ScrapbookStar
from src.sql.database import get_db
from src.common.response import verify_token
from src.routes.apis.v1.book.schemas import BookIn

rt = APIRouter(prefix='/apis/v1/scrapbook', tags=['/apis/v1/scrapbook'])

@rt.get('s', description='스크랩북 목록 읽기 API')
def get_scrapbooks(limit: int, offset: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    scrapbooks = ScrapbookService.get_scrapbooks(db, user.id, limit, offset)
    scrapbooks = jsonable_encoder(scrapbooks)
    res = JSONResponse(content={"scrapbooks": scrapbooks})
    return res

# uuid 기반으로 스크랩북에 참가하는 경우는 어떻게 할까.
@rt.post('', description='스크랩북 생성 API', status_code=status.HTTP_201_CREATED)
def create_scrapbook(book: BookIn = Body(...), db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_book = BookService.existed_book(db, book.authors, book.title)
    if not db_book:
        db_book = BookService.create_book(db, book)
    if ScrapbookService.scrapbook_already_exists(db, user.id, db_book.id):
        return JSONResponse(content={"error": "already scrapbook existed", "ok": False}, status_code=status.HTTP_200_OK)
    ok = ScrapbookService.create_scrapbook(db, user, db_book.id)
    if ok:
        return {"ok": True}
    return {"ok": False}

@rt.get('/{scrapbook_id}')
def get_scraps_in_scrapbook(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    for scrapbook_user in db_scrapbook.users:
        if user.id == scrapbook_user.id:
            res = JSONResponse(content=jsonable_encoder(db_scrapbook))
            return res

@rt.delete('/{scrapbook_id}', description='스크랩북 삭제 API')
def delete_scrapbook(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    if not user not in db_scrapbook.users:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=error(40300))
    ScrapbookService.delete_scrapbook(db, db_scrapbook)
    return {"ok": True}

@rt.post('/{scrapbook_id}/star', description='스크랩북 즐겨찾기 생성 API')
def create_scrapbook_star(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    if user not in db_scrapbook.users:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=error(40300))
    if db_scrapbook.star:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': False, 'error': "이미 즐겨찾기가 되어있습니다."})
    ok = ScrapbookService.create_star(db, scrapbook_id, user.id)
    if ok:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'ok': ok})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': ok, 'error': '즐겨찾기 생성을 실패했습니다.'})

@rt.delete('/{scrapbook_id}/star', description='스크랩북 즐겨찾기 삭제 API')
def delete_scrapbook_star(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    if user not in db_scrapbook.users:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=error(40300))
    if not db_scrapbook.star:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': False, 'error': "이미 즐겨찾기가 없습니다."})
    ok = ScrapbookService.delete_star(db, scrapbook_id, user.id)
    if ok:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'ok': ok})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': ok, 'error': '즐겨찾기 삭제를 실패했습니다.'})