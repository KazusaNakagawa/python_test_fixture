import sqlite3


class DB(object):

    def __init__(self, db_name: str, table_name: str):
        self.db_name = db_name
        self.table_name = table_name

    def connect_db(self):
        return sqlite3.connect(self.db_name)

    def close_connect(self, con):
        con.close()

    def create_table(self, con) -> None:
        cur = con.cursor()

        try:
            cur.execute(f'''CREATE TABLE {self.table_name}
                       (id PRIMARY KEY, date text, trans text, symbol text, qty real, price real)''')
        except sqlite3.OperationalError as ex:
            print(ex)

    def insert_user(self, con, insert_num=460):
        cur = con.cursor()

        # Insert a row of data
        for i in range(1, insert_num + 1):
            cur.execute(f"INSERT INTO {self.table_name} VALUES ('{i}','2006-01-05','BUY_{i}','RHAT',100,35.14)")

        # Save (commit) the changes
        con.commit()

    def query(self, con):
        cur = con.cursor()
        for row in cur.execute(f"SELECT * FROM {self.table_name} ORDER BY price"):
            print(row)

    def query_write_file(self, con, file_name='test.text'):
        cur = con.cursor()
        with open(file_name, 'w', encoding='utf-8') as f:
            for row in cur.execute(f'SELECT * FROM {self.table_name} ORDER BY price'):
                write_str = f"INSERT INTO {self.table_name} VALUES {row};\n"
                f.write(write_str)


if __name__ == '__main__':
    DB_NAME = 'test4'

    db1 = DB(db_name=f"../../db/{DB_NAME}.db", table_name='stocks')

    con = db1.connect_db()
    db1.create_table(con)
    db1.insert_user(con, insert_num=460000)

    db1.query_write_file(con=con, file_name=f"../../data/{DB_NAME}.sql")
    db1.close_connect(con)
