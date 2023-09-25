
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
import json
from streamlit_lottie import st_lottie

# ----------- Initializing Database --------------#
conn = sqlite3.connect("database/safety.db")
cur = conn.cursor()
df = pd.read_sql_query("Select * From Safety ORDER BY date desc limit 40", conn)
# print(df)
# ['TIME_STAMP', 'DATE', 'EVENT', 'LOCATION', 'STATUS']
# -------------------------------------------------

# -------------------- Setting Up Page layout --------------------------#
st.set_page_config(layout="wide", page_title="Safety", initial_sidebar_state="collapsed")

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


def main():
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

    col1, col2 = st.columns((7, 5), gap="small")
    with col1:
        st.write("""## <div style="font-size:250%;color:green"><u>Safety Dashboard """, unsafe_allow_html=True)
        with col2:
            with open("Assets/safty.json", 'r') as f:
                data = json.load(f)
            st_lottie(data, speed=0.3, loop=True, height=350, width=350)
    # ----------------------------------------------------------------------------

    st.markdown("____")
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

            fig = px.bar(new_event_df, x='DATE', y='NO. OF EVENTS',
                         height=700, width=500, title="Daily Trends", template='plotly_dark')
            st.plotly_chart(fig)
        with col2:
            fig2 = px.line(new_event_df, x="DATE", y='NO. OF EVENTS', height=700, width=500, template='plotly_dark')
            st.plotly_chart(fig2)

    st.markdown("___")
    st.markdown("## Latest Events :")
    df_new = df[['DATE', 'EVENT', 'LOCATION', 'STATUS']]
    st.table(df_new)


if __name__ == "__main__":
    main()
