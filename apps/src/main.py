from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .sql.models import Base
from .sql.database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

from .routes.apis.v1 import main_routes
from .routes.apis.v1.auth import routes as authRoutes
from .routes.apis.v1.user import routes as userRoutes
from .routes.apis.v1.book import routes as bookRoutes
from .routes.apis.v1.scrapbook import routes as scrapbookRoutes

app.include_router(main_routes.rt)
app.include_router(authRoutes.rt)
app.include_router(userRoutes.rt)
app.include_router(bookRoutes.rt)
app.include_router(scrapbookRoutes.rt)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)

path = "/Users/kunolee_98/Project/scrap-book/fastapi/src"
