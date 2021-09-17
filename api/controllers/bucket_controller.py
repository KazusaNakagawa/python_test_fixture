from config import const
from api.models import bucket


def s3_bucket_management():
    """ aws s3 management """
    management_bucket = bucket.Bucket(client=const.CLIENT, bucket_name=const.BUCKET_NAME, region=const.TOKYO_REGION)

    # TODO: 指定 Directory のファイルを格納する
    data_list = ['user.sql', 'user.json']

    if const.BUCKET_CREATE:
        management_bucket.create_bucket()

    if const.UPLOAD:
        for data in data_list:
            management_bucket.upload_data(bucket_name=const.BUCKET_NAME, upload_data=f"data/{data}")

    if const.DOWNLOAD:
        for data in data_list:
            management_bucket.download_data(download_data=data)

    if const.DELETE:
        for data in data_list:
            management_bucket.delete_data(bucket_name=const.BUCKET_NAME, delete_data=f"data/{data}")

    if const.BUCKET_DELETE:
        management_bucket.delete_all_buckets()

    # 最終的に存在している Bucketを確認する
    management_bucket.print_bucket_name()
