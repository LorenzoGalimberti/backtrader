import sqlite3
import config
import ccxt

#curser object for database 
connection=sqlite3.connect(config.DB_FILE)
#connection=sqlite3.connect('app.db') vedere se funziona

connection.row_factory=sqlite3.Row
cursor= connection.cursor()

cursor.execute(""" 
 SELECT  symbol , name FROM crypto
""")

rows=cursor.fetchall()
symbols=[row['symbol'] for row in rows]  # built a list of symbols



#CCXT CONNECTION

binance=ccxt.binance()

markets= binance.fetchMarkets()

#table population
for market in markets:
    try:
        if market['active'] is True  and market['symbol'] not in symbols:
            print(f"Added a new crypto {market['symbol']} {market['lowercaseId']}")
            cursor.execute("insert into crypto (symbol,name) values (?,?)",(market['symbol'],market['lowercaseId']))
    except Exception as e:
        print(market['symbol'])
        print(e)
#cursor.execute("insert into stock (symbol,company) values ('ADBE','Adobe Inc.')")
#cursor.execute("insert into stock (symbol,company) values ('VZ','Verizon')")
#cursor.execute("insert into stock (symbol,company) values ('Z','Zillow')")

#cursor.execute("delete from stock")
connection.commit()
