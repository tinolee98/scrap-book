from flask import flash, Blueprint

bp = Blueprint('main', __name__, url_prefix="/")

@bp.route('/')
def hello():
    return 'hello scrap!'