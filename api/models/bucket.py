import boto3

from botocore.exceptions import ClientError

from api.models import logger_tool


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
        data = open(upload_data, 'rb')

        self.resource_bucket.Bucket(bucket_name).put_object(Key=key, Body=data)

    def down_load_data(self):
        """
        Bucket にあるファイルをダウンロードする
        """

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
        全ての bucketを削除する
        """
        buckets = list(self.resource_bucket.buckets.all())

        if buckets:
            logger_tool.info(
                action='delete',
                status='run',
                bucket_name=self.bucket_name
            )

            [key.delete() for key in self.resource_bucket.buckets.all()]

            logger_tool.info(
                action='delete',
                status=204,
                bucket_name=self.bucket_name
            )


if __name__ == '__main__':
    BUCKET_CREATE = 0
    UPLOAD = 0
    BUCKET_DELETE = 1

    CLIENT = 's3'
    BUCKET_NAME = 'testbucket-0911-2'
    TOKYO_REGION = 'ap-northeast-1'

    # create instance
    bucket1 = Bucket(client=CLIENT, bucket_name=BUCKET_NAME, region=TOKYO_REGION)
    bucket2 = Bucket(client=CLIENT, bucket_name='testbucket-0912', region=TOKYO_REGION)

    if BUCKET_CREATE:
        bucket1.create_bucket()
        bucket2.create_bucket()

    if UPLOAD:
        bucket1.upload_data(bucket_name=BUCKET_NAME, upload_data='../../images/*.png')

    if BUCKET_DELETE:
        bucket1.delete_all_buckets()
