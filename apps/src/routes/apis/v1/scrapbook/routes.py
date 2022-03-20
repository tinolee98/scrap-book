from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import asc
from sqlalchemy.orm import Session

from src.common.schema import OkError
from src.common.response import error, verify_token
from src.service.book import BookService
from src.service.scrapbooks import ScrapbookService
from src.sql.models import User, Scrapbook, ScrapbookStar, Scrap
from src.sql.database import get_db
from src.routes.apis.v1.scrap.schemas import ResScraps
from src.routes.apis.v1.scrapbook.schemas import ResScrapbooks, ResScrapbook, ResUUID, UUIDIn
from src.routes.apis.v1.book.schemas import BookIn

rt = APIRouter(prefix='/apis/v1/scrapbook', tags=['/apis/v1/scrapbook'])

@rt.get('s', description='스크랩북 목록 읽기 API', response_model=ResScrapbooks)
def get_scrapbooks(limit: int, offset: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    scrapbooks = ScrapbookService.get_scrapbooks(db, user.id, limit, offset)
    scrapbooks = jsonable_encoder(scrapbooks)
    res = JSONResponse(content={"scrapbooks": scrapbooks})
    return res

@rt.post('', description='스크랩북 생성 API', response_model=OkError ,status_code=status.HTTP_201_CREATED)
def create_scrapbook(book: BookIn = Body(...), db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_book = BookService.existed_book(db, book.authors, book.title)
    # 어떤 것들을 비교해야 동일한 책이라는 것을 알 수 있을까? 모든 것을 비교하는 것은 비효율적인 것 같아서.
    if not db_book:
        db_book = BookService.create_book(db, book)
    if not db_book:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, '책 정보를 불러오는데 실패했습니다.'))
    if ScrapbookService.scrapbook_already_exists(user, db_book.id):
        return JSONResponse(content={"ok": False, "error": "스크랩북이 이미 존재합니다."}, status_code=status.HTTP_200_OK)
    db_scrapbook = ScrapbookService.create_scrapbook(db, user, db_book.id)
    if db_scrapbook:
        if ScrapbookService.join_scrapbook(db, user.id, db_scrapbook):
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"ok": True})
        ScrapbookService.delete_scrapbook(db, db_scrapbook)
    return JSONResponse(status_code=status.HTTP_200_OK,content={"ok": False, 'error': '스크랩북 생성에 실패하였습니다.'})

@rt.get('/{scrapbook_id}', description='id 기반 스크랩북 읽기 API', response_model=ResScraps)
def get_scraps_in_scrapbook(limit: int, offset: int, scrapbook_id: int, user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, '스크랩북이 존재하지 않습니다.'))
    scraps = jsonable_encoder(db_scrapbook.scraps.order_by(asc(Scrap.page)).limit(limit).offset(offset).all())
    return JSONResponse(status_code=status.HTTP_200_OK, content={'scraps': scraps})

@rt.delete('/{scrapbook_id}', description='스크랩북 삭제 API', response_model=OkError)
def delete_scrapbook(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    if user not in db_scrapbook.users:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=error(40300))
    if ScrapbookService.go_out_scrapbook(db, user, db_scrapbook):
        return {"ok": True}
    return {"ok": False, "error": "스크랩북 삭제 실패"}

@rt.post('/join', description='스크랩북 참가 API', response_model=OkError)
def join_scrapbook(uuidIn: UUIDIn = Body(...), db: Session = Depends(get_db), user: User = Depends(verify_token)):
    uuid = uuidIn.uuid
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_uuid(db, uuid)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    if user in db_scrapbook.users:
        return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': False, 'error': '이미 스크랩북에 들어가있습니다.'})
    if ScrapbookService.join_scrapbook(db, user, db_scrapbook):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'ok': True})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': False, 'error': '스크랩북 참가에 실패하였습니다.'})
    
@rt.get('/{scrapbook_id}/uuid', description='스크랩북 uuid 읽기 API', response_model=ResUUID)
def get_scrapbook_uuid(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    return JSONResponse(status_code=status.HTTP_200_OK, content={'uuid': db_scrapbook.uuid})

@rt.put('/{scrapbook_id}/star', description='스크랩북 즐겨찾기 토글 API', response_model=OkError)
def toggle_scrapbook_star(scrapbook_id: int, db: Session = Depends(get_db), user: User = Depends(verify_token)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, "스크랩북이 존재하지 않습니다."))
    if user not in db_scrapbook.users:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=error(40300))
    if ScrapbookService.is_starred(db, scrapbook_id, user.id):
        ok = ScrapbookService.off_star(db, scrapbook_id, user.id)
    else:
        ok = ScrapbookService.on_star(db, scrapbook_id, user.id)
    if ok:
        return {'ok': True}
    return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': False, 'error': '즐겨찾기 토글에 실패하였습니다.'})

# @TODO: Leagcy - Toggle 형태로 바꿀 수 있는 PUT API로 수정
@rt.post('/{scrapbook_id}/star', description='스크랩북 즐겨찾기 생성 API', response_model=OkError)
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

@rt.delete('/{scrapbook_id}/star', description='스크랩북 즐겨찾기 삭제 API', response_model=OkError)
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

# 아직 scrapbook_star가 없는 모든 스크랩북에 is_starred = False를 설정해주기 위한 API
@rt.post('/makeAllStar')
def make_all_star_false(db: Session = Depends(get_db)):
    scrapbooks = db.query(Scrapbook).all()
    for scrapbook in scrapbooks:
        users = scrapbook.users
        for user in users:
            star = db.query(ScrapbookStar).filter(ScrapbookStar.scrapbookId == scrapbook.id).filter(ScrapbookStar.userId == user.id).first()
            if not star:
                new_star = ScrapbookStar(scrapbookId=scrapbook.id, userId=user.id)
                db.add(new_star)
                db.commit()