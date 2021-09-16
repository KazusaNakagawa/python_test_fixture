import pathlib

from api.models import db
from api.models.bucket import Bucket
from config import const


def db_main():
    print('start ...')

    p_file = pathlib.Path('db')

    db1 = db.DB(db_name=f"{p_file}/{const.DB_NAME}.db", table_name=const.TABLE_NAME)

    con = db1.connect_db()

    db1.create_table('name', 'age', 'email', con=con)
    db1.query_insert('test_name', '0', 'sample@com', con=con, insert_num=const.INSERT_RECODE_NUM)

    db1.query_write_file(con=con, file_name=f"data/{const.DB_NAME}.sql")
    # db1.query_drop_(con)

    db1.close_connect(con)

    print('done')


def bucket_main():
    data_list = ['user.sql', 'user.json']

    # create instance
    bucket1 = Bucket(client=const.CLIENT, bucket_name=const.BUCKET_NAME, region=const.TOKYO_REGION)
    bucket2 = Bucket(client=const.CLIENT, bucket_name='testbucket-0912', region=const.TOKYO_REGION)

    if const.BUCKET_CREATE:
        bucket1.create_bucket()
        # bucket2.create_bucket()

    if const.UPLOAD:
        for data in data_list:
            bucket1.upload_data(bucket_name=const.BUCKET_NAME, upload_data=data)

    if const.DOWNLOAD:
        for data in data_list:
            bucket1.download_data(download_data=data)

    if const.DELETE:
        for data in data_list:
            bucket1.delete_data(bucket_name=const.BUCKET_NAME, delete_data=f"data/{data}")

    if const.BUCKET_DELETE:
        bucket1.delete_all_buckets()


def main():
    # db_main()
    bucket_main()


if __name__ == '__main__':
    main()
