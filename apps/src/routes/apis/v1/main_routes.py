from fastapi import APIRouter

rt = APIRouter()

@rt.get('/', description="스크랩북 API")
def Scrapbook():
    return {"hello": "scrapbook"}