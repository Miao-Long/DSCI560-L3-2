import mysql.connector
import getpass
import yfinance

class Portfolio:
    def __init__(self, host, user, password, database, funds) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.funds = funds
        self.cursor = self.connect_to_database()

        self.select_query = """SELECT * FROM portfolio;"""
        self.table_query = """
            CREATE TABLE IF NOT EXISTS portfolio (
                stk_symbol VARCHAR(10) PRIMARY KEY,
                stk_owned INT
            );
        """


    def table_exists(self, cursor, table_name):
        try:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def connect_to_database(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
            return self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            print("Connection closed")

    def table_exists(self, cursor, table_name):
        try:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            result = cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def buy_stock(self, symbol, quantity) -> None:
        try:
            buy_query = """
                INSERT INTO portfolio
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE stk_owned = stk_owned + %s;
            """
            values = (symbol, quantity, quantity)
            self.cursor.execute(buy_query, values)
            self.connection.commit()
            print(f"Bought {quantity} shares of {symbol}.")
        except mysql.connector.Error as err:
            print(f"(3e) Error buying {symbol}: {err}")

    def sell_stock(self, symbol, quantity) -> None:
        try:
            sell_query = """
                UPDATE portfolio
                SET stk_owned = CASE
                    WHEN stk_symbol = %s AND stk_owned >= %s THEN stk_owned - %s
                    ELSE stk_owned
                END;
            """
            values = (symbol, quantity, quantity)
            self.cursor.execute(sell_query, values)
            self.connection.commit()
            print(f"Sold {quantity} shares of {symbol}.")
        except mysql.connector.Error as err:
            print(f"(3e) Error selling {symbol}: {err}")


    def fetch_prices(self) -> None:
        self.cursor.execute(self.select_query)
        result = self.cursor.fetchall()
        print(result)

    def open_portfolio(self):
        try:
            print("(1) Creating portfolio table")
            self.cursor.execute(self.table_query)
        except mysql.connector.Error as err:
            print(f"(1e) Error creating Portfolio: {err}")

        try:
            print("(2) Fetching portfolio")
            self.cursor.execute(self.select_query)
            print(self.cursor.fetchall())
        except mysql.connector.Error as err:
            print(f"(1e) Error fetching portfolio : {err}")

        
        #     print(f"Accessing portfolio '{portfolio_name}'.")
        #     try:
        #         table_query = f"""
        #         SELECT * FROM {portfolio_name};
        #         """
        #         self.cursor.execute(table_query)

        #         #TODO: update prices here.
        #         print(self.cursor.fetchall())
        #     except mysql.connector.Error as err:
        #         
        # else:
        #     print(f"The portfolio '{portfolio_name}' does not exist. Creating new portfolio.")
        #     try:
        #         #TODO: create a dummy stock here that controls your total money
        #         create_table_query = f"""
        #         CREATE TABLE IF NOT EXISTS {portfolio_name} (
        #             id INT AUTO_INCREMENT PRIMARY KEY,
        #             column1 VARCHAR(255),
        #             column2 INT
        #         )
        #         """
        #         self.cursor.execute(create_table_query)
        #         print(f"Portfolio '{portfolio_name}' has been created.")
        #     except mysql.connector.Error as err:
        #         print(f"Error creating Portfolio '{portfolio_name}': {err}")
        

    # Add other methods to interact with your database here

if __name__ == "__main__":
    # host = input("Enter MySQL host: ")
    # user = input("Enter MySQL user: ")
    # password = getpass.getpass("Enter your password: ")
    # database = input("Enter MySQL database: ")
    # funds = input("Enter Funds:")

    host = "localhost"
    user = "root"
    password = getpass.getpass("Enter your password: ")
    database="dsci560_lab3"
    funds=1000

    portfolio = Portfolio(
        host=host,
        user=user,
        password=password,
        database=database,
        funds=funds
    )

    # Perform database operations here
    portfolio.open_portfolio()
    portfolio.buy_stock("GOOGL", 1000)
    portfolio.buy_stock("GOOGL", 1000)
    portfolio.sell_stock("GOOGL", 1000)
    portfolio.fetch_prices()

    portfolio.close_connection()

