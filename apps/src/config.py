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
    BASE_DIR=BASE_DIR
    ACCESS_TOKEN_KEY=JsonConfig.get_data("ACCESS_TOKEN_KEY")
    REFRESH_TOKEN_KEY=JsonConfig.get_data("REFRESH_TOKEN_KEY")
    JWT_ALGORITHM=JsonConfig.get_data("JWT_ALGORITHM")