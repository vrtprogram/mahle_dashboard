import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px
from annotated_text import annotated_text as at

conn = sqlite3.connect("database/safety.db")
cur = conn.cursor()
df=pd.read_sql_query("SELECT * FROM 'UNSAFE INCIDENCES'",conn)

st.set_page_config(layout="wide", page_title="Safety FTD", initial_sidebar_state="collapsed")

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
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    st.markdown(
        """
        <center>
         <div style="margin-bottom:1rem;background-color: blue; font-family:fantasy">
            <i><u>
                <h1>
                    Safety FTD 
                </h1>
            </u></i>
        </div>
        </center>
        """,
        unsafe_allow_html=True
    )

    d_col1, d_col2=st.columns((1,0.3))
    with d_col2:
        on_date = st.date_input(":green[Select Date:]")
    col1,col2=st.columns((1.4,1))
    with col1:
        date=datetime.now().date().strftime("%d-%m-%Y")
        st.subheader(f"Status as on: {date}",divider="rainbow")
        colr1,colr2=st.columns((1,0.6))
        with colr1:
            
            # st.markdown(f"""<p style='font-size:1.2rem;text-align:center;background-color:skyblue; font-weight:bold;'>Daily Update: {date}</p>""",unsafe_allow_html=True)
            # st.write(date)
            total_event = {}
            for i in df['DATE']:
                # print(i)
                cur.execute(f"SELECT COUNT(*) FROM 'UNSAFE INCIDENCES' WHERE DATE = '{i}'")
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
                            height=450, width=350, title="Daily Trends", template='plotly_dark')
            st.plotly_chart(fig)
        with colr2:
            # at("Hello ","world!", "noun", color="#8ef", border="1px dashed red")
            st.write("""<p style='color:red;font-weight:bold; padding-top:12rem;'>Rec Lost Time Injury:</p>""",unsafe_allow_html=True)
            st.write("""<p style='color:magenta;font-weight:bold;'>Rec Accident:</p>""",unsafe_allow_html=True)
            st.write("""<p style='color:yellow;font-weight:bold;'>First Aid:</p>""",unsafe_allow_html=True)
            st.write("""<p style='color:yellow;font-weight:bold;'>Near MIS:</p>""",unsafe_allow_html=True)
            st.write("""<p style='color:blue;font-weight:bold;'>Fire:</p>""",unsafe_allow_html=True)
            st.write("""<p style='color:green;font-weight:bold;'>No Incident:</p>""",unsafe_allow_html=True)
    with col2:
        st.subheader(":red[Safety Incident Details]",divider="rainbow")


    cl1,cl2,cl3=st.columns((1,4,1))
    with cl2:
        st.markdown("""<center><div style='font-size:1.5rem;font-weight:bold;'><u>SAFETY INCIDENTS TRACKING</u></div></center>""",unsafe_allow_html=True)
    # on_date = st.date_input("Data on:")
    # st.write(on_date)
    cr11,cr12,cr13,cr14,cr15=st.columns((1,1,1,1,1))
    with cr11:
        st.markdown(f"""<div style='background-color:red;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Lost Time Injury FTD:</div>""",unsafe_allow_html=True)
    with cr12:
        st.markdown(f"""<div style='background-color:green;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Accident FTD:</div>""",unsafe_allow_html=True)
    with cr13:
        st.markdown(f"""<div style='background-color:yellow;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>First Aid FTD:</div>""",unsafe_allow_html=True)
    with cr14:
        st.markdown(f"""<div style='background-color:magenta;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Near MIS FTD:</div>""",unsafe_allow_html=True)
    with cr15:
        st.markdown(f"""<div style='background-color:skyblue;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Fire FTD:</div>""",unsafe_allow_html=True)
    
    # *** Get Data between two dates***
    # from_date = st.date_input("From:")
    # to_date = st.date_input("To:")
    # days = from_date - to_date
    # query = "SELECT SUM(Value) AS Total FROM UNSAFE_PRACTICE_TRACKING WHERE Date BETWEEN ? AND ?"
    # cursor.execute(query, (from_date, to_date))
    # Value_SD = cursor.fetchone()[0]
    # if st.button("Show"):
    #     st.write(f"Total value for {days} days: {Value_SD}")


main()
