from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)   # 프론트와 동시 실행 시 발생할 수 있는 CORS 오류 방지
    app.config.from_object(config)

    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):   # sqlite의 경우 오류 방지를 위해서 추가 설정을 해줘야하나 일단 안했음.
        migrate.init_app(app, db)
    else:
        migrate.init_app(app, db)

    from . import models

    from .views import main_views
    app.register_blueprint(main_views.bp)
    return app