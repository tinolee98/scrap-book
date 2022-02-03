from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)   # 프론트와 동시 실행 시 발생할 수 있는 CORS 오류 방지


    from .views import main_views
    app.register_blueprint(main_views.bp)
    return app