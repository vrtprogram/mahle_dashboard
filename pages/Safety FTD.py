import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px
from annotated_text import annotated_text,annotation

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
        # st.write(on_date)

    new_dict=dict()
    new_dict['Recordable Lost Time']=56
    new_dict['First Aid']=0
    new_dict['Recordable Accident']=0
    new_dict['Near MIS']=0
    new_dict['Fire']=0

    data=dict()
    data['INCIDENT'] = "testing incident"
    data['DATETIME'] = on_date
    data['LOCATION'] = "Location testing"
    data['MEDICAL']  = True
    data['ACTION']   = "Action taken"
    # for item in df["CATEGORY"]:
    #     if item == "Recordable Lost Time":
    #         new_dict["Recordable Lost Time"] +=1
    #     if item == "First Aid":
    #         new_dict["First Aid"] +=1
    #     if item == "Recordable Accident":
    #         new_dict["Recordable Accident"] +=1
    #     if item == "Near Miss":
    #         new_dict["Near MIS"] +=1
    #     if item == "Fire":
    #         new_dict["Fire"] +=1

    col1,col2=st.columns((1.4,1))
    with col1:
        # date=datetime.now().date().strftime("%d-%m-%Y")
        st.subheader(f"Status as on: {on_date}",divider="rainbow")
        colr1,colr2,colr3=st.columns((1,0.6,0.09))
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
            st.write("""<div style='padding-top:10rem;'></div>""",unsafe_allow_html=True)
            annotated_text(annotation("Rec Lost Time Injury:",color="red",background="skyblue"))
            annotated_text(annotation("Rec Accident:",color="brown",background="skyblue"))
            annotated_text(annotation("First Aid:",color="orange",background="skyblue"))
            annotated_text(annotation("Near MIS:",color="yellow",background="skyblue"))
            annotated_text(annotation("Fire:",color="blue",background="skyblue"))
            annotated_text(annotation("No Incident:",color="green",background="skyblue"))
        with colr3:
            st.write("""<div style='padding-top:10rem;'></div>""",unsafe_allow_html=True)
            st.write(f"{new_dict['Recordable Lost Time']}")
            st.write(f"{new_dict['Recordable Accident']}")
            st.write(f"{new_dict['First Aid']}")
            st.write(f"{new_dict['Near MIS']}")
            st.write(f"{new_dict['Fire']}")
            st.write("0")
    with col2:
        st.subheader(":red[Safety Incident Details]",divider="rainbow")
        st.markdown("""
                    <style>
                        .float-container {
                            # border: 3px solid #fff;
                            padding: 20px;
                        }
                        .float-child {
                            width: 50%;
                            float: left;
                            padding: 20px;
                            border: 2px solid red;
                        }
                    </style>
            <div class="float-container">
                <div class="float-child">
                    <div class="green">Float Column 1</div>
                </div>
                <div class="float-child">
                    <div class="blue">Float Column 2</div>
                </div>
            </div>
        """,unsafe_allow_html=True)
        # st.markdown(f"""<div><div style='color:red; height:5rem; border:1px solid black;'>Recordable Lost Time</div><div style='height:2.5rem;border:1px solid black;'>this is incident</div></div>""",unsafe_allow_html=True)
        # st.markdown("""<input type='tel' id='phone' name='phone' placeholder='123-45-678'>""",unsafe_allow_html=True)


    cl1,cl2,cl3=st.columns((1,4,1))
    with cl2:
        st.markdown("""<center><div style='font-size:1.5rem;font-weight:bold;'><u>SAFETY INCIDENTS TRACKING</u></div></center>""",unsafe_allow_html=True)
    # on_date = st.date_input("Data on:")
    # st.write(on_date)

    cr11,cr12,cr13,cr14,cr15=st.columns((1,1,1,1,1))
    with cr11:
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Lost Time Injury FTD:
                    <h4 style='color:white;font-weight:bold;'>$$</h4></div>""".replace("$$",str(new_dict["Recordable Lost Time"])),unsafe_allow_html=True)
    with cr12:
        st.markdown(f"""<div style='background-color:red;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Accident FTD:
                    <h4 style='color:white;font-weight:bold;'>$$</h4></div>""".replace("$$",str(new_dict["Recordable Accident"])),unsafe_allow_html=True)
        # st.markdown(f"""<div style='background-color:green;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Accident FTD:</div>""",unsafe_allow_html=True)
    with cr13:
        st.markdown(f"""<div style='background-color:orange;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>First Aid FTD:
                    <h4 style='color:white;font-weight:bold;'>$$</h4></div>""".replace("$$",str(new_dict["First Aid"])),unsafe_allow_html=True)
        # st.markdown(f"""<div style='background-color:yellow;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>First Aid FTD:</div>""",unsafe_allow_html=True)
    with cr14:
        st.markdown(f"""<div style='background-color:yellow;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Near MIS FTD:
                    <h4 style='color:white;font-weight:bold;'>$$</h4></div>""".replace("$$",str(new_dict["Near MIS"])),unsafe_allow_html=True)
        # st.markdown(f"""<div style='background-color:magenta;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Near MIS FTD:</div>""",unsafe_allow_html=True)
    with cr15:
        st.markdown(f"""<div style='background-color:skyblue;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Fire FTD:
                    <h4 style='color:white;font-weight:bold;'>$$</h4></div>""".replace("$$",str(new_dict["Fire"])),unsafe_allow_html=True)
        # st.markdown(f"""<div style='background-color:skyblue;height:10rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Fire FTD:</div>""",unsafe_allow_html=True)
    
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
