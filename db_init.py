import sqlite3
import pandas as pd
from datetime import datetime 



conn = sqlite3.connect('database/safety.db')

cur  = conn.cursor()
# cur.execute("DROP TABLE DELIVERY")
# cur.execute("CREATE TABLE Delivery(Time_Stamp DATETIME ,Date DATE ,TARGET SALE INTEGER,ACTUAL SALE INTEGER, ISSUES TEXT)")
# cur.execute(f"""INSERT INTO DELIVERY VALUES ("{datetime.now()}", "2023-07-23",500,400,'DELIVERY WAS DELAYED DUE TO RAIN')""")
# conn.commit()

# cur.execute("CREATE TABLE SAFETY(TIME_STAMP DATETIME, DATE DATE , EVENT TEXT, LOCATION TEXT ,STATUS TEXT)")
cur.execute(F"""INSERT INTO SAFETY VALUES ("{datetime.now()}", "2023-07-08", "Oil Spilage near machine", "FDM", "CLOSED")""")
df  = pd.read_sql_query("Select * from safety", conn)
print(df)