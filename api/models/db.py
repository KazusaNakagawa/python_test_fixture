import logging
import sqlite3


class DB(object):
    """ãDB æä½ã """

    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

    def connect_db_ram(self):
        return sqlite3.connect(":memory:")

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def close_connect(self, con):
        con.cursor()
        con.close()

    def create_table(self, *args, con,) -> None:
        cur = con.cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {args[0]} text,
                    {args[1]} int,
                    {args[2]} text
                    )'''
                    )

    def query_insert(self, *args, con, insert_num: int = 460):
        cur = con.cursor()

        email = args[2].split('@')
        # Insert a row of data
        for i in range(1, insert_num + 1):
            cur.execute(
                f'''INSERT INTO {self.table_name} ( name, age, email ) VALUES (
                '{args[0]}_{i}',
                '{int(args[1]) + i}',
                '{email[0]}_{i}@{email[1]}'
                )'''
            )

        con.commit()

    def query_select_order_by(self, con, oder_by_name='id'):
        cur = con.cursor()
        for row in cur.execute(f"SELECT * FROM {self.table_name} ORDER BY {oder_by_name}"):
            print(row)

    def query_write_file(self, con, file_name='test.text'):
        cur = con.cursor()
        with open(file_name, 'w', encoding='utf-8') as f:
            for row in cur.execute(f"SELECT * FROM {self.table_name} ORDER BY id"):
                write_str = f"INSERT INTO {self.table_name} VALUES {row};\n"
                f.write(write_str)

    def query_drop_(self, con):
        cur = con.cursor()
        cur.execute(f"DROP TABLE {self.table_name}")


if __name__ == '__main__':
    MEMORY = 1

    DB_NAME = 'user'
    TABLE_NAME = 'user'
    INSERT_RECODE_NUM = 460

    print('start ...')

    db1 = DB(db_name=f"../../db/{DB_NAME}.db", table_name=TABLE_NAME)

    if MEMORY:
        con = db1.connect_db_ram()

    if not MEMORY:
        con = db1.connect_db()

    db1.create_table('name', 'age', 'email', con=con)
    db1.query_insert('test_name', '0', 'sample@com', con=con, insert_num=INSERT_RECODE_NUM)

    db1.query_write_file(con=con, file_name=f"../../data/{DB_NAME}.sql")
    # db1.query_drop_(con)

    db1.close_connect(con)

    print('done')
