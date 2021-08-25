import pathlib

from api.models import db

DB_NAME = 'user'
TABLE_NAME = 'user'
INSERT_RECODE_NUM = 10


def main():
    print('start ...')

    p_file = pathlib.Path('db')

    db1 = db.DB(db_name=f"{p_file}/{DB_NAME}.db", table_name=TABLE_NAME)

    con = db1.connect_db()

    db1.create_table(con, 'name', 'age', 'email')
    db1.query_insert('test_name', '0', 'sample@com', con=con, insert_num=INSERT_RECODE_NUM)

    db1.query_write_file(con=con, file_name=f"data/{DB_NAME}.sql")
    # db1.query_drop_(con)

    db1.close_connect(con)

    print('done')


if __name__ == '__main__':
    main()
