import boto3

from botocore.exceptions import ClientError

from api.models import logger_tool
from config import const


class Bucket(object):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html
    """

    def __init__(self, client: str, bucket_name: str, region: str):
        """

        params
        ------
        client(str): s3
        bucket_name(str): choice bucket name
        region(str): Region code
        """
        self.client = boto3.client(client)
        self.resource_bucket = boto3.resource(client)
        self.bucket_name = bucket_name
        self.region = region

    def is_bucket_check(self, bucket_name: str, max_key: int):
        """
        作成するbucket が既に存在するかチェックする


        :return:
            bucketがある時はbucketを作成しない
        """
        # TODO:【暫定】例外でbucket有無の切り分ける方法は避けたい
        # ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects
        try:
            response = self.client.list_objects_v2(
                Bucket=bucket_name,
                MaxKeys=max_key,
            )
            return True

        except ClientError as ex:
            logger_tool.error(
                action='bucket check',
                status='error',
                bucket_name=bucket_name,
                ex=ex
            )
            return False

    def create_bucket(self):
        """
        https://github.com/aws/aws-cli/issues/2603#issuecomment-349191935
        """

        logger_tool.info(
            action='create',
            status='run',
            bucket_name=self.bucket_name
        )

        if not self.is_bucket_check(self.bucket_name, 2):
            self.client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )
            logger_tool.info(
                action='create',
                status=200,
                bucket_name=self.bucket_name
            )

    def upload_data(self, bucket_name: str, upload_data: str):
        """
        params
        ------
        upload_data: ex) sample.png
        """
        key = upload_data.split('/')[-1]

        logger_tool.info(
            action='upload',
            status='run',
            bucket_name=bucket_name,
            data=key,
        )

        with open(upload_data, 'rb') as upload_data_file:
            self.resource_bucket.Bucket(bucket_name).put_object(Key=key, Body=upload_data_file)

        logger_tool.info(
            action='upload',
            status=200,
            bucket_name=bucket_name,
            data=key,
        )

    def down_load_data(self):
        """
        Bucket にあるファイルをダウンロードする
        """

    def delete_data(self, bucket_name: str, delete_data: str):
        """
        bucketにあるデータを削除
        """

        key = delete_data.split('/')[-1]

        logger_tool.info(
            action='delete',
            status='run',
            bucket_name=bucket_name,
            data=key,
        )
        try:
            response = self.client.delete_object(
                Bucket=bucket_name,
                Key=key,
            )
            return response

        except ClientError as ex:
            logger_tool.error(
                action='delete data',
                status=404,
                bucket_name=bucket_name,
                ex=ex
            )

        logger_tool.info(
            action='delete',
            status=204,
            bucket_name=bucket_name,
            data=key,
        )

    def print_bucket_name(self):
        """
        is select buckets
        """

        for bucket in self.resource_bucket.Buckets.all():
            print(bucket.name)

    def delete_all_buckets(self):
        """
        全ての bucketを削除する
        """
        buckets = list(self.resource_bucket.buckets.all())

        if buckets:
            logger_tool.info(
                action='delete',
                status='run',
                bucket_name=self.bucket_name
            )

            response = [key.delete() for key in self.resource_bucket.buckets.all()]

            logger_tool.info(
                action='delete',
                status=204,
                bucket_name=self.bucket_name
            )
            return response


if __name__ == '__main__':
    data_list = ['../../data/user.sql', '../../data/user.json']

    # create instance
    bucket1 = Bucket(client=const.CLIENT, bucket_name=const.BUCKET_NAME, region=const.TOKYO_REGION)
    bucket2 = Bucket(client=const.CLIENT, bucket_name='testbucket-0912', region=const.TOKYO_REGION)

    if const.BUCKET_CREATE:
        bucket1.create_bucket()
        # bucket2.create_bucket()

    if const.UPLOAD:
        for data in data_list:
            bucket1.upload_data(bucket_name=const.BUCKET_NAME, upload_data=data)

    if const.DELETE:
        for data in data_list:
            bucket1.delete_data(bucket_name=const.BUCKET_NAME, delete_data=data)

    if const.BUCKET_DELETE:
        bucket1.delete_all_buckets()
