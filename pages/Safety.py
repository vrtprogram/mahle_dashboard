"""
This is the property of VR Technologies please take permission before redistribution.
Author@ Swapnil Diwakar
EmailId@ Diwakarswapnil@gmail.com
Date@ 13/07/23

"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# import json
# from streamlit_lottie import st_lottie

# ----------- Initializing Database --------------#
conn = sqlite3.connect("database/safety.db")
month = datetime.now().month
year = datetime.now().year
cur = conn.cursor()
if month < 10:
    df = pd.read_sql_query(f"Select * From Safety WHERE strftime('%Y-%m', date) = '{year}-0{month}' ", conn)
else:
    df = pd.read_sql_query(f"Select * From Safety WHERE strftime('%Y-%m', date) = '{year}-{month}' AND strftime('%Y', date) = '{year} ", conn)

closed = 0
for item in df["STATUS"]:
    if item == "Close" or item == "Closed" or item == "close" or item == 'closed' :
        closed += 1
# -------------------------------------------------

# -------------------- Setting Up Page layout --------------------------#
st.set_page_config(layout="wide", page_title="Unsafe Practices Tracking", initial_sidebar_state="collapsed")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 20px;
                    padding-bottom: 0rem;
                    padding-left: 10px;
                    padding-right: 10px;
                }
        </style>
        """, unsafe_allow_html=True)


def main():
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton{visibility: hidden}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # -----------------------------------------------------
    st.markdown(
        """
        <center>
         <div style="background-color: blue; font-family:fantasy">
            <i><u>
                <h1>
                    Unsafe Practice Tracking
                </h1>
            </u></i>
        </div>
        </center>
        """,
        unsafe_allow_html=True
    )

    st.markdown("____")
    col_indices_1, col_indices_2, col_indices_3 = st.columns((0.5, 2, 0.5))

    with col_indices_2:
        col_indices_A, col_indices_B, col_indices_C = st.columns((2, 2, 2))
        with col_indices_A:
            st.metric("Unsafe Practices", len(df))
        with col_indices_B:
            st.metric("Unsafe Practices Closed", closed)
        with col_indices_C:
            st.metric("Closure Percentage", int((closed / len(df))))
    st.markdown("---")
    st.markdown("## Unsafe Practices Trend :")
    with st.container():
        col1, col2 = st.columns((8, 8), gap="small")
        with col1:
            total_event = {}
            for i in df['DATE']:
                # print(i)
                cur.execute(f"SELECT COUNT(*) FROM SAFETY WHERE DATE = '{i}'")
                value = cur.fetchall()
                no_of_event = value[0][0]
                if i in total_event.keys():
                    pass
                else:
                    total_event[i] = no_of_event

            # print(total_event)
            new_event_df = pd.DataFrame()
            new_event_df['DATE'] = total_event.keys()
            new_event_df['NO. OF EVENTS'] = total_event.values()
            # print(new_event_df)

            fig = px.bar(new_event_df, x='DATE', y='NO. OF EVENTS', title="Monthly Trends", template='plotly_dark')
            st.plotly_chart(fig)
        with col2:
            new_df = pd.DataFrame()
            lst = []
            new_df['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            for i in range(0, 12):
                if i < 10:
                    df_year = pd.read_sql_query(f"Select * From Safety WHERE strftime('%m', date) = '0{i+1}' ", conn)
                else:
                    df_year = pd.read_sql_query(f"Select * From Safety WHERE strftime('%m', date) = '{i+1}' ", conn)
                lst.append(len(df_year))

            new_df['No. Of Events'] = lst

            fig2 = px.bar(new_df, x='Month', y='No. Of Events', title="Yearly Trends")
            st.plotly_chart(fig2)

    st.markdown("""
        <style>
        .col_heading{
            background:"green";
        }
        
    """, unsafe_allow_html=True)

    st.markdown("___")
    st.markdown("## Latest Events :")
    df_new = pd.read_sql_query("""SELECT * FROM SAFETY WHERE STATUS='Open' ORDER BY TIME_STAMP DESC """, conn)
    st.table(df_new)

    # df_test = pd.read_sql_query("""
    #             SELECT
    #                 strftime('%Y', time_stamp) AS year,
    #                 strftime('%W', time_stamp) AS week_number,
    #                 MIN(time_stamp) AS start_of_week,
    #                 MAX(time_stamp) AS end_of_week
    #             FROM
    #                 SAFETY
    #             WHERE
    #                 strftime('%w', time_stamp) = '1' -- '1' represents Monday in SQLite
    #             GROUP BY
    #                 year, week_number
    #             ORDER BY
    #                 year DESC, week_number DESC;
    # """, conn
    #                             )
    # print(df_test)


if __name__ == "__main__":
    main()
