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

    def buy_stock(self) -> None:
        pass

    def sell_stock(self) -> None:
        pass

    def update_stocks(self) -> None:
        pass

    def open_portfolio(self, portfolio_name):
        if self.table_exists(self.cursor, portfolio_name):
            print(f"Accessing portfolio '{portfolio_name}'.")
            try:
                table_query = f"""
                SELECT * FROM {portfolio_name};
                """
                self.cursor.execute(table_query)

                #TODO: update prices here.
                print(self.cursor.fetchall())
            except mysql.connector.Error as err:
                print(f"Error creating Portfolio '{portfolio_name}': {err}")
        else:
            print(f"The portfolio '{portfolio_name}' does not exist. Creating new portfolio.")
            try:
                #TODO: create a dummy stock here that controls your total money
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {portfolio_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    column1 VARCHAR(255),
                    column2 INT
                )
                """
                self.cursor.execute(create_table_query)
                print(f"Portfolio '{portfolio_name}' has been created.")
            except mysql.connector.Error as err:
                print(f"Error creating Portfolio '{portfolio_name}': {err}")
        

    # Add other methods to interact with your database here

if __name__ == "__main__":
    host = input("Enter MySQL host: ")
    user = input("Enter MySQL user: ")
    password = getpass.getpass("Enter your password: ")
    database = input("Enter MySQL database: ")
    funds = input("Enter Funds:")

    portfolio = Portfolio(
        host=host,
        user=user,
        password=password,
        database=database,
        funds=funds
    )

    # Perform database operations here
    portfolio.open_portfolio("Tech")
    portfolio.close_connection()

