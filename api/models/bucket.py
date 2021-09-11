import boto3
import logging

from pathlib import Path

from api.models import time


class Bucket(object):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
    """

    def __init__(self, client: str, bucket_name: str, location: str):
        """

        params
        ------
        client(str): s3
        bucket_name(str): choice bucket name
        location(str): Region code
        """
        self.client = boto3.client(client)
        self.resource_bucket = boto3.resource(client)
        self.bucket_name = bucket_name
        self.location = location

    def create_bucket(self):
        """
        https://github.com/aws/aws-cli/issues/2603#issuecomment-349191935
        """
        # TODO: Bucket existence check

        logger.info({
            'action': 'create',
            'status': 'run',
            'bucket name': self.bucket_name,
            'time': time.datetime_now(),
        })

        self.client.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={'LocationConstraint': self.location}
        )
        logger.info({
            'action': 'create',
            'status': 200,
            'bucket name': self.bucket_name,
            'time': time.datetime_now(),
        })

    def upload_data(self, upload_data: str):
        """
        params
        ------
        upload_data: ex) sample.png
        """

        data = open(upload_data, 'rb')
        self.resource_bucket.Bucket(BUCKET_NAME).put_object(Key=upload_data, Body=data)

    def delete_data(self):
        """
        bucketにあるデータを削除
        """

    def print_bucket_name(self):
        """
        is select buckets
        """

        for bucket in self.resource_bucket.Buckets.all():
            print(bucket.name)

    def delete_all_buckets(self):
        """

        """
        buckets = list(self.resource_bucket.buckets.all())

        if buckets:
            logger.info({
                'action': 'delete',
                'status': 'run',
                'bucket name': self.bucket_name,
                'time': time.datetime_now(),
            })

            [key.delete() for key in self.resource_bucket.buckets.all()]

            logger.info({
                'action': 'delete',
                'status': 204,
                'bucket name': self.bucket_name,
                'time': time.datetime_now(),
            })


if __name__ == '__main__':
    LOGFILE_PATH = '../../log/'
    LOG_FILE = 'bucket.log'

    Path(LOGFILE_PATH).mkdir(exist_ok=True)
    logging.basicConfig(filename=Path(f"{LOGFILE_PATH}{LOG_FILE}"), level=logging.INFO)
    logger = logging.getLogger(__name__)

    CLIENT = 's3'
    BUCKET_NAME = 'testbucket-0911-2'
    TOKYO_REGION = 'ap-northeast-1'

    bucket1 = Bucket(client=CLIENT, bucket_name=BUCKET_NAME, location=TOKYO_REGION)

    bucket1.create_bucket()
    bucket1.delete_all_buckets()
