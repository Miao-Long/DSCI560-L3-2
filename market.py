import mysql.connector
import getpass
import yfinance as yf
import datetime

# Get the current date

class Portfolio:
    def __init__(self, host, user, password, database, funds) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = self.connect_to_database()
        self.start_date = datetime.date.today()
        self.funds = funds

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
            self.fetch_totals([])
            print(f"Sold {quantity} shares of {symbol} for .")
        except mysql.connector.Error as err:
            print(f"(3e) Error selling {symbol}: {err}")

    def fetch_totals(self, tickers) -> dict:
        prices = {}  # Create an empty dictionary to store prices
        for pack in tickers:
            try:
                # Create a Ticker object for the symbol
                symbol, quantity = pack[0], pack[1]
                company_info = yf.Ticker(symbol)
                
                # Get the current stock price
                current_price = company_info.history(period="1d")["Close"].iloc[0]
                
                # Add the price to the dictionary with the symbol as the key
                prices[symbol] = (current_price, current_price * quantity)
            except Exception as e:
                print(f"Error fetching price for {symbol}: {e}")
        return prices

    def open_portfolio(self):
        self.cursor.execute(self.table_query)
        try:
            print("(2) Fetching portfolio")
            self.cursor.execute(self.select_query)
            portfolio_data = self.cursor.fetchall()
            total_prices = self.fetch_totals([x for x in portfolio_data])
            portfolio_total = 0
            for symbol, prices in total_prices.items():
                print(f"Stock Symbol: {symbol}    PPU: ${prices[0]:.2f}    Total Price: ${prices[1]:.2f}\n")
                portfolio_total += prices[1]
            print(f"Portfolio Total: ${portfolio_total:.2f}")
        except mysql.connector.Error as err:
            print(f"(1e) Error fetching portfolio : {err}")
    
    def get_metrics(self) -> None:
        self.cursor.execute(self.select_query)
        portfolio_data = self.cursor.fetchall()
        total_prices = self.fetch_totals([x for x in portfolio_data])
        portfolio_total = 0


        # Calculate the elapsed time in years
        end_date = datetime.date.today()
        elapsed_years = (end_date - self.start_date).days / 365.0  # Assuming a 365-day year

        # Calculate the annualized returns
        annualized_returns = ((portfolio_total / self.funds) ** (1 / elapsed_years)) - 1


        for symbol, prices in total_prices.items():
            portfolio_total += prices[1]
        print(f"""
            Portfolio Total: ${portfolio_total:.2f} 
            ROI: {portfolio_total/self.funds*100:.2f}%
            Annualized Returns {annualized_returns * 100:.2f}%
            """)
        return portfolio_total

if __name__ == "__main__":
    host = "localhost"
    user = "root"
    password = getpass.getpass("Enter your password: ")
    database="dsci560_lab3"
    funds=100000

    portfolio = Portfolio(
        host=host,
        user=user,
        password=password,
        database=database,
        funds=funds
    )

    # Perform database operations here
    portfolio.open_portfolio()
    portfolio.buy_stock("META", 500)
    portfolio.buy_stock("TSLA", 500)
    portfolio.buy_stock("GOOGL", 1000)
    portfolio.sell_stock("GOOGL", 1000)
    portfolio.get_metrics()
    portfolio.close_connection()

