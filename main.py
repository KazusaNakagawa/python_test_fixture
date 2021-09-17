import api.controllers.bucket_controller
import pathlib

from api.models import db
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


if __name__ == '__main__':
    api.controllers.bucket_controller.s3_bucket_management()
