from api.models import db


class Sales(object):
    """ SQL操作を確かめるために作成
    ref)
    https://docs.snowflake.com/ja/sql-reference/constructs/group-by.html#examples
    """

    def __init__(self, product_id='product_id', retail_price='retail_price', quantity='quantity', city='city',
                 state='state'):
        self.product_id = product_id
        self.retail_price = retail_price
        self.quantity = quantity
        self.city = city
        self.state = state
        # TODO: DB model を読み込んでいるが実装しにくい。。。
        self.db = db.DB(db_name='../../db/sales.db', table_name='sales')

    def connect_cursor(self):
        con = self.db.connect_db()
        cur = con.cursor()

        return con, cur

    def create_table(self) -> None:
        """
        EX)
        https://docs.snowflake.com/ja/sql-reference/constructs/group-by.html#examples
        """
        con, cur = self.connect_cursor()

        cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.db.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {self.product_id} int,
                    {self.retail_price} real,
                    {self.quantity} int,
                    {self.city} varchar,
                    {self.state} varchar
                    )'''
                    )

    def query_insert(self):
        con, cur = self.connect_cursor()

        cur.execute(
            f'''INSERT INTO {self.db.table_name} (product_id, retail_price, quantity, city, state) VALUES
                 (1, 2.00,  1, 'SF', 'CA'),
                 (1, 2.00,  2, 'SJ', 'CA'),
                 (2, 5.00,  4, 'SF', 'CA'),
                 (2, 5.00,  8, 'SJ', 'CA'),
                 (2, 5.00, 16, 'Miami', 'FL'),
                 (2, 5.00, 32, 'Orlando', 'FL'),
                 (2, 5.00, 64, 'SJ', 'PR')
            '''
        )
        con.commit()

    def query_select_product_id(self):
        con, cur = self.connect_cursor()

        query = \
            f'''
        SELECT product_id, sum(retail_price * quantity) AS gross_revenue
        from {self.db.table_name}
        GROUP BY product_id;'''

        self.print_format(query)
        print('(PRODUCT_ID, PROFIT)')

        for row in cur.execute(query):
            print(row)

    def query_select_group_by_multiple(self, col1: str, col2: str):
        con, cur = self.connect_cursor()

        query = \
            f'''
        select {col1}, {col2}, sum(retail_price * quantity) as gross_revenue
        from {self.db.table_name}
        group by state, city;'''

        print('(STATE, CITY, GROSS REVENUE )')
        self.print_format(query)
        for row in cur.execute(query):
            print(row)

    @staticmethod
    def print_format(query):
        print('-' * 20, query, '\n', '=' * 20)


if __name__ == '__main__':
    # TODO: DB反映する判定が機能していない
    MEMORY = 0

    sales = Sales()
    if MEMORY:
        con = sales.db.connect_db_ram()
    if not MEMORY:
        con = sales.db.connect_db()

    # table create & insert
    sales.create_table()
    sales.query_insert()

    # query select
    # sales.db.query_select_order_by(con)
    sales.query_select_product_id()
    sales.query_select_group_by_multiple(col1='state', col2='city')

    # sales.db.query_drop_(con)
    sales.db.close_connect(con)
