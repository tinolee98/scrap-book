import os

BASE_DIR = os.path.dirname(__file__)

# local db를 사용하여 테스트할 땐 sqlite, 실제로는 aws rds postgresql 서버를 이용하자
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, 'scrap.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
