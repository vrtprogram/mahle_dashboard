"""
This is the property of VR Technologies please take permission before redistribution.
Author@ Swapnil Diwakar
EmailId@ Diwakarswapnil@gmail.com
Date@ 13/07/23

"""

import streamlit as st
import json
import sqlite3
from plotly import express as px
from annotated_text import annotated_text
from streamlit_lottie import st_lottie
import pandas as pd

# -------------- Initializing The Data Base -----------------------------------#
conn = sqlite3.connect('database/personal.db')
df = pd.read_sql_query("SELECT * FROM PERSONAL ORDER BY DATE DESC LIMIT 7", conn)
# print(df)
# --------------------------------------------------------------------------------

# --------------- Setting up Page Layout --------------------------------------#
st.set_page_config(layout="wide", page_title="Personal", initial_sidebar_state="collapsed")

# Hiding the streamlit buttons
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Setting The page side layout
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

colimg1, colimg2, colimg3 = st.columns((1.75, 1, 9), gap="small")
with colimg1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.image("resources/logo.png")
with colimg3:
    st.write("")
    st.write("")
    st.markdown("""<u><div style="font-size:450%;color:white"> VR Technologies</h1></u>""", unsafe_allow_html=True)

# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

# Images at the side
colA, colB = st.columns((5, 7), gap="small")
with colA:
    st.write("""## <div style="font-size:200%;color:blue"><u>Personal Dashboard """, unsafe_allow_html=True)
with colB:
    with open("Assets/worker.json", "r") as f:
        data = json.load(f)
    st_lottie(data)
# ---------------------------------------------------------------------------------------
st.markdown("___")
with st.container():
    st.write("""<div style = "font-size:200%"><u>Today's Data""", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3, col4 = st.columns((2, 2, 2, 2))
        with col2:
            annotated_text("Last Updated      : ")
            annotated_text("Manpower required : ")
            annotated_text("Manpower Present  : ")
            annotated_text("Manpower Absent   : ")
            annotated_text("Personal Gap      : ")
        with col3:
            annotated_text((f"{df['Date'][0]}", "", "green"))
            annotated_text((f"{df['Manpower_Req'][0]}", "", "green"))
            annotated_text((f"{df['Manpower_Req'][0] - df['Manpower_Absent'][0]}", "", "Green"))
            annotated_text((f"{df['Manpower_Absent'][0]}", "", "red"))
            manpower_gap = (df['Manpower_Absent'][0] / df['Manpower_Req'][0]) * 100
            annotated_text((f"{manpower_gap:0.2f}%", "", "red"))
        st.markdown("___")
with st.container():
    st.subheader("Daily Trends")
    date = []
    Manpower_per = []
    Manpower_abs = []

    for i in df['Date']:
        date.append(i)
    for i in zip(df['Manpower_Req'], df['Manpower_Absent']):
        req, absent = i
        Manpower_per.append(req)
        Manpower_abs.append(req - absent)

    new_df_data = {
        'Date': date,
        'Manpower_Required': Manpower_per,
        'Manpower_Present': Manpower_abs
    }
    new_df = pd.DataFrame(new_df_data)

    col1, col2 = st.columns((2, 2), gap='small')
    with col1:
        fig = px.bar(
            new_df,
            x='Date',
            y=['Manpower_Present', 'Manpower_Required'],
            barmode='group',
            title="Daily Attendance Trend"
        )
        st.plotly_chart(fig)
    with col2:
        fig = px.line(
            df,
            x='Date',
            y='Casual_Present',
            title='Casual Attendance Trend'
        )
        st.plotly_chart(fig)
#
st.markdown('___')
st.markdown("""<div style = "font-size:200%"><u>Daily Manpower Data""", unsafe_allow_html=True)
df_mod = df[['Date', 'Manpower_Req', 'Manpower_Absent', 'Casual_Present']]
st.table(df_mod)
