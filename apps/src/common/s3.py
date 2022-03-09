import os
import time
import boto3
import random

from PIL import Image

from src.config import Config, JsonConfig


class S3FileUploader:
    def __init__(self, file) -> None:
        self.s3 = boto3.client('s3', aws_access_key_id=JsonConfig.get_data('S3_ACCESS_KEY'),
                               aws_secret_access_key=JsonConfig.get_data('S3_SECRET_KEY'), region_name='ap-northeast-2')
        self.bucket = Config.S3_BUCKET_NAME
        self.file = file

    async def upload(self, dir: str = 'scrap', is_checked: bool = True):
        format_list = ['image/png', 'image/jpeg', 'image/gif']
        if is_checked:
            if self.file.content_type not in format_list:
                return None

        path = '{}/img'.format('scraps')
        extension = self.file.filename.split('.')[-1]

        number = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        now = str(time.time()).replace('.', '')
        filename = '{}/{}{}.{}'.format(path, number, now, extension)

        contents = await self.file.read()
        with open(filename, 'wb') as fp:
            fp.write(contents)
        self.s3.upload_file(filename, self.bucket, '{}/{}{}.{}'.format(dir, number, now, extension))
        result = 'https://{}.s3.ap-northeast-2.amazonaws.com/{}/{}{}.{}'.format(self.bucket, dir, number, now, extension)
        return result