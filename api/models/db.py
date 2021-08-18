import logging
import sqlite3


class DB(object):
    """　DB 操作を """

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

    def create_table(self, con) -> None:
        cur = con.cursor()

        cur.execute(f'''CREATE TABLE {self.table_name}
                   (id PRIMARY KEY,
                    date text,
                    trans text,
                    symbol text,
                    qty real,
                    price real)'''
                    )

    def query_insert(self, con, insert_num=460):
        cur = con.cursor()

        # Insert a row of data
        for i in range(1, insert_num + 1):
            cur.execute(f"INSERT INTO {self.table_name} VALUES ('{i}','2006-01-05','BUY_{i}','RHAT',100,35.14)")

        con.commit()

    def query_select_order_by(self, con, oder_by_name='id'):
        cur = con.cursor()
        for row in cur.execute(f"SELECT * FROM {self.table_name} ORDER BY {oder_by_name}"):
            print(row)

    def query_write_file(self, con, file_name='test.text'):
        cur = con.cursor()
        with open(file_name, 'w', encoding='utf-8') as f:
            for row in cur.execute(f"SELECT * FROM {self.table_name} ORDER BY price"):
                write_str = f"INSERT INTO {self.table_name} VALUES {row};\n"
                f.write(write_str)

    def query_drop_(self, con):
        cur = con.cursor()
        cur.execute(f"DROP TABLE {self.table_name}")


if __name__ == '__main__':
    DB_NAME = 'test'
    INSERT_RECODE_NUM = 460000

    print('start ...')

    db1 = DB(db_name=f"../../db/{DB_NAME}.db", table_name='stocks')

    # con = db1.connect_db()
    con = db1.connect_db_ram()

    db1.create_table(con)
    db1.query_insert(con, insert_num=INSERT_RECODE_NUM)

    db1.query_write_file(con=con, file_name=f"../../data/{DB_NAME}.sql")
    # db1.query_drop_(con)

    db1.close_connect(con)

    print('done')
