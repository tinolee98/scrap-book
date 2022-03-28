# scrap-book

**스크랩북 프로젝트 백엔드 구성**

FastAPI를 활용한 스크랩북 프로젝트입니다.



#### 유의사항

1. 가상환경을 사용해야하므로 가상환경을 설치할 것

```linux
(가장 바깥 directory에서)
python3 -m venv venv
source goVenv.sh
pip install -r requirement.txt
```

2. alembic db migration 시 반드시 src directory에서 실행할 것 (alembic autogenerate도 마찬가지)

```linux
alembic revision --autogenerate -m "커밋 이름"
alembic upgrade head
```
