from fastapi import FastAPI
from .sql.models import Base
from .sql.database import engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

from .routes.v1 import main_routes, auth_routes
app.include_router(main_routes.rt)
app.include_router(auth_routes.rt)

path = "/Users/kunolee_98/Project/scrap-book/fastapi/src"
