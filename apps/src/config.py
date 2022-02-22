import os
import json

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

class JsonConfig:
    Data = json.loads(open("{}/config.json".format(BASE_DIR)).read())

    @staticmethod
    def get_data(varname, value=None):
        result = JsonConfig.Data.get(varname) or os.getenv(varname) or value
        if result == "true":
            return True
        elif result == "false":
            return False
        return result

class Config:
    ERROR_CODE = {
        40000: '입력 값이 잘못되었습니다.',
        40100: '유효하지 않은 토큰입니다.',
        40300: '권한이 없습니다.',
        40400: '찾을 수 없습니다.',
        50000: '서버 에러.',
    }

    BASE_DIR=BASE_DIR
    ACCESS_TOKEN_KEY=JsonConfig.get_data("ACCESS_TOKEN_KEY")
    REFRESH_TOKEN_KEY=JsonConfig.get_data("REFRESH_TOKEN_KEY")
    JWT_ALGORITHM=JsonConfig.get_data("JWT_ALGORITHM")
    KAKAO_BOOK_SEARCH_API_KEY=JsonConfig.get_data("KAKAO_BOOK_SEARCH_API_KEY")
    KAKAO_BOOK_SEARCH_URL=JsonConfig.get_data("KAKAO_BOOK_SEARCH_URL")