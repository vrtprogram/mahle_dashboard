"""
This is the property of VR Technologies please take permission before redistribution.
Author@ Swapnil Diwakar
EmailId@ Diwakarswapnil@gmail.com
Date@ 13/07/23

"""

import streamlit as st
import plotly.express as px
from streamlit_lottie import st_lottie
import json
import sqlite3
import pandas as pd
from annotated_text import annotated_text

# -------- Making Connection to Database -----------------#
conn = sqlite3.connect("database/delivery.db")
df = pd.read_sql_query("Select * From DELIVERY ORDER BY Date desc LIMIT 7", conn)
# print(df)
# ---------------------------------------------------------#


st.set_page_config(page_title="Delivery",
                   initial_sidebar_state="collapsed",
                   layout="wide",

                   )


def main():
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

    st.session_state['count'] = 1

    # CSS to inject contained in a string
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

    colA, colB = st.columns((3, 4), gap="small")
    with colA:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("""## <div style="font-size:200%;color:blue"><u>Delivery Dashboard""", unsafe_allow_html=True)
    with colB:
        with open("Assets/delivery.json", "r") as f:
            data = json.load(f)
        st_lottie(data, speed=1, width=400)

    def func():
        st.markdown("___")
        st.write("Today's Production")
        colA, colB, colC, colD = st.columns((2, 2, 2, 2))
        with colB:
            annotated_text("Last Updated :")
            annotated_text("Today's Target :")
            annotated_text("Actual :")
        with colC:
            annotated_text((f"{df['Date'][0]}", '', 'Green'))
            annotated_text((f"{df['TARGET'][0]}", '', ''))
            annotated_text((f"{df['ACTUAL'][0]}", '', ''))
        st.markdown("___")
        st.write("# <u>Target Vs Actual Data Trend<u>", unsafe_allow_html=True)
        cola, colb = st.columns((2, 2))
        with cola:
            fig = px.bar(df, x='Date', y=['TARGET', 'ACTUAL'], barmode='group', height=700, width=600,
                         title="Actual Vs Target")
            fig.update_layout(
                font=dict(
                    size=60  # Increase the font size to 14
                )
            )
            st.plotly_chart(fig,width=200)
            # pass
        with colb:
            # pass
            fig2 = px.line(df, x='Date', y=['TARGET', 'ACTUAL'], height=700, width=600, title="Actual Vs Target",
                           color_discrete_map={
                               'Target': "#456987",
                               'Actual': "#147852"
                           })
            fig2.layout.template = "presentation"
            st.plotly_chart(fig2, width=100)

    func()

    with st.container():
        st.write("---")
        st.write("# Latest Issues:")
        spacer1, col1, spacer2 = st.columns((0.8, 20, 0.8), gap='large')
        with col1:
            df_issues = df[['Date', 'ISSUES']]
            st.table(df_issues)


if __name__ == "__main__":
    main()
