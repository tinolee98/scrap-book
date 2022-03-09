from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, status, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.common.errors import error
from src.common.response import verify_token
from src.common.schema import OkError
from src.service.scrap import ScrapService
from src.service.scrapbooks import ScrapbookService
from src.sql.database import get_db
from src.sql.models import User
from src.routes.apis.v1.scrap.schemas import ResScrap, ResScraps
from src.common.s3 import S3FileUploader

rt = APIRouter(prefix='/apis/v1/scrapbook', tags=['/apis/v1/scrapbook'])
  

@rt.post('/{scrapbook_id}/scrap', description='스크랩 생성 API', response_model=OkError)
async def create_scrap(scrapbook_id: int, picture: UploadFile = Body(...), scrap: ResScrap = Body(...), user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, '스크랩북이 존재하지 않습니다.'))
    file_uploader = S3FileUploader(picture)
    picture_url = file_uploader.upload()
    if ScrapService.create_scrap(db, user.id, scrapbook_id, scrap.text, scrap.page, picture_url):
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'ok': True})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': False, 'error': '스크랩 생성에 실패하였습니다.'})


@rt.delete('/{scrapbook_id}/scrap/{scrap_id}', description='스크랩 삭제 API', response_model=OkError)
def delete_scrap(scrapbook_id: int, scrap_id: int, user: User = Depends(verify_token), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=error(40100))
    db_scrapbook = ScrapbookService.get_scrapbook_by_id(db, scrapbook_id, user.id)
    if not db_scrapbook:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=error(40400, '스크랩북이 존재하지 않습니다.'))
    if user not in db_scrapbook.users:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=error(40300))
    if ScrapService.delete_scrap(db, scrap_id):
        return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': True})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'ok': False, 'error': '스크랩 삭제에 실패하였습니다.'})
    

@rt.put('/{scrapbook_id}/scrap', description='스크랩 수정 API', response_model=OkError)
def update_scrap(scrapbook_id: int, picture: Optional[UploadFile] = Body(None)):
    pass