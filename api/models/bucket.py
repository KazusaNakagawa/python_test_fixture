import boto3

from botocore.exceptions import ClientError
from pathlib import Path

from config import const, logger_tool


class Bucket(object):
    """
    AWS S3 Bucket 操作する model
    """

    def __init__(self, client: str, bucket_name: str, region: str):
        """ initialization parameter

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

    def create_bucket(self):
        """ Bucket を作成する処理

        params
        -------
            max_key(int): default: 2
                is_bucket_check fuc args
        """
        logger_tool.info(
            module=__name__,
            action='create',
            status='run',
            bucket_name=self.bucket_name
        )

        try:
            self.client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )

        except self.client.exceptions.BucketAlreadyExists as err:
            logger_tool.error(
                module=__name__,
                action='create',
                status=409,
                bucket_name=self.bucket_name,
                ex=err,
                msg="Bucket {} already exists!".format(err.response['Error']['BucketName']),
            )
            raise err

        except self.client.exceptions.BucketAlreadyOwnedByYou as err:
            logger_tool.error(
                module=__name__,
                action='create',
                status=409,
                bucket_name=self.bucket_name,
                ex=err,
                msg="Bucket {} already Owned By You!".format(err.response['Error']['BucketName']),
            )
            raise err

        logger_tool.info(
            module=__name__,
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
            module=__name__,
            action='upload',
            status='run',
            bucket_name=bucket_name,
            data=key,
        )

        with open(upload_data, 'rb') as upload_data_file:
            self.resource_bucket.Bucket(bucket_name).put_object(Key=key, Body=upload_data_file)

        logger_tool.info(
            module=__name__,
            action='upload',
            status=200,
            bucket_name=bucket_name,
            data=key,
        )

    def download_data(self, download_data: str) -> None:
        """
        Bucket にあるファイルをダウンロードする

        params
        ------
            download_data(str): S3にある指定データを download する
        """
        # download 用に作成
        Path(const.TMP_PATH).mkdir(exist_ok=True)

        logger_tool.info(
            module=__name__,
            action='download',
            status='run',
            bucket_name=self.bucket_name,
            data=download_data,
        )
        try:
            self.resource_bucket.meta.client.download_file(
                self.bucket_name, download_data, f"tmp/{download_data}"
            )
            logger_tool.info(
                module=__name__,
                action='download',
                status=204,
                bucket_name=self.bucket_name,
                data=download_data,
            )
        except ClientError as ex:
            logger_tool.error(
                module=__name__,
                action='download',
                status=404,
                bucket_name=self.bucket_name,
                ex=ex
            )

    def delete_data(self, bucket_name: str, delete_data: str):
        """
        bucketにあるデータを削除

        params
        ------
            bucket_name(str):  Bucket name
            delete_data(data): 削除するファイル名

        return
        ------
            response: 削除が成功した結果を返すレスポンス parameter
        """

        key = delete_data.split('/')[-1]

        logger_tool.info(
            module=__name__,
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
                module=__name__,
                action='delete data',
                status=404,
                bucket_name=bucket_name,
                ex=ex
            )

        logger_tool.info(
            module=__name__,
            action='delete',
            status=204,
            bucket_name=bucket_name,
            data=key,
        )

    def print_bucket_name(self):
        """
        is select buckets
        """
        buckets = [bucket.name for bucket in self.resource_bucket.buckets.all()]

        if not buckets:
            return print('No Buckets')

        if buckets:
            print('Bucket list', buckets)

    def delete_all_buckets(self):
        """
        全ての bucketを削除する

        return
        ------
            response: bucket を削除した結果を返す response parameter
        """

        buckets = list(self.resource_bucket.buckets.all())

        if buckets:
            logger_tool.info(
                module=__name__,
                action='delete',
                status='run',
                bucket_name=self.bucket_name
            )

            response = [key.delete() for key in self.resource_bucket.buckets.all()]

            logger_tool.info(
                module=__name__,
                action='delete',
                status=204,
                bucket_name=self.bucket_name
            )
            return response
