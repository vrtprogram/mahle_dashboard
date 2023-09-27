from datetime import datetime, timedelta
import sqlite3

import pandas as pd

conn = sqlite3.connect("database/safety.db")

# Define the year and month you want to work with
year = datetime.now().year
month = datetime.now().month

# Create a list to store the weeks
weeks = []

# Start with the first day of the month
current_date = datetime(year, month, 1)

# Find the first Monday of the month
while current_date.weekday() != 0:  # 0 represents Monday
    current_date += timedelta(days=1)

# Loop through the weeks of the month
lst_value = []
lst_week_no = []
week_count = 0
while current_date.month == month:
    df_apple : pd.DataFrame = pd.DataFrame()
    start_of_week = current_date
    end_of_week = current_date + timedelta(days=6)
    start_of_week = start_of_week.date()
    end_of_week = end_of_week.date()
    print(start_of_week, end_of_week)
    week_number = current_date.strftime("%U")

    df_apple = pd.read_sql_query(
        f"Select * from Safety where date between '{start_of_week}' and '{end_of_week}'", conn)
    week_count +=1
    lst_value.append(len(df_apple))
    lst_week_no.append(week_count)


    current_date += timedelta(days=7)  # Move to the next Monday

df = pd.DataFrame()
df["value"] = lst_value
df["week"] = lst_week_no
print(df)