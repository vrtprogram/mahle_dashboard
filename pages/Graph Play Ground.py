import sqlite3
import pandas as pd
import streamlit as st
import pygwalker as pyg

st.write("<h1>Welcome To Graph Ground", unsafe_allow_html=True)
st.write("Select The Time Period For Data")
from_date = st.date_input("From date")
to_date = st.date_input("To Date")
selected = st.selectbox("Select the Data Set to load", options=['', 'Delivery', 'Personal', 'Quality', 'Safety'])

match selected:
    case 'Delivery':
        conn = sqlite3.connect("database/delivery.db")
        df = pd.read_sql_query(f'Select * from delivery where Date Between "{from_date}" and "{to_date} order by date desc"', conn)
        # print(df)
    case 'Personal':
        conn = sqlite3.connect("database/personal.db")
        df = pd.read_sql_query(f'Select * from personal where Date Between "{from_date}" and "{to_date}"', conn)
        # print(df)
    case 'Quality':
        conn = sqlite3.connect("database/quality.db")
        df = pd.read_sql_query(f'Select * from quality where Date Between "{from_date}" and "{to_date}"', conn)
        # print(df)
    case 'Safety':
        conn = sqlite3.connect("database/safety.db")
        df = pd.read_sql_query(f'Select * from safety where Date Between "{from_date}" and "{to_date}"', conn)
        # print(df)

with st.container():
    if selected != '':
        pyg.walk(df, env='Streamlit')
