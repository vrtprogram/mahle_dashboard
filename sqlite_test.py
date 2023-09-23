# import sqlite3
# import pandas as pd
# from datetime import datetime
# conn = sqlite3.connect("database/quality.db")
# cur  = conn.cursor()
#
# # cur.execute('DROP TABLE DELIVERY')
# # cur.execute("CREATE TABLE QUALITY(TIME_STAMP DATETIME, DATE DATE, PART_NAME TEXT ,TOTAL_PRODUCTION INTEGER, TOTAL_NG INTEGER, ISSUE TEXT)")
# cur.execute(f'INSERT INTO QUALITY values ("{datetime.now()}", "2023-07-08", "Fx5u", 7000, 600, "Operator was BAD")')
# conn.commit()
#
# df = pd.read_sql_query('SELECT * FROM QUALITY', conn)
# print(df)

import streamlit_authenticator as stauth

hassed_passwd = stauth.Hasher(['admin']).generate()
print(hassed_passwd)