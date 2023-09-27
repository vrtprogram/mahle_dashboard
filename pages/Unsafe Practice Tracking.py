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
from datetime import datetime, timedelta

# import json
# from streamlit_lottie import st_lottie

# ----------- Initializing Database --------------#
conn = sqlite3.connect("database/safety.db")
month = datetime.now().month
year = datetime.now().year
cur = conn.cursor()
if month < 10:
    df = pd.read_sql_query(f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%Y-%m', date) = '{year}-0{month}' ", conn)
else:
    df = pd.read_sql_query(
        f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%Y-%m', date) = '{year}-{month}' AND strftime('%Y', date) = '{year} ",
        conn)

closed = 0
for item in df["STATUS"]:
    if item == "Close" or item == "Closed" or item == "close" or item == 'closed':
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
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton{visibility: hidden}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)


def main():
    # -----------------------------------------------------
    st.markdown(
        """
        <center>
         <div>
            <i><u>
                <h1 style="font-size:60px;">
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
            st.metric("Closure Percentage", format((closed / len(df))*100, ".2f"))
    st.markdown("---")
    st.markdown("## Unsafe Practices Trend :")
    with st.container():
        col1, col2 = st.columns((8, 8), gap="small")
        with col1:
            current_month = datetime.now().month
            current_year = datetime.now().year
            current_date = datetime(year, month, 1)

            while current_date.weekday() != 0:  # 0 represents Monday
                current_date += timedelta(days=1)

            lst_value = []
            lst_week_no = []
            week_count = 0

            while current_date.month == month:
                df_week: pd.DataFrame = pd.DataFrame()
                start_of_week = current_date
                end_of_week = current_date + timedelta(days=6)
                current_date += timedelta(days=7)
                df_week = pd.read_sql_query(
                    f"Select * from 'UNSAFE PRACTICES TRACKING' where date between '{start_of_week}' and '{end_of_week}'", conn)

                week_count += 1
                lst_value.append(len(df_week))
                lst_week_no.append(week_count)

            df_weekly = pd.DataFrame()
            df_weekly['No. Of Events'] = lst_value
            df_weekly['Weeks'] = lst_week_no
            fig = px.bar(df_weekly, x='Weeks', y='No. Of Events', title="Monthly Trends", template='plotly_dark', width=700)
            fig.update_xaxes(
                tickmode='array',
                tickvals=df_weekly["Weeks"]
            )
            st.plotly_chart(fig)
        with col2:
            new_df = pd.DataFrame()
            lst = []
            new_df['Month'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                               'October', 'November', 'December']
            for i in range(0, 12):
                if i < 10:
                    df_month = pd.read_sql_query(f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%m', date) = '0{i + 1}' ", conn)
                else:
                    df_month = pd.read_sql_query(f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%m', date) = '{i + 1}' ", conn)
                lst.append(len(df_month))

            new_df['No. Of Events'] = lst

            fig2 = px.bar(new_df, x='Month', y='No. Of Events', title="Yearly Trends", width=700)
            st.plotly_chart(fig2)

    st.markdown("""
        <style>
        .col_heading{
            background:"green";
        }
        
    """, unsafe_allow_html=True)

    st.markdown("___")
    st.markdown("## Open Observations :")
    df_new = pd.read_sql_query("""SELECT * FROM 'UNSAFE PRACTICES TRACKING' WHERE STATUS='Open' ORDER BY DATE DESC """, conn)
    # print(df_new)
    st.table(df_new[["DATE", "CATEGORY", "RESPONSIBILITY", "LOCATION", "STATUS"]])


if __name__ == "__main__":
    main()
