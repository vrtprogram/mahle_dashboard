import streamlit as st
import sqlite3
import base64
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import datetime
import calendar
# import altair as alt
from xml.etree import ElementTree as ET


#************ Body layout Start ************#
on_date = "%y-%m-%d"    #Date define for all pages
tm = "%H-%M-%S"

def  layout(heading):
    st.set_page_config(layout="wide", page_title="Mahle Dashboard", initial_sidebar_state="collapsed")
    st.markdown("""<style>.block-container { padding: 0.5rem; }</style>""", unsafe_allow_html=True)
    hide_streamlit_style = """<style>#MainMenu { visibility: hidden;}footer { visibility: hidden;}</style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown("""
        <center>
            <div style="margin-bottom:0.6rem; background-color:darkblue; font-family:fantasy"><i><h1 style='color:white';>heading</h1></i></div>
        </center>""".replace("heading",str(heading)),unsafe_allow_html=True
    )
    # st.markdown("___")
    st.write("""
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
            text-align: center;
        }
        table, th, td {
            border: 1px solid black;
            padding: 10px;
            font-size:0.7rem;
        }
        th {
            text-align: center;
            background-color: #f2f2f2;
            font-size:0.8rem;
        }
        </style>
    """, unsafe_allow_html=True)

def current_updates():
    d_col1, d_col2=st.columns((1,0.3))
    with d_col1:
        # st.link_button("Home","/App")
        pass
    with d_col2:
        st.markdown("""<style>
                        .st-emotion-cache-vft1hk:nth-child(0){}
                    </style>""", unsafe_allow_html=True)
        global on_date
        on_date = st.date_input(":green[Select Date:]")

def current_date():
    d_col1, d_col2=st.columns((1,0.3))
    with d_col1:
        # st.link_button("Home","/App")
        pass
    with d_col2:
        date = datetime.datetime.now().date().strftime("%Y-%m-%d")
        st.markdown(f"""<center style='padding-top:1rem;'><div style=' width:75%;background-color:lightgray;'>Date: {date}</center></div>""",unsafe_allow_html=True)
    st.markdown("___")
    return date

#************ Body layout End ************#

#************ Main Data Fetch Start ************#
def fetch_month_data(table_name):   #Fetch data for current month
    with sqlite3.connect("database/main_database.db") as conn:
        query = f"SELECT * FROM \"{table_name}\";"
        dataframe = pd.read_sql_query(query, conn)
        dataframe['DATE'] = pd.to_datetime(dataframe['DATE'])
        current_month = pd.Timestamp('now').to_period('M')
        dataframe = dataframe[((dataframe['DATE'].dt.to_period('M')) == current_month)]
        # dataframe['DATE'] = dataframe['DATE'].dt.strftime('%Y-%m-%d')
    return dataframe

def fetch_data(table_name): #Fetch data for current year
    with sqlite3.connect("database/main_database.db") as conn:
        query = f"SELECT * FROM \"{table_name}\";"
        dataframe = pd.read_sql_query(query, conn)
        dataframe['DATE'] = pd.to_datetime(dataframe['DATE'])
        current_year = pd.Timestamp('now').to_period('Y')
        # current_month = pd.Timestamp('now').to_period('M')
        dataframe = dataframe[((dataframe['DATE'].dt.to_period('Y')) == current_year)]
        # dataframe['DATE'] = dataframe['DATE'].dt.strftime('%Y-%m-%d')
    return dataframe

def data_filter_between(table_name:str, start_date, end_date):  #Filter data between dates
    with sqlite3.connect("database/main_database.db") as conn:
        query = f"SELECT * FROM \"{table_name}\" WHERE DATE BETWEEN ? AND ? ;"
        dataframe = pd.read_sql_query(query, conn, params=(start_date, end_date))
        # dataframe['DATE'] = dataframe['DATE'].dt.strftime('%Y-%m-%d')
        # dataframe = dataframe.sort_values(by="DATE", ascending=True)
    return dataframe

#************ Main Data Fetch End ************#

#************************** Safety_FTD Start **************************#
def safety_ftd():
    class data():
        def __init__(self, incident, time, location, medical, action):
            self.incident = incident
            self.time = time
            self.location = location
            self.medical = medical
            self.action = action
        def show(self):
            return f"incident{self.incident} at time {self.time} on location {self.location}, medical given {self.medical} and take action {self.action}"
    try:
        new_dict = {
            "Recordable Lost Time": 0,
            "Recordable Accident": 0,
            "First Aid": 0,
            "Near MIS": 0,
            "Fire": 0
        }
        row_data = fetch_data("INCIDENCES DETAILS")
        for index, row in row_data.iterrows():
            date = pd.Timestamp(row["DATE"]).strftime('%Y-%m-%d')
            if date == f"{on_date}":
                if row["CATEGORY"] == "Recordable Loss Time Injury":
                    new_dict["Recordable Lost Time"] +=1
                if row["CATEGORY"] == "Recordable Accident": 
                    new_dict["Recordable Accident"] +=1
                if row["CATEGORY"] == "First Aid":
                    new_dict["First Aid"] +=1
                if row["CATEGORY"] == "Near MIS":
                    new_dict["Near MIS"] +=1
                if row["CATEGORY"] == "Fire":
                    new_dict["Fire"] +=1

        # st.subheader(f"Status as on: {on_date}", divider="gray")
        st.markdown(f"""
            <div>
                <h3 style='position:absolute; bottom:0rem;'>Status as on: {on_date}</h3>
            </div>
            <hr>
        """, unsafe_allow_html=True)
        
        st.markdown(
            """
            <style>
            .custom {
                margin: 0.4rem;
                padding-top: 0.7rem;
                border: 1px solid black;
                height: 5rem;
                border-radius: 0.7rem;
                font-weight: bold;
                font-size:0.7rem;
                box-shadow: 5px 5px 10px;
                text-align: center;
            }
            .custom h4{ color:white;font-weight:bold; padding-top:0.5rem; }
            @media (min-width: 1920px) and (max-width: 2860px){
                .custom { font-size:1.35rem; height:10rem; }
                .custom h4{ color:white; font-size:1.3rem; font-weight:bold; padding-top:1rem}
            }
            </style>
            """,
            unsafe_allow_html=True
        )   #custom css for columns
        cr11,cr12,cr13,cr14,cr15=st.columns((1,1,1,1,1))
        with cr11:
            st.markdown(f"""<div class="custom" style='background-color:red;'>Recordable Lost Time Injury FTD:
                        <h4>{new_dict["Recordable Lost Time"]}</h4></div>""",unsafe_allow_html=True)
        with cr12:
            st.markdown(f"""<div class="custom" style='background-color:#cc4757;'>Recordable Accident FTD:
                        <h4>{new_dict["Recordable Accident"]}</h4></div>""",unsafe_allow_html=True)
        with cr13:
            st.markdown(f"""<div class="custom" style='background-color:orange;'>First Aid FTD:
                        <h4>{new_dict["First Aid"]}</h4></div>""",unsafe_allow_html=True)
        with cr14:
            st.markdown(f"""<div class="custom" style='background-color:yellow;'>Near MIS FTD:
                        <h4>{new_dict["Near MIS"]}</h4></div>""",unsafe_allow_html=True)
        with cr15:
            st.markdown(f"""<div class="custom" style='background-color:skyblue;'>Fire FTD:
                        <h4>{new_dict["Fire"]}</h4></div>""",unsafe_allow_html=True)
        pass
    except Exception as e:
        print("An error: ", str(e))
        pass
    try:
        Record_lost_time = data("Incident", "time", "location", "medical", "action")
        First_aid = data("Incident", "time", "location", "medical", "action")
        Near_mis = data("Incident", "time", "location", "medical", "action")
        Fire_mtd = data("Incident", "time", "location", "medical", "action")
        # colors = ["red", "darkred", "orange", "yellow", "blue", "green"]
        colors = {
            "record_lost_time": False,
            "record_accident": False,
            "first_aid": False,
            "near_mis": False,
            "fire_mtd": False
        }
        color = "green" #Default color
        for index, row in row_data.iterrows():
            incident = data(row['EVENT'], row['TIME'], row['VALUE STREAM'], row['MEDICAL'], row['ACTION'])
            date = pd.Timestamp(row["DATE"]).strftime('%Y-%m-%d')
            if date == f"{on_date}":
                if row["CATEGORY"] == "Recordable Loss Time Injury":
                    Record_lost_time = incident #Insert data in class object from incident acording to category 
                    colors["record_lost_time"] = True   
                if row["CATEGORY"] == "Recordable Accident":
                    colors["record_accident"] = True
                    pass
                if row["CATEGORY"] == "First Aid":
                    First_aid = incident
                    colors["first_aid"] = True
                if row["CATEGORY"] == "Near MIS":
                    Near_mis = incident
                    colors["near_mis"] = True
                if row["CATEGORY"] == "Fire":
                    Fire_mtd = incident
                    colors["fire_mtd"] = True
        
        #Colors define for all category acording to priority
        if on_date.weekday() == 6: color = "blue"
        else:
            if colors["record_lost_time"] == True: color = "red"
            elif colors["record_accident"] == True: color = "#cc4757"
            elif colors["first_aid"] == True: color = "orange"
            elif colors["near_mis"] == True: color = "yellow"
            elif colors["fire_mtd"] == True: color = "blue"
            else: color = "green"
        col1,col2=st.columns((1,1.7))
        with col1:  #******** Dynamic S letter ********#
            tree = ET.parse('resources\S.svg')
            root = tree.getroot()
            current_date = datetime.date.today()
            row_data = fetch_month_data("INCIDENCES DETAILS")
            first_day_of_month = current_date.replace(day=1)
            days_to_add = 0
            for i in range(1, 32):
                colors = {
                        "record_lost_time": False, "record_accident": False,
                        "first_aid": False, "near_mis": False, "fire_mtd": False
                    }
                if i < 10:
                    target_element = root.find(f".//*[@id='untitled-u-day{i}']")
                else:
                    target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
                new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
                days_to_add += 1
                df = row_data[row_data["DATE"] == f"{new_date}"]
                if len(row_data) == 0:
                    if new_date.weekday() == 6:
                        target_element.set('fill', 'blue')
                        tree.write('s_out.svg')
                    else:
                        target_element.set('fill', '#d2dbed')
                        tree.write('s_out.svg')
                elif new_date.weekday() == 6:
                        target_element.set('fill', 'blue')
                        tree.write('s_out.svg')
                else:
                    for index, row in df.iterrows():
                        if row["CATEGORY"] == "Recordable Loss Time Injury":
                            colors["record_lost_time"] = True
                        if row["CATEGORY"] == "Recordable Accident":
                            colors["record_accident"] = True
                        if row["CATEGORY"] == "First Aid":
                            colors["first_aid"] = True
                        if row["CATEGORY"] == "Near MIS":
                            colors["near_mis"] = True
                        if row["CATEGORY"] == "Fire":
                            colors["fire_mtd"] = True
                        if new_date.weekday() == 6: color = "blue"
                        else:
                            if colors["record_lost_time"] == True: color = "red"
                            elif colors["record_accident"] == True: color = "tomato"
                            elif colors["first_aid"] == True: color = "orange"
                            elif colors["near_mis"] == True: color = "yellow"
                            elif colors["fire_mtd"] == True: color = "blue"
                            else: color = "green"
                        target_element.set('fill', color)
                        tree.write('daily_s.svg')
            # Display the modified SVG using Streamlit
            with open('daily_s.svg', 'r') as f:
                svg = f.read()
                b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
                html = r'<img src="data:image/svg+xml;base64,%s" style="height:24rem;"/>' % b64
                st.write(f"""
                    <style>
                        .daily_d{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
                    </style>
                    <div style='position:relative; right:3rem; width:110%; top:2rem;'>{html}
                        <p class="daily_d" style='left:21rem; top:4rem; color:black;'>LEGEND:</p>
                        <p class="daily_d" style='left:21rem; top:6rem; color:red;'>RECORDABLE LOST TIME ENJURY</p>
                        <p class="daily_d" style='left:21rem; top:10rem; color:tomato;'>RECORDABLE ACCIDENT</p>
                        <p class="daily_d" style='left:21rem; top:12rem; color:orange;'>FIRST AID</p>
                        <p class="daily_d" style='left:21rem; top:14rem; color:yellow;'>NEAR MISS</p>
                        <p class="daily_d" style='left:21rem; top:16rem; color:blue;'>FIRE</p>
                        <p class="daily_d" style='left:21rem; top:18rem; color:green;'>NO INCIDENT</p>
                    </div>""", unsafe_allow_html=True)

            # tree = ET.parse('resources\S.svg')
            # root = tree.getroot()
            # for i in range(1,32):
            #     if i<10:
            #         target_element = root.find(f".//*[@id='untitled-u-day{i}']")
            #     else:
            #         target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
            #     # Change the color of the element
            #     if i == on_date.day:
            #         target_element.set('fill', color)
            #     else:
            #         target_element.set('fill', 'gray')
            #     # Save the modified SVG file
            #     tree.write('daily_s.svg')
            # # Display the modified SVG using Streamlit
            # with open('daily_s.svg', 'r') as f:
            #     svg = f.read()
            #     b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
            #     html = r'<img src="data:image/svg+xml;base64,%s" style="height:17rem;"/>' % b64
            #     st.write(f"""
            #         <style>
            #             .daily_d{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
            #         </style>
            #         <div>{html}
            #             <p class="daily_d" style='left:17rem; top:2rem; color:black;'>LEGEND:</p>
            #             <p class="daily_d" style='left:17rem; top:4rem; color:red;'>RECORDABLE LOST TIME ENJURY</p>
            #             <p class="daily_d" style='left:17rem; top:8rem; color:tomato;'>RECORDABLE ACCIDENT</p>
            #             <p class="daily_d" style='left:17rem; top:10rem; color:orange;'>FIRST AID</p>
            #             <p class="daily_d" style='left:17rem; top:12rem; color:yellow;'>NEAR MISS</p>
            #             <p class="daily_d" style='left:17rem; top:14rem; color:blue;'>FIRE</p>
            #             <p class="daily_d" style='left:17rem; top:16rem; color:green;'>NO INCIDENT</p>
            #         </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                        <style>
                            .float-container {{ padding: 5px; }}
                            .float-cat {{ width: 20%; font-size:0.7rem; float: left; height:5rem; text-align:center; padding: 0.3rem; border: 2px solid black;}}
                            .float-inc {{ width: 35%; font-size:0.7rem; float: left; height:5rem; text-align:center; padding: 1rem.5rem; border: 2px solid black;}}
                            .float-date {{ width: 15%; font-size:0.7rem; float: left; font-weight:bold; height:5rem; text-align:center; padding: 0.3rem; border: 2px solid black;}}
                            .float-loc {{ width: 18%; font-size:0.7rem; float: left; font-weight:bold; height:5rem; text-align:center; padding: 0.3rem; border: 2px solid black;}}
                            .float-med {{ width: 12%; font-size:0.7rem; float: left; font-weight:bold; height:5rem; text-align:center; padding: 0.3rem; border: 2px solid black;}}
                            .float-pact {{ width: 20%; font-size:0.7rem; float: left; height:5rem; text-align:center; padding: 0.3rem; font-weight:bold; border: 2px solid black;}}
                            .float-act {{ width: 80%; font-size:0.7rem; float: left; height:5rem; text-align:center; padding: 0.3rem; border: 2px solid black;}}
                            .heading5 {{font-size:0.7rem; font-weight:bold;}}
                            .heading6 {{font-size:0.65rem; padding-top:0.4rem}}
                            hr{{ margin:0rem; }}
                            @media (min-width: 1920px) and (max-width: 2860px) {{
                                .float-container {{ padding: 5px; }}
                                .float-cat {{ width: 15%; font-size:1.1rem; float: left; height:10rem; text-align:center; padding-top: 10px; border: 2px solid black;}}
                                .float-inc {{ width: 40%; font-size:1rem; float: left; height:10rem; text-align:center; padding: 2.5rem; border: 2px solid black;}}
                                .float-date {{ width: 15%; font-size:0.7rem; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 2px solid black;}}
                                .float-loc {{ width: 18%; font-size:0.7rem; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 2px solid black;}}
                                .float-med {{ width: 12%; font-size:0.7rem; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 2px solid black;}}
                                .float-pact {{ width: 20%; font-size:1.1rem; float: left; height:10rem; text-align:center; padding: 1rem; font-weight:bold; border: 2px solid black;}}
                                .float-act {{ width: 80%; font-size:1.1rem; float: left; height:10rem; text-align:center; padding: 2rem; border: 2px solid black;}}
                                .heading6 {{font-size:0.6rem; padding:0.5rem}}
                                .heading5 {{font-size:0.7rem; font-weight:bold;}}
                                hr{{ margin:0rem; }}
                            }}
                        </style>
                <div class="float-container">
                    <div class="float-cat" style='background-color:red; color:white; font-weight:bold;'>
                        <div class="green">Recordable Lost Time Injury, Recordable Accident (Latest)</div>
                    </div>
                    <div class="float-inc">
                        <div class="blue">{Record_lost_time.incident}</div>
                    </div>
                    <div class="float-date">
                        <div class="heading5">Time<hr>
                            <h6 class="heading6" style='padding-top:1rem;'>{Record_lost_time.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div class="heading5">Location<hr>
                            <h6 class="heading6" style='padding-top:1rem;'>{Record_lost_time.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div class="heading5">Medical<hr>
                            <h6 class="heading6" style='padding-top:1rem;'>{Record_lost_time.medical}</h6>
                        </div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pact" >
                        Preventive Measures Implemented and Lesson Learned
                    </div>
                    <div class="float-act" style='padding-top:2rem;'>
                        {Record_lost_time.action}
                    </div>
                </div>

                <div class="float-container">
                    <div class="float-cat" style='background-color:orange; font-weight:bold; padding-top:2rem;'>
                        <div class="green">First Aid (Latest)</div>
                    </div>
                    <div class="float-inc">
                        <div >{First_aid.incident}</div>
                    </div>
                    <div class="float-date">
                        <div class="heading5">Time<hr>
                            <h6 class="heading6" style='padding-top:1rem;'>{First_aid.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div class="heading5">Location<hr>
                            <h6 class="heading6" style='padding-top:1rem;'>{First_aid.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div class="heading5">Medical<hr>
                            <h6 class="heading6" style='padding-top:1rem;'>{First_aid.medical}</h6>
                        </div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pact" >
                        Preventive Measures Implemented and Lesson Learned
                    </div>
                    <div class="float-act" style='padding-top:2rem;'>
                        {First_aid.action}
                    </div>
                </div>
                        
                <div class="float-container">
                    <div class="float-cat" style='background-color:yellow; font-weight:bold; padding-top:1rem;'>
                        <div>Near_MIS <br>
                            Fire_Det
                        </div>
                    </div>
                    <div class="float-inc">
                        <p style='font-size:0.65rem;'>Near MIS: {Near_mis.incident}</p>
                        <p style='font-size:0.65rem;'>Fire Details: {Fire_mtd.incident}</p>
                    </div>
                    <div class="float-date">
                        <div class="heading5">Time<hr>
                            <h6 class="heading6">{Near_mis.time}</h6>
                            <h6 class="heading6">{Fire_mtd.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div class="heading5">Location<hr>
                            <h6 class="heading6">{Near_mis.location}</h6>
                            <h6 class="heading6">{Fire_mtd.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div class="heading5">Medical<hr>
                            <h6 class="heading6">{Near_mis.medical}</h6>
                            <h6 class="heading6">{Fire_mtd.medical}</h6>
                        </div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pact" >
                        Preventive Measures Implemented and Lesson Learned
                    </div>
                    <div class="float-act">
                        <p class="heading6">Near Mis: {Near_mis.action}</p>
                        <p class="heading6">Fire details: {Fire_mtd.action}</p>
                    </div>
                </div>
            """,unsafe_allow_html=True)
            pass
    except Exception as e:
        print("An error: ", str(e))
        pass

def unsafe_incident_tracking():
    df = fetch_data("INCIDENCES DETAILS")
    df['DATE'] = pd.to_datetime(df['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    month_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    target_data = fetch_data("SET DAILY TARGET")
    target_data = target_data[target_data["CATEGORY"] == 'Incident details']
    monthly_target = target_data[((target_data["DATE"].dt.to_period("M")) == current_month)]
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    Record_lost_time = 0
    record_accident = 0
    First_aid = 0
    Near_mis = 0
    Fire_mtd = 0
    for index, row in month_data.iterrows():
        if row["CATEGORY"] == "Recordable Loss Time Injury":
            Record_lost_time += 1
        if row["CATEGORY"] == "Recordable Accident":
            record_accident += 1
        if row["CATEGORY"] == "First Aid":
            First_aid += 1
        if row["CATEGORY"] == "Near MIS":   
            Near_mis += 1
        if row["CATEGORY"] == "Fire":
            Fire_mtd += 1
    col_indices_A, col_indices_B, col_indices_C, col_indices_D, col_indices_E = st.columns((1,1,1,1,1))
    with col_indices_A:
        st.markdown(f"""<div style='background-color:red;margin:0.4rem;padding-top:0.7rem;border:1px solid black;height:5rem;border-radius:0.7rem;font-size:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Lost Time Injury FTD:
                <h4 style='color:white;font-weight:bold; padding-top:0.5rem;'>{Record_lost_time}</h4></div>""",unsafe_allow_html=True)
    with col_indices_B:
        st.markdown(f"""<div style='background-color:tomato;margin:0.4rem;padding-top:0.7rem;border:1px solid black;height:5rem;border-radius:0.7rem;font-size:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Accident FTD:
                <h4 style='color:white;font-weight:bold; padding-top:0.5rem;'>{record_accident}</h4></div>""",unsafe_allow_html=True)
    with col_indices_C:
        st.markdown(f"""<div style='background-color:orange;margin:0.4rem;padding-top:0.7rem;border:1px solid black;height:5rem;border-radius:0.7rem;font-size:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>First Aid FTD:
                <h4 style='color:white;font-weight:bold; padding-top:0.5rem;'>{First_aid}</h4></div>""",unsafe_allow_html=True)
    with col_indices_D:
        st.markdown(f"""<div style='background-color:yellow;margin:0.4rem;padding-top:0.7rem;border:1px solid black;height:5rem;border-radius:0.7rem;font-size:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Near MIS FTD:
                <h4 style='color:white;font-weight:bold; padding-top:0.5rem;'>{Near_mis}</h4></div>""",unsafe_allow_html=True)
    with col_indices_E:
        st.markdown(f"""<div style='background-color:skyblue;margin:0.4rem;padding-top:0.7rem;border:1px solid black;height:5rem;border-radius:0.7rem;font-size:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Fire FTD:
                <h4 style='color:white;font-weight:bold; padding-top:0.5rem;'>{Fire_mtd}</h4></div>""",unsafe_allow_html=True)
    st.markdown("___")

    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:   # ****** Daily_Data ****** #
        desired_data = month_data[month_data['DATE'].dt.strftime('%U') == current_week_number]
        daily_data_count = desired_data.groupby(desired_data['DATE'].dt.to_period('D')).size().reset_index(name='data')
        desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')  # Day format in weekdays
        unique_desired_data = desired_data.drop_duplicates(subset='Day', keep='first')
        desired_trgt = monthly_target[monthly_target['DATE'].dt.strftime('%U') == current_week_number]
        desired_trgt['DATE'] = desired_trgt['DATE'].dt.strftime("%Y-%m-%d")
        daily_data_count['DATE'] = daily_data_count['DATE'].dt.strftime("%Y-%m-%d") # Convert 'DATE' to a string in both DataFrames for merging
        merged_data = pd.merge(daily_data_count, desired_trgt, on='DATE')  # Merge on the 'DATE' column
        merged_data['color'] = np.where(merged_data['data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(unique_desired_data['Day'], merged_data['data'], merged_data['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='count', line=dict(color=my_color, width=30), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=unique_desired_data['Day'], y=merged_data['VALUE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)
    with cl2:   # ****** Weekly_Data ****** #
        weekly_data = month_data.groupby(month_data['DATE'].dt.to_period('W')).size()
        weekly_trgt = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum()
        weekly_data = pd.DataFrame({'my_data': weekly_data})
        merged_data = pd.merge(weekly_data, weekly_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        fig = go.Figure(data=[
            go.Bar(
                x=list(weekly_data['WEEKLY_NUMBER']),  # Convert range to list
                y=merged_data['my_data'],
                marker_color=[color for color in merged_data['color']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    with cl3:   # ****** Monthly_Data ****** #
        monthly_data = df.groupby(df['DATE'].dt.to_period('M')).size()
        monthly_target = target_data.groupby(target_data['DATE'].dt.to_period('M'))['VALUE'].sum()
        monthly_data = pd.DataFrame({'my_data': monthly_data})
        merged_data = pd.merge(monthly_data, monthly_target, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        monthly_data.index = monthly_data.index.strftime('%b')
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=merged_data['my_data'], marker_color=[color for color in merged_data['color']],)])
        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
        pass
    
    # **********************
    current_month_data = month_data
    st.subheader("Get data acording to the status")
    col1,col2,col3,col4 = st.tabs(['Clear',':red[Open Status]',':green[Close Status]',':orange[Inprocessing]'])
    with col1:
        st.write("Please choose option for showing data!")
    with col2:
        open_data = current_month_data[current_month_data["STATUS"] == "Open"]
        st.table(open_data[["DATE", "TIME", "CATEGORY", "VALUE STREAM", "EVENT", "ACTION", "STATUS"]])
    with col3:
        close_data = current_month_data[current_month_data["STATUS"] == "Closed"]
        st.table(close_data[["DATE", "TIME", "CATEGORY", "VALUE STREAM", "EVENT", "ACTION", "STATUS"]])
    with col4:
        inprocessing = current_month_data[current_month_data["STATUS"] == "Inprocess"]
        st.table(inprocessing[["DATE", "TIME", "CATEGORY", "VALUE STREAM", "EVENT", "ACTION", "STATUS"]])
    
def unsafe_practice_tracking():
    df = fetch_data("UNSAFE PRACTICES TRACKING")
    df['DATE'] = pd.to_datetime(df['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    month_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    target_data = fetch_data("SET DAILY TARGET")
    target_data = target_data[target_data["CATEGORY"] == 'Incident Practices']
    monthly_target = target_data[((target_data["DATE"].dt.to_period("M")) == current_month)]
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')

    closed = 0
    for item in month_data['STATUS']:
        if item == 'Closed':
            closed +=1
    col_indices_1, col_indices_2, col_indices_3 = st.columns((0.5, 2, 0.5))
    with col_indices_2:
        col_indices_A, col_indices_B, col_indices_C = st.columns((2, 2, 2))
        with col_indices_A:
            st.markdown(f"""<div class="custom" style='background-color:#f53527; text-align:center; font-size:1rem; border:1px solid black; border-radius:25px; font-weight:bold; padding:10px;'>Unsafe Practices
                        <h3 style='color:white;'>{len(month_data)}</h3></div>""",unsafe_allow_html=True)
            # st.metric(":blue[Unsafe Practices]", len(df))
        with col_indices_B:
            st.markdown(f"""<div class="custom" style='background-color:#4be373; text-align:center; font-size:1rem; border:1px solid black; border-radius:25px; font-weight:bold; padding:10px;'>Unsafe Practices Closed
                        <h3 style='color:white;'>{closed}</h3></div>""",unsafe_allow_html=True)
            # st.metric("Unsafe Practices Closed", closed)
        with col_indices_C:
            if len(month_data) == 0:
                closer_data = 0 
            else:
                closer_data = round((closed / len(month_data))*100)
            st.markdown(f"""<div class="custom" style='background-color:#4be373; text-align:center; font-size:1rem; border:1px solid black; border-radius:25px; font-weight:bold; padding:10px;'>Closure Percentage
                        <h3 style='color:white;'>{closer_data}%</h3></div>""",unsafe_allow_html=True)

    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:   # ****** Daily_Data ****** #
        desired_data = month_data[month_data['DATE'].dt.strftime('%U') == current_week_number]
        daily_data_count = desired_data.groupby(desired_data['DATE'].dt.to_period('D')).size().reset_index(name='data')
        desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')  # Day format in weekdays
        unique_desired_data = desired_data.drop_duplicates(subset='Day', keep='first')
        desired_trgt = monthly_target[monthly_target['DATE'].dt.strftime('%U') == current_week_number]
        desired_trgt['DATE'] = desired_trgt['DATE'].dt.strftime("%Y-%m-%d")
        daily_data_count['DATE'] = daily_data_count['DATE'].dt.strftime("%Y-%m-%d") # Convert 'DATE' to a string in both DataFrames for merging
        merged_data = pd.merge(daily_data_count, desired_trgt, on='DATE')  # Merge on the 'DATE' column
        merged_data['color'] = np.where(merged_data['data'] >= merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(unique_desired_data['Day'], merged_data['data'], merged_data['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='count', line=dict(color=my_color, width=30), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=unique_desired_data['Day'], y=merged_data['VALUE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)
    with cl2:   # ****** Weekly_Data ****** #
        weekly_data = month_data.groupby(month_data['DATE'].dt.to_period('W')).size()
        weekly_trgt = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum()
        weekly_data = pd.DataFrame({'my_data': weekly_data})
        merged_data = pd.merge(weekly_data, weekly_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        fig = go.Figure(data=[
            go.Bar(
                x=list(weekly_data['WEEKLY_NUMBER']),  # Convert range to list
                y=merged_data['my_data'],
                marker_color=[color for color in merged_data['color']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    with cl3:   # ****** Monthly_Data ****** #
        monthly_data = df.groupby(df['DATE'].dt.to_period('M')).size()
        monthly_target = target_data.groupby(target_data['DATE'].dt.to_period('M'))['VALUE'].sum()
        monthly_data = pd.DataFrame({'my_data': monthly_data})
        merged_data = pd.merge(monthly_data, monthly_target, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        monthly_data.index = monthly_data.index.strftime('%b')
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=merged_data['my_data'], marker_color=[color for color in merged_data['color']],)])
        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
        pass
    
    current_month_data = month_data
    st.subheader("Get data acording to the status")
    col1,col2,col3,col4 = st.tabs(['Clear',':red[Open Status]',':green[Close Status]',':orange[Inprocessing]'])
    with col1:
        st.write("Please choose option for showing data!")
    with col2:
        open_data = current_month_data[current_month_data["STATUS"] == "Open"]
        st.table(open_data[["DATE", "EVENT", "VALUE STREAM", "RESPONSIBILITY", "TARGET DATE", "STATUS"]])
    with col3:
        close_data = current_month_data[current_month_data["STATUS"] == "Closed"]
        st.table(close_data[["DATE", "EVENT", "VALUE STREAM", "RESPONSIBILITY", "TARGET DATE", "STATUS"]])
    with col4:
        inprocessing = current_month_data[current_month_data["STATUS"] == "Inprocess"]
        st.table(inprocessing[["DATE", "EVENT", "VALUE STREAM", "RESPONSIBILITY", "TARGET DATE", "STATUS"]])

#************************** Safety_FTD End **************************#


#************************** Cost_FTD Start **************************#
def cost_ftd():
    #******** Productivity and OEE Section ********#
    rows = fetch_data("PRODUCTIVITY AND OEE")
    issue_data = fetch_data("COST ISSUE")
    hp_issue = []
    oee_issue = []
    hp_max = 3
    oee_max = 3
    hp_issues = issue_data[(issue_data["DATE"] == f"{on_date}") & (issue_data["CATEGORY"] == "HUMAN PRODUCTIVITY")]
    oee_issues = issue_data[(issue_data["DATE"] == f"{on_date}") & (issue_data["CATEGORY"] == "PLANT AGGREGATE OEE")]
    hp_length = len(hp_issues)
    oee_length = len(oee_issues)
    for index, row in hp_issues.iterrows():
        issue = {
            "issue": row["ISSUE"],
            "raise_date": row["RAISE DATE"],
            "target_date": row["TARGET DATE"],
            "responsibility": row["RESPONSIBILITY"],
            "action": row["ACTION"],
            "status": row["STATUS"]
        }
        hp_issue.append(issue)
        pass
    while hp_length < hp_max:
        dummy_issue = {
            "issue": "N/A",
            "raise_date": "N/A",
            "target_date": "N/A",
            "responsibility": "N/A",
            "action": "N/A",
            "status": "N/A"
        }
        hp_issue.append(dummy_issue)
        hp_max = hp_max-1
    
    for index, row in oee_issues.iterrows():
        issue = {
            "issue": row["ISSUE"],
            "raise_date": row["RAISE DATE"],
            "target_date": row["TARGET DATE"],
            "responsibility": row["RESPONSIBILITY"],
            "action": row["ACTION"],
            "status": row["STATUS"]
        }
        oee_issue.append(issue)
        pass
    while oee_length < oee_max:
        dummy_issue = {
            "issue": "N/A",
            "raise_date": "N/A",
            "target_date": "N/A",
            "responsibility": "N/A",
            "action": "N/A",
            "status": "N/A"
        }
        oee_issue.append(dummy_issue)
        oee_max = oee_max-1

    human_productivity = cmp(0,0)
    plant_agrigate = cmp(0,0)
    for index, row in rows.iterrows():
        date = pd.Timestamp(row["DATE"]).strftime('%Y-%m-%d')
        if date == f"{on_date}":
            if row["CATEGORY"] == "HUMAN PRODUCTIVITY":
                human_productivity = cmp(row["TARGET"], row["ACTUAL"])
            elif row["CATEGORY"] == "PLANT AGGREGATE OEE":
                plant_agrigate = cmp(row["TARGET"], row["ACTUAL"])
    # st.subheader(f"Status as on: {on_date}",divider="gray")
    st.markdown(f"""
            <div>
                <h3 style='position:absolute; bottom:0rem;'>Status as on: {on_date}</h3>
            </div>
            <hr>
        """, unsafe_allow_html=True)
        
    col1,col2=st.columns((1,1.7))
    with col1:  #Dynamic C letter

        tree = ET.parse('resources\C.svg')
        root = tree.getroot()
        current_date = datetime.date.today()
        total_days = (current_date.day)
        row_data = fetch_month_data("PRODUCTIVITY AND OEE")
        first_day_of_month = current_date.replace(day=1)
        days_to_add = 0
        for i in range(1, 32):
            if i < 10:
                target_element = root.find(f".//*[@id='untitled-u-day{i}']")
            else:
                target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
            # st.write(days_to_add)
            new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
            days_to_add += 1
            if len(row_data) == 0:
                if new_date.weekday() == 6:
                    target_element.set('fill', 'blue')
                    tree.write('c.svg')
                else:
                    target_element.set('fill', '#d2dbed')
                    tree.write('c.svg')
            else:
                df = row_data[row_data["DATE"] == f"{new_date}"]
                filter_data = df[df["CATEGORY"] == "HUMAN PRODUCTIVITY"]
                oe_target = filter_data["TARGET"]
                oe_actual = filter_data["ACTUAL"]
                comparison = np.where(oe_target > oe_actual, '#fa3232', '#4cf02b')
                if new_date.weekday() == 6: target_element.set('fill', '#2f52ed')
                else:
                    for result in comparison:
                        color = result
                        target_element.set('fill', color)
                    tree.write('daily_c.svg')
        # Display the modified SVG using Streamlit
        with open('daily_c.svg', 'r') as f:
            svg = f.read()
            b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
            html = r'<img src="data:image/svg+xml;base64,%s" style="height:20rem;"/>' % b64
            st.write(f"""
                <style>
                    .daily_c{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
                </style>
                <div>{html}
                    <p class="daily_c" style='left:20rem; top:4rem; color:black;'>LEGEND:</p>
                    <p class="daily_c" style='left:20rem; top:6.5rem; color:#4cf02b;'>TARGET ACHIEVED</p>
                    <p class="daily_c" style='left:20rem; top:9rem; color:#fa3232;'>TARGET MISSED</p>
                    <p class="daily_c" style='left:20rem; top:11.5rem; color:#2f52ed;'>PLANT OFF</p>
                </div>""", unsafe_allow_html=True)


        # tree = ET.parse('resources\C.svg')
        # root = tree.getroot()
        # current_date = datetime.date.today()
        # total_days = (current_date.day)
        # row_data = fetch_data("PRODUCTIVITY AND OEE")
        # daily_data = row_data[row_data["DATE"] == f"{on_date}"]
        # filter_data = daily_data[daily_data["CATEGORY"] == "HUMAN PRODUCTIVITY"]
        # oe_target = filter_data["TARGET"]
        # oe_actual = filter_data["ACTUAL"]
        # comparison = np.where(oe_target > oe_actual, 0, 1)
        # color = 'gray'
        # if on_date.weekday() == 6: color = 'blue'
        # else:
        #     for result in comparison:
        #         color='red' if result == 0 else 'green'
        #         # target_element.set('fill', color)
        # for i in range(1,32):
        #     if i<10:
        #         target_element = root.find(f".//*[@id='untitled-u-day{i}']")
        #     else:
        #         target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
        #     # Change the color of the element
        #     if i == on_date.day:
        #         target_element.set('fill', color)
        #     else:
        #         target_element.set('fill', 'gray')
        #     # Save the modified SVG file
        #     tree.write('daily_c.svg')
        # # Display the modified SVG using Streamlit
        # with open('daily_c.svg', 'r') as f:
        #     svg = f.read()
        #     b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        #     html = r'<img src="data:image/svg+xml;base64,%s" style="height:17rem;"/>' % b64
        #     st.write(f"""
        #         <style>
        #             .daily_c{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
        #         </style>
        #         <div>{html}
        #             <p class="daily_c" style='left:20rem; top:7rem; color:black;'>LEGEND:</p>
        #             <p class="daily_c" style='left:20rem; top:8.5rem; color:green;'>TARGET ACHIEVED</p>
        #             <p class="daily_c" style='left:20rem; top:10rem; color:red;'>TARGET MISSED</p>
        #             <p class="daily_c" style='left:20rem; top:11.5rem; color:blue;'>PLANT OFF</p>
        #         </div>""", unsafe_allow_html=True)
    with col2:
        # st.subheader("PRODUCTIVITY AND OEE")
        blk1,blk2=st.columns((1,1))
        with blk1:  #Actual vs Target
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HUMAN PRODUCTIVITY<hr style='margin:0em;'>
                            <div style='content: "";height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{human_productivity.target}</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{human_productivity.actual}</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>PLANT AGGREGATE OEE<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{plant_agrigate.target}</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{plant_agrigate.actual}</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
        with blk2:  #Top Issues
            st.markdown(f"""
                <style>
                        .float-container {{  padding: 5px;   }}
                        .float-bd1 {{width: 100%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:9rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                        }}
                        .par {{padding-top:0.2rem; line-height:0.05rem; font-size:0.7rem; color:black; }}
                        hr{{ margin:0em; }}
                </style>
                <div class="float-container">
                    <div class="float-bd1">Top 3 Productivity Problems<hr style='margin:0.6rem 0rem;'>
                            <p class="par">{hp_issue[0]["issue"]}</p>
                            <p class="par">{hp_issue[1]["issue"]}</p>
                            <p class="par">{hp_issue[2]["issue"]}</p>
                    </div>
                </div>
            """,unsafe_allow_html=True)
            st.markdown(f"""
                <div class="float-container">
                    <div class="float-bd1">Top 3 OEE Related Problems<hr style='margin:0.6rem 0rem;'>
                        <p class="par">{oee_issue[0]["issue"]}</p>
                        <p class="par">{oee_issue[1]["issue"]}</p>
                        <p class="par">{oee_issue[2]["issue"]}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
    #******** Machine Breakdown TIme Section ********#
    breakdown = fetch_data("MACHINE BREAKDOWN TIME")
    breakdown_issue = []
    breakdown = breakdown[(breakdown["DATE"] == f"{on_date}")]
    length = len(breakdown)
    max_bd_issues =  4
    for index, row in breakdown.iterrows():
        issue = {
            "line": row["LINE"],
            "machine": row["MACHINE"],
            "bd_time": row["B/D TIME"],
            "issue": row["ISSUE"],
            "action": row["ACTION"],
            "status": row["STATUS"],
            "del_fail": row["DELIVERY FAILURE"]
        }
        breakdown_issue.append(issue)
        pass
    while length < max_bd_issues:
        dummy_issue = {
            "line": "N/A",
            "machine": "N/A",
            "bd_time": "N/A",
            "issue": "N/A",
            "action": "N/A",
            "status": "N/A",
            "del_fail": "N/A"
        }
        breakdown_issue.append(dummy_issue)
        max_bd_issues = max_bd_issues-1

    # st.table(raw1)
    # st.subheader("MACHINE BREAKDOWN TIME")
    st.markdown(F"""
        <style>
                .float-container {{  padding: 5px;   }}
                .float-ln {{width: 8%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}}
                .float-icp {{width: 24%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .float-msd {{width: 12%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .float-ln1 {{width: 8%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}}
                .float-icp1 {{width: 24%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .float-msd1 {{width: 12%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .par {{padding-top:1rem; font-size:0.7rem; color:black; }}
                hr{{ margin:0em; }}
        </style>
        <div class="float-container">
            <div class="float-ln">Line</div><div class="float-msd">Machine</div>
            <div class="float-ln">B/D Time</div><div class="float-icp">Issue</div>
            <div class="float-icp">Action Points</div><div class="float-msd">Status</div>
            <div class="float-msd">Delivery Failure</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[0]["line"]}</div><div class="float-msd1">{breakdown_issue[0]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[0]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[0]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[0]["action"]}</div><div class="float-msd1">{breakdown_issue[0]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[0]["del_fail"]}</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[1]["line"]}</div><div class="float-msd1">{breakdown_issue[1]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[1]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[1]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[1]["action"]}</div><div class="float-msd1">{breakdown_issue[1]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[1]["del_fail"]}</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[2]["line"]}</div><div class="float-msd1">{breakdown_issue[2]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[2]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[2]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[2]["action"]}</div><div class="float-msd1">{breakdown_issue[2]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[2]["del_fail"]}</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[3]["line"]}</div><div class="float-msd1">{breakdown_issue[3]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[3]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[3]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[3]["action"]}</div><div class="float-msd1">{breakdown_issue[3]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[3]["del_fail"]}</div>
        </div>
    """,unsafe_allow_html=True)

    #******** RAW Material Section ********#
    # material_data = fetch_month_data("RAW MATERIAL PDI")
    # material_a = material_data[(material_data["DATE"] == f"{on_date}") & (material_data["CATEGORY"] == "A")]
    # material_b = material_data[(material_data["DATE"] == f"{on_date}") & (material_data["CATEGORY"] == "B")]
    # material_c = material_data[(material_data["DATE"] == f"{on_date}") & (material_data["CATEGORY"] == "C")]
    # len_a = len(material_a)
    # len_b = len(material_b)
    # len_c = len(material_c)
    # mat_a = []
    # mat_b = []
    # mat_c = []
    # max_a = 1
    # max_b = 1
    # max_c = 1
    # for index, row in material_a.iterrows():
    #     issue = { "PART_NO": row["PART NO"], "VALUE_MINR": row["VALUE_MINR"], "ACTUAL_VALUE": row["ACTUAL VALUE_MINR"], "PDI": row["PDI"] }
    #     mat_a.append(issue)
    # while len_a < max_a:
    #     dummy_issue = { "PART_NO": "N/A", "VALUE_MINR": "N/A", "ACTUAL_VALUE": "N/A", "PDI": "N/A" }
    #     mat_a.append(dummy_issue)
    #     max_a = max_a-1
    
    # for index, row in material_b.iterrows():
    #     issue = { "PART_NO": row["PART NO"], "VALUE_MINR": row["VALUE_MINR"], "ACTUAL_VALUE": row["ACTUAL VALUE_MINR"], "PDI": row["PDI"] }
    #     mat_b.append(issue)
    # while len_b < max_b:
    #     dummy_issue = { "PART_NO": "N/A", "VALUE_MINR": "N/A", "ACTUAL_VALUE": "N/A", "PDI": "N/A" }
    #     mat_b.append(dummy_issue)
    #     max_b = max_b-1

    # for index, row in material_c.iterrows():
    #     issue = { "PART_NO": row["PART NO"], "VALUE_MINR": row["VALUE_MINR"], "ACTUAL_VALUE": row["ACTUAL VALUE_MINR"], "PDI": row["PDI"] }
    #     mat_c.append(issue)
    # while len_c < max_c:
    #     dummy_issue = { "PART_NO": "N/A", "VALUE_MINR": "N/A", "ACTUAL_VALUE": "N/A", "PDI": "N/A" }
    #     mat_c.append(dummy_issue)
    #     max_c = max_c-1

    # st.subheader("RAW MATERIAL P.D.I.")
    # col1,col2=st.columns((3,1))
    # with col1:
    #     st.markdown(f"""
    #             <style>
    #                 .float-container {{  padding: 5px;   }}
    #                 .float-nop {{width: 20%; font-weight:bold; font-size:1rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.7rem; line-height:1rem; border: 1px solid black;}}
    #                 .float-ct1 {{width: 20%; font-weight:bold; font-size:3rem; float: left; height:4.5rem; text-align:center; padding-top: 0rem; border: 1px solid black;}}
    #                 .float-nop1 {{width: 20%; font-size:0.7rem; float: left; word-wrap:break-word; height:4.5rem; text-align:center; padding: 2rem; line-height:1rem; border: 1px solid black;}}
    #                 .float-prb1 {{width: 30%; font-size:0.7rem; float: left; word-wrap:break-word; height:4.5rem; text-align:center; padding: 2rem; line-height:1rem; border: 1px solid black;}}
    #                 hr{{ margin:0em; }}
    #             </style>
    #             <div class="float-container">
    #                 <div class="float-nop">Category</div><div class="float-nop">No of Parts</div>
    #                 <div class="float-nop">Value (MINR)</div><div class="float-nop">Actual Value (MINR)</div>
    #                 <div class="float-nop">P.D.I.</div>
    #             </div>
    #             <div class="float-container">
    #                 <div class="float-ct1">A</div><div class="float-nop1">{mat_a[0]["PART_NO"]}</div>
    #                 <div class="float-nop1">{mat_a[0]["VALUE_MINR"]}</div><div class="float-nop1">{mat_a[0]["ACTUAL_VALUE"]}</div>
    #                 <div class="float-nop1">{mat_a[0]["PDI"]}</div>
    #             </div>
    #             <div class="float-container">
    #                 <div class="float-ct1">B</div><div class="float-nop1">{mat_b[0]["PART_NO"]}</div>
    #                 <div class="float-nop1">{mat_b[0]["VALUE_MINR"]}</div><div class="float-nop1">{mat_b[0]["ACTUAL_VALUE"]}</div>
    #                 <div class="float-nop1">{mat_b[0]["PDI"]}</div>
    #             </div>
    #             <div class="float-container">
    #                 <div class="float-ct1">C</div><div class="float-nop1">{mat_c[0]["PART_NO"]}</div>
    #                 <div class="float-nop1">{mat_c[0]["VALUE_MINR"]}</div><div class="float-nop1">{mat_c[0]["ACTUAL_VALUE"]}</div>
    #                 <div class="float-nop1">{mat_c[0]["PDI"]}</div>
    #             </div>
    #         """,unsafe_allow_html=True)
    # with col2:
    #     st.markdown(f"""
    #         <style>
    #             .float-container {{  padding: 5px;   }}
    #             .float-prb {{width: 100%; font-weight:bold; font-size:1rem; float: left; height:16.5rem; text-align:center; padding: 0.7rem; line-height:1rem; border: 1px solid black;}}    
    #             .float-prb p{{padding-top:1rem; color:black; }}
    #         </style>
    #         <div class="float-container">
    #             <div class="float-prb">Top 3 Problems <hr style='padding:0.5rem 0rem;'>
    #                 <p>prblm</p>
    #                 <p>prblm</p>
    #                 <p>prblm</p>
    #             </div>
    #         </div>
    #     """,unsafe_allow_html=True)

def productivity_oee():
    current_date()
    oee_data = fetch_month_data("PRODUCTIVITY AND OEE")
    hp_month_actual = oee_data[(oee_data["CATEGORY"] == "HUMAN PRODUCTIVITY")]["ACTUAL"].sum()
    hp_month_target = oee_data[(oee_data["CATEGORY"] == "HUMAN PRODUCTIVITY")]["TARGET"].sum()
    plant_month_actual = oee_data[(oee_data["CATEGORY"] == "PLANT AGGREGATE OEE")]["ACTUAL"].sum()
    plant_month_target = oee_data[(oee_data["CATEGORY"] == "PLANT AGGREGATE OEE")]["TARGET"].sum()
    blk1,blk2=st.columns((1,1))
    with blk1:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HUMAN PRODUCTIVITY<hr>
                            <div style='content: ""; height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{hp_month_target}</h6>
                                </div>
                                    <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{hp_month_actual}</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>PLANT AGGREGATE OEE<hr>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{plant_month_target}</h6>
                                </div>
                                    <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{plant_month_actual}</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    
    issues = fetch_month_data("COST ISSUE")
    hp_issue = issues[issues["CATEGORY"] == "HUMAN PRODUCTIVITY"]
    plant_issue = issues[issues["CATEGORY"] == "PLANT AGGREGATE OEE"]
    hp_len = len(hp_issue)
    plant_len = len(plant_issue)
    hp_event = []
    plant_event = []
    max_hp = 3
    max_plant = 3
    for index, row in hp_issue.iterrows():
        issue = row["ISSUE"]
        hp_event.append(issue)
    while hp_len < max_hp:
        dummy_issue = "N/A"
        hp_event.append(dummy_issue)
        max_hp = max_hp-1
        print(max_hp)
    for index, row in plant_issue.iterrows():
        issue = row["ISSUE"]
        plant_event.append(issue)
    while plant_len < max_plant:
        dummy_issue = "N/A"
        plant_event.append(dummy_issue)
        max_plant = max_plant-1
    with blk2:
        st.markdown(f"""
            <style>
                .float-container {{  padding: 5px;   }}
                .float-bd1 {{width: 100%; font-weight:bold; font-size:1rem; float: left; word-wrap:break-word; height:9rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                }}
                .float-hd1 {{width: 100%; font-size:1rem; color:black; float: left; word-wrap:break-word; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                }}
                .par {{padding-top:0.5rem; line-height:0.1rem; font-size:0.7rem; color:black; }}
                hr{{ margin:0em; }}
            </style>
            <div class="float-container">
                <div class="float-bd1">Top 3 Productivity Problems<hr style='margin:0.6rem 0rem;'>
                    <p class="par">{hp_event[0]}</p>
                    <p class="par">{hp_event[0]}</p>
                    <p class="par">{hp_event[0]}</p>
                </div>
            </div>
        """,unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="float-container">
                <div class="float-bd1">Top 3 OEE Related Problems<hr style='margin:0.6rem 0rem;'>
                    <p class="par">{plant_event[0]}</p>
                    <p class="par">{plant_event[0]}</p>
                    <p class="par">{plant_event[0]}</p>
                </div>
            </div>
        """,unsafe_allow_html=True)
    
    # st.subheader("Productivity and OEE Trend")
    current_month = pd.Timestamp('now').to_period('M')
    d_data = fetch_data("PRODUCTIVITY AND OEE")
    hp_data = d_data[d_data['DATE'].dt.to_period('M') == current_month]
    human_data = hp_data[hp_data["CATEGORY"] == "HUMAN PRODUCTIVITY"]
    plant_data = hp_data[hp_data["CATEGORY"] == "PLANT AGGREGATE OEE"]
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    st.subheader("Human Productivity")
    col1,col2,col3 = st.columns((1,1,1))
    with col1:  # ****** Daily_Data ****** #
        # st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data.index = daily_data.index.strftime('%a') 
        # st.bar_chart(daily_data, color=["#fa2323","#5fe650"])

        desired_data = human_data[human_data['DATE'].dt.strftime('%U') == current_week_number]
        desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = desired_data[(desired_data['DATE'] >= start_of_week) & (desired_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=40), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)
        pass

    with col2:  # ****** Weekly_Data ****** #
        # st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Weekly Trend</center>""",unsafe_allow_html=True)
        # weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])
        weekly_data = human_data.groupby(human_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:  # ****** Monthly_Data ****** #
        # st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Yearly Trend</center>""",unsafe_allow_html=True)
        # hp_data_month = d_data[d_data['CATEGORY'] == 'HUMAN PRODUCTIVITY']
        # monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'HUMAN PRODUCTIVITY']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Plant Aggregate OEE")
    col1,col2,col3 = st.columns((1,1,1))
    with col1:  # ****** Daily_Data ****** #
        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data.index = daily_data.index.strftime('%a') 
        # st.bar_chart(daily_data, color=["#fa2323","#5fe650"]
        hp_data = plant_data[plant_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=40), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)
        pass
    
    with col2:  # ****** Weekly_Data ****** #
        # weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])
        weekly_data = plant_data.groupby(plant_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:  # ****** Monthly_Data ****** #
        # hp_data_month = d_data[d_data['CATEGORY'] == 'PLANT AGGREGATE OEE']
        # monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])
        hp_data_month = d_data[d_data['CATEGORY'] == 'PLANT AGGREGATE OEE']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Get data acording to the status")
    col1,col2,col3,col4 = st.tabs(['Clear',':red[Open Status]',':green[Close Status]',':orange[Inprocessing]'])
    with col1:
        st.write("Please choose option for showing data!")
    with col2:
        open_data = issues
        open_data = open_data[open_data["STATUS"] == "Open"]
        st.table(open_data[["DATE", "CATEGORY", "ISSUE", "RAISE DATE", "TARGET DATE", "RESPONSIBILITY", "ACTION", "STATUS"]])
    with col3:
        close_data = issues
        close_data = close_data[close_data["STATUS"] == "Closed"]
        st.table(close_data[["DATE", "CATEGORY", "ISSUE", "RAISE DATE", "TARGET DATE", "RESPONSIBILITY", "ACTION", "STATUS"]])
    with col4:
        inprocessing = issues
        inprocessing = inprocessing[inprocessing["STATUS"] == "Inprocess"]
        st.table(inprocessing[["DATE", "CATEGORY", "ISSUE", "RAISE DATE", "TARGET DATE", "RESPONSIBILITY", "ACTION", "STATUS"]])
    
def mach_break_time():
    breakdown = fetch_month_data("MACHINE BREAKDOWN TIME")
    breakdown_issue = []
    length = len(breakdown)
    max_bd_issues =  4
    for index, row in breakdown.iterrows():
        issue = {
            "line": row["LINE"],
            "machine": row["MACHINE"],
            "bd_time": row["B/D TIME"],
            "issue": row["ISSUE"],
            "action": row["ACTION"],
            "status": row["STATUS"],
            "del_fail": row["DELIVERY FAILURE"]
        }
        breakdown_issue.append(issue)
        pass
    while length < max_bd_issues:
        dummy_issue = {
            "line": "N/A",
            "machine": "N/A",
            "bd_time": "N/A",
            "issue": "N/A",
            "action": "N/A",
            "status": "N/A",
            "del_fail": "N/A"
        }
        breakdown_issue.append(dummy_issue)
        max_bd_issues = max_bd_issues-1
    st.markdown(F"""
        <style>
                .float-container {{  padding: 5px;   }}
                .float-ln {{width: 8%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}}
                .float-icp {{width: 24%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .float-msd {{width: 12%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .float-ln1 {{width: 8%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}}
                .float-icp1 {{width: 24%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .float-msd1 {{width: 12%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}}
                .par {{padding-top:1rem; font-size:0.7rem; color:black; }}
                hr{{ margin:0em; }}
        </style>
        <div class="float-container">
            <div class="float-ln">Line</div><div class="float-msd">Machine</div>
            <div class="float-ln">B/D Time</div><div class="float-icp">Issue</div>
            <div class="float-icp">Action Points</div><div class="float-msd">Status</div>
            <div class="float-msd">Delivery Failure</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[0]["line"]}</div><div class="float-msd1">{breakdown_issue[0]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[0]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[0]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[0]["action"]}</div><div class="float-msd1">{breakdown_issue[0]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[0]["del_fail"]}</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[1]["line"]}</div><div class="float-msd1">{breakdown_issue[1]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[1]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[1]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[1]["action"]}</div><div class="float-msd1">{breakdown_issue[1]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[1]["del_fail"]}</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[2]["line"]}</div><div class="float-msd1">{breakdown_issue[2]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[2]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[2]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[2]["action"]}</div><div class="float-msd1">{breakdown_issue[2]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[2]["del_fail"]}</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">{breakdown_issue[3]["line"]}</div><div class="float-msd1">{breakdown_issue[3]["machine"]}</div>
            <div class="float-ln1">{breakdown_issue[3]["bd_time"]}</div><div class="float-icp1">{breakdown_issue[3]["issue"]}</div>
            <div class="float-icp1">{breakdown_issue[3]["action"]}</div><div class="float-msd1">{breakdown_issue[3]["status"]}</div>
            <div class="float-msd1">{breakdown_issue[3]["del_fail"]}</div>
        </div>
    """,unsafe_allow_html=True)

    df = fetch_data("MACHINE BREAKDOWN TIME")
    df['DATE'] = pd.to_datetime(df['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    month_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    target_data = fetch_data("SET DAILY TARGET")
    target_data = target_data[target_data["CATEGORY"] == 'Machine Breakdown Time']
    monthly_target = target_data[((target_data["DATE"].dt.to_period("M")) == current_month)]
    st.subheader("FTP Trend")
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:   # ****** Daily_Data ****** #
        # st.markdown("")
        # st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.7rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
        desired_data = month_data[month_data['DATE'].dt.strftime('%U') == current_week_number] #Data of current week
        desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')    #Day format in weekdays
        desired_trgt = monthly_target[monthly_target['DATE'].dt.strftime('%U') == current_week_number] #Target data of current week
        merged_data = pd.merge(desired_data, desired_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['B/D TIME'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        # st.write(merged_data)
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(merged_data['Day'], merged_data['B/D TIME'], merged_data['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='BD Time', line=dict(color=my_color, width=30), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=merged_data['Day'], y=merged_data['VALUE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Time (min)')
        st.plotly_chart(fig, use_container_width=True)

    with cl2:   # ****** Weekly_Data ****** #
        weekly_data = month_data.groupby(month_data['DATE'].dt.to_period('W'))['B/D TIME'].sum()
        weekly_trgt = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum()
        merged_data = pd.merge(weekly_data, weekly_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['B/D TIME'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        fig = go.Figure(data=[
            go.Bar(
                x=list(weekly_data['WEEKLY_NUMBER']),  # Convert range to list
                y=merged_data['B/D TIME'],
                marker_color=[color for color in merged_data['color']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

    with cl3:   # ****** Monthly_Data ****** #
        monthly_data = df.groupby(df['DATE'].dt.to_period('M'))['B/D TIME'].sum()
        monthly_target = target_data.groupby(target_data['DATE'].dt.to_period('M'))['VALUE'].sum()
        merged_data = pd.merge(monthly_data, monthly_target, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['B/D TIME'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        monthly_data.index = monthly_data.index.strftime('%b')
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=merged_data['B/D TIME'], marker_color=[color for color in merged_data['color']],)])
        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

#************************** Cost_FTD End **************************#


#************************** Delivery_FTD Start **************************#
class cmp():
    def __init__(self, target, actual):
        self.target = target
        self.actual = actual
    def show(self):
        return f"Target was {self.target}% and achived {self.actual}%"
     
def delivery_ftd():
    oe = cmp(0,0)
    aftermarket = cmp(0,0)
    oe_spares = cmp(0,0)
    export = cmp(0,0)
    msil = cmp(0,0)
    honda = cmp(0,0)
    gm = cmp(0,0)
    hd = cmp(0,0)
    rnaipl = cmp(0,0)
    ford = cmp(0,0)
    d_data = fetch_data("OTIF_CC PDI")
    for index, row in d_data.iterrows():
        date = pd.Timestamp(row["DATE"]).strftime('%Y-%m-%d')
        if date == f"{on_date}":
            if row["CATEGORY"] == "OE":
                oe = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "AfterMarket":
                aftermarket = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "OE_Spare":
                oe_spares = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "Export":
                export = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "MSIL":
                msil = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "Honda":
                honda = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "GM":
                gm = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "HD":
                hd = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "RNAIPL":
                rnaipl = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "Ford":
                ford = cmp(row["TARGET"], row["ACTUAL"])
            pass

    # st.subheader(f"Status as on: {on_date}", divider="gray")
    st.markdown(f"""
            <div>
                <h3 style='position:absolute; bottom:0rem;'>Status as on: {on_date}</h3>
            </div>
            <hr>
        """, unsafe_allow_html=True)
        
    col1,col2=st.columns((1,1.9))
    with col1:  #Dynamic D letter

        tree = ET.parse('resources\D.svg')
        root = tree.getroot()
        current_date = datetime.date.today()
        # total_days = (current_date.day)
        row_data = fetch_month_data("OTIF_CC PDI")
        first_day_of_month = current_date.replace(day=1)
        days_to_add = 0
        for i in range(1, 32):
            if i < 10:
                target_element = root.find(f".//*[@id='d-u-day{i}']")
            else:
                target_element = root.find(f".//*[@id='d-u-day{i}_']")
            new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
            days_to_add += 1
            if len(row_data) == 0:
                if new_date.weekday() == 6:
                    target_element.set('fill', 'blue')
                    tree.write('d.svg')
                else:
                    target_element.set('fill', '#d2dbed')
                    tree.write('d.svg')
            else:
                df = row_data[row_data["DATE"] == f"{new_date}"]
                filter_data = df[df["CATEGORY"] == "OE"]
                oe_target = filter_data["TARGET"]
                oe_actual = filter_data["ACTUAL"]
                comparison = np.where(oe_target > oe_actual, '#fa3232', '#4cf02b')
                if new_date.weekday() == 6: target_element.set('fill', '#2f52ed')
                else:
                    for result in comparison:
                        # st.write(result)
                        color = result
                        target_element.set('fill', color)
                    tree.write('daily_d.svg')
        # Display the modified SVG using Streamlit
        with open('daily_d.svg', 'r') as f:
            svg = f.read()
            b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
            html = r'<img src="data:image/svg+xml;base64,%s" style="height:20rem;"/>' % b64
            st.write(f"""
                <style>
                    .daily_d{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
                </style>
                <div>{html}
                    <p class="daily_d" style='left:20rem; top:4rem; color:black;'>LEGEND:</p>
                    <p class="daily_d" style='left:20rem; top:6.5rem; color:#4cf02b;'>TARGET ACHIEVED</p>
                    <p class="daily_d" style='left:20rem; top:9rem; color:#fa3232;'>TARGET MISSED</p>
                    <p class="daily_d" style='left:20rem; top:11.5rem; color:#2f52ed;'>PLANT OFF</p>
                </div>""", unsafe_allow_html=True)


        # tree = ET.parse('resources\D.svg')
        # root = tree.getroot()
        # current_date = datetime.date.today()
        # total_days = (current_date.day)
        # row_data = fetch_data("OTIF_CC PDI")
        # daily_data = row_data[row_data["DATE"] == f"{on_date}"]
        # filter_data = daily_data[daily_data["CATEGORY"] == "OE"]
        # oe_target = filter_data["TARGET"]
        # oe_actual = filter_data["ACTUAL"]
        # comparison = np.where(oe_target > oe_actual, 0, 1)
        # color = 'gray'
        # if on_date.weekday() == 6: color = 'blue'
        # else:
        #     for result in comparison:
        #         color='red' if result == 0 else 'green'
        # for i in range(1,32):
        #     if i<10:
        #         target_element = root.find(f".//*[@id='d-u-day{i}']")
        #     else:
        #         target_element = root.find(f".//*[@id='d-u-day{i}_']")
        #     # Change the color of the element
        #     if i == on_date.day:
        #         target_element.set('fill', color)
        #     else:
        #         target_element.set('fill', 'gray')
        #     # Save the modified SVG file
        #     tree.write('daily_d.svg')
        # # Display the modified SVG using Streamlit
        # with open('daily_d.svg', 'r') as f:
        #     svg = f.read()
        #     b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        #     html = r'<img src="data:image/svg+xml;base64,%s" style="height:17rem;"/>' % b64
        #     st.write(f"""
        #         <style>
        #             .daily_d{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
        #         </style>
        #         <div>{html}
        #             <p class="daily_d" style='left:17rem; top:7rem; color:black;'>LEGEND:</p>
        #             <p class="daily_d" style='left:17rem; top:8.5rem; color:green;'>TARGET ACHIEVED</p>
        #             <p class="daily_d" style='left:17rem; top:10rem; color:red;'>TARGET MISSED</p>
        #             <p class="daily_d" style='left:17rem; top:11.5rem; color:blue;'>PLANT OFF</p>
        #         </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div style='text-align:center; font-size:1.5rem; font-weight:bold'>ON TIME IN FULL (OTIF)</div>""",unsafe_allow_html=True)
        blk1,blk2=st.columns((1,1))
        with blk1:
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:7rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>OE<hr style='margin:0em;'>
                            <div style='content: ""; height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{oe.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{oe.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:7rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>OE SPARES<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{oe_spares.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{oe_spares.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
        with blk2:
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:7rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>AFTERMARKET<hr style='margin:0em;'>
                            <div style='content: ""; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{aftermarket.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{aftermarket.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:7rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>EXPORT<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{export.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{export.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
        h1_col1, h1_col2 = st.columns((1,1.1))
        with h1_col1:
            st.subheader("SALE PLAN VS ACTUAL")
        with h1_col2:
            pass
        sale_plan = fetch_data("SALE PLAN VS ACTUAL")
        bs_today = 0
        ord_book = 0
        act_sale = 0
        dlt_sb = 0
        dlt_so = 0
        filtered_data = sale_plan[sale_plan['DATE'] == pd.to_datetime(on_date, format='%Y-%m-%d')]
        if not filtered_data.empty:
            bs_today = filtered_data.iloc[0]["BUDGETED SALE"]
            ord_book = filtered_data.iloc[0]["ORDER BOOK"]
            act_sale = filtered_data.iloc[0]["ACTUAL SALE"]
            dlt_sb = filtered_data.iloc[0]["DELTA SB"]
            dlt_so = filtered_data.iloc[0]["DELTA SO"]
        else:
            bs_today = 0
            ord_book = 0
            act_sale = 0
            dlt_sb = 0
            dlt_so = 0
    st.markdown(f"""
        <style>
                .float-container {{  padding: 5px;   }}
                .float-bd {{width: 20%; font-size:1rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.4rem; border: 1px solid black; overflow:hidden;
                }}
                .float-hd {{width: 20%; font-size:1rem; color:black; float: left; word-wrap:break-word; height:8rem; text-align:center; padding-top: 2.5rem; line-height:1rem; border: 1px solid black; overflow:hidden;
                }}
                .float-icu {{width: 100%; font-size:1.2rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.8rem; border: 1px solid black; overflow:hidden;
                }}
                .float-hcu {{width: 46%; font-size:1rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:7rem; text-align:center; padding: 10px; line-height:1rem; border: 1px solid black; overflow:hidden;
                }}
                .float-hcd {{width: 20%; font-size:1rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:15rem; text-align:center; padding: 10px; border: 1px solid black; overflow:hidden;}}
                .float-dcd {{width: 20%; font-size:1rem; color:black; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 10px; border: 1px solid black; overflow:hidden;}}
                .par {{padding-top:1rem; font-size:1rem; color:black; overflow:hidden; }}
                hr{{ margin:0em; }}
        </style>
        <div class="float-container">
            <div class="float-bd">BUDGETED SALE (B)</div>
            <div class="float-bd">ORDER BOOK (O)</div>
            <div class="float-bd">ACTUAL SALE (S)</div>
            <div class="float-bd">DELTA (S-B)</div>
            <div class="float-bd">DELTA (S-O)</div>
        </div>
        <div class="float-container">
            <div class="float-hd">{bs_today}</div>
            <div class="float-hd">{ord_book}</div>
            <div class="float-hd">{act_sale}</div>
            <div class="float-hd">{dlt_sb}</div>
            <div class="float-hd">{dlt_so}</div>
        </div>
    """,unsafe_allow_html=True)
    
    issues = fetch_data("DELIVERY ISSUES")
    delivery_issue = []
    issues = issues[(issues["DATE"] == f"{on_date}")]
    length = len(issues)
    del_max_issues = 3
    for index, row in issues.iterrows():
        issue = {
            "PART_NO": row["PART NO"],
            "ISSUE": row["ISSUE RAISED"],
            "ACTION": row["ACTION"],
            "T_DATE": row["TARGET DATE"]
        }
        delivery_issue.append(issue)
        pass
    while length < del_max_issues:
        dummy_issue = {
            "PART_NO": "N/A",
            "ISSUE": "N/A",
            "ACTION": "N/A",
            "T_DATE": "N/A"
        }
        delivery_issue.append(dummy_issue)
        del_max_issues = del_max_issues-1
    
    st.markdown(f"""
            <div class="float-container">
                <div class="float-icu">Costomer Urgencies/Issues</div>
            </div>
            <div class="float-container">
                <div class="float-hcd">Part No <hr>
                    <p class="par">{delivery_issue[0]["PART_NO"]}</p>
                    <p class="par">{delivery_issue[1]["PART_NO"]}</p>
                    <p class="par">{delivery_issue[2]["PART_NO"]}</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Issue Raised <hr>
                    <p class="par">{delivery_issue[0]["ISSUE"]}</p>
                    <p class="par">{delivery_issue[1]["ISSUE"]}</p>
                    <p class="par">{delivery_issue[2]["ISSUE"]}</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Action to be Taken <hr>
                    <p class="par">{delivery_issue[0]["ACTION"]}</p>
                    <p class="par">{delivery_issue[1]["ACTION"]}</p>
                    <p class="par">{delivery_issue[2]["ACTION"]}</p>
                </div>
                <div class="float-hcd">Trgt Date <hr>
                    <p class="par">{delivery_issue[0]["T_DATE"]}</p>
                    <p class="par">{delivery_issue[1]["T_DATE"]}</p>
                    <p class="par">{delivery_issue[2]["T_DATE"]}</p>
                </div>
            </div>
    """,unsafe_allow_html=True)
    # CRITICAL COSTOMER PDI
    st.subheader("CRITICAL COSTOMER P.D.I.")
    bl1,bl2,bl3=st.columns((1,1,1))
    with bl1:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>MSIL<hr style='margin:0em;'>
                            <div style='content: ""; height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{msil.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div> 
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{msil.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>HD<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{hd.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{hd.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl2:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HONDA<hr style='margin:0em;'>
                            <div style='content: ""; height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{honda.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{honda.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>RNAIPL<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{rnaipl.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{rnaipl.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl3:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>GM<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{gm.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{gm.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>FORD<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{ford.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{ford.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)

def otif():
    oe = cmp(0,0)
    aftermarket = cmp(0,0)
    oe_spares = cmp(0,0)
    export = cmp(0,0)
    # rows = delivery_data_fetch()
    today = current_date()
    d_data = fetch_data("OTIF_CC PDI")
    for index, row in d_data.iterrows():
        date = pd.Timestamp(row["DATE"]).strftime('%Y-%m-%d')
        if date == f"{today}":
            if row["CATEGORY"] == "OE":
                oe = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "AfterMarket":
                aftermarket = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "OE_Spare":
                oe_spares = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "Export":
                export = cmp(row["TARGET"], row["ACTUAL"])
            pass
    blk1,blk2,blk3,blk4=st.columns((1,1,1,1))
    with blk1:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>OE<hr style='margin:0em;'>
                        <div style='content: ""; height:72%;display: table; display:flex;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                <h6>{oe.target}%</h6>
                            </div>
                            <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                            <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                <h6>{oe.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
    with blk2:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>OE SPARES<hr style='margin:0em;'>
                        <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                <h6>{oe_spares.target}%</h6>
                            </div>
                            <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                <h6>{oe_spares.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
    with blk3:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>AFTERMARKET<hr style='margin:0em;'>
                        <div style='content: ""; height:72%;display: table;display:flex;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                <h6>{aftermarket.target}%</h6>
                            </div>
                            <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                            <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                <h6>{aftermarket.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
    with blk4:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>EXPORT<hr style='margin:0em;'>
                        <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                <h6>{export.target}%</h6>
                            </div>
                            <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                <h6>{export.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)

    d_data['DATE'] = pd.to_datetime(d_data['DATE'])
    # month_data = d_data[d_data["DATE"].dt.month == 10]  # Filter data for the month
    # st.write(month_data)
    current_month = pd.Timestamp('now').to_period('M')  # Filter data for the month
    # cl1,cl2,cl3,cl4 = st.columns((1,1,1,1))
    # with cl1:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>OE</center>""",unsafe_allow_html=True)
    # with cl2:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>OE_SPARES</center>""",unsafe_allow_html=True)
    # with cl3:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>AFTERMARKET</center>""",unsafe_allow_html=True)
    # with cl4:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>EXPORT</center>""",unsafe_allow_html=True)
    # st.markdown("___")

    otif_month_data = fetch_month_data("OTIF_CC PDI")
    # oe_data = d_data[(d_data['CATEGORY'] == 'OE') & (d_data['DATE'].dt.to_period('M') == current_month)]
    # oe_spare_data = d_data[(d_data['CATEGORY'] == 'OE_Spare') & (d_data['DATE'].dt.to_period('M') == current_month)]
    # aftermarket_data = d_data[(d_data['CATEGORY'] == 'AfterMarket') & (d_data['DATE'].dt.to_period('M') == current_month)]
    # export_data = d_data[(d_data['CATEGORY'] == 'Export') & (d_data['DATE'].dt.to_period('M') == current_month)]
    st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    d1,d2,d3,d4 = st.columns((1,1,1,1))
    with d1:    # ****** Daily_Data ****** #
        # Filter the DataFrame for the desired month and week number
        desired_data = otif_month_data[otif_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "OE"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='OE', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)


        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)
    with d2:    # ****** Daily_Data ****** #
        desired_data = otif_month_data[otif_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "OE_Spare"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='OE SPAREs', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)


        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)
    with d3:    # ****** Daily_Data ****** #
        desired_data = otif_month_data[otif_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "AfterMarket"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='AFTERMARKET', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)


        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)
    with d4:    # ****** Daily_Data ****** #
        desired_data = otif_month_data[otif_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "Export"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='EXPORT', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)


        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)

    st.markdown("___")
    st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Weekly Trend</center>""",unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns((1,1,1,1))
    with m1:    # ****** Weekly_Data ****** #
        # weekly_data = oe_data.groupby(oe_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = otif_month_data[otif_month_data["CATEGORY"] == "OE"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=week,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="OE",
        )
        st.plotly_chart(fig, use_container_width=True)

    with m2:    # ****** Weekly_Data ****** #
        # weekly_data = oe_spare_data.groupby(oe_spare_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = otif_month_data[otif_month_data["CATEGORY"] == "OE_Spare"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=week,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="OE SPARES",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with m3:    # ****** Weekly_Data ****** #
        # weekly_data = aftermarket_data.groupby(aftermarket_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = otif_month_data[otif_month_data["CATEGORY"] == "AfterMarket"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=week,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="AFTERMARKET",
        )
        st.plotly_chart(fig, use_container_width=True)

    with m4:    # ****** Weekly_Data ****** #
        # weekly_data = export_data.groupby(export_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])
        hp_data = otif_month_data[otif_month_data["CATEGORY"] == "Export"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=week,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="EXPORT",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("___")
    st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Yearly Trend</center>""",unsafe_allow_html=True)
    y1,y2,y3,y4 = st.columns((1,1,1,1))
    with y1:    # ****** Monthly_Data ****** #
        # oe_data_month = d_data[d_data['CATEGORY'] == 'OE']
        # monthly_data = oe_data_month.groupby(oe_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])
        hp_data_month = d_data[d_data['CATEGORY'] == 'OE']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="OE",
        )
        st.plotly_chart(fig, use_container_width=True)

    with y2:    # ****** Monthly_Data ****** #
        # oe_spare_data_month = d_data[d_data['CATEGORY'] == 'OE_Spare']
        # monthly_data = oe_spare_data_month.groupby(oe_spare_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'OE_Spare']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="OE SPARES",
        )
        st.plotly_chart(fig, use_container_width=True)

    with y3:    # ****** Monthly_Data ****** #
        # aftermarket_data_month = d_data[d_data['CATEGORY'] == 'AfterMarket']
        # monthly_data = aftermarket_data_month.groupby(aftermarket_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'AfterMarket']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="AFTERMARKET",
        )
        st.plotly_chart(fig, use_container_width=True)

    with y4:    # ****** Monthly_Data ****** #
        # export_data_month = d_data[d_data['CATEGORY'] == 'Export']
        # monthly_data = export_data_month.groupby(export_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'Export']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="EXPORT",
        )
        st.plotly_chart(fig, use_container_width=True)

def sale_actual():
    # Sale Plan vs Actual Plan
    current_date()
    # st.subheader("Sale Plan vs Actual Trend")

    current_month = pd.Timestamp('now').to_period('M')
    d_data = fetch_data("SALE PLAN VS ACTUAL")
    hp_data = d_data[d_data['DATE'].dt.to_period('M') == current_month]
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    

    sale_plan = d_data
    sale_plan["DATE"] = pd.to_datetime(sale_plan["DATE"])
    month = datetime.datetime.now().month
    filter_data = sale_plan[sale_plan["DATE"].dt.month == month]
    Total_month_budget = filter_data["BUDGETED SALE"].sum()
    Total_month_order = filter_data["ORDER BOOK"].sum()
    Total_month_actual_sale = filter_data["ACTUAL SALE"].sum()
    Total_delta_sb = Total_month_actual_sale - Total_month_budget
    Total_delta_so = Total_month_actual_sale - Total_month_order
    # st.write(f"value is = {Total_delta_so}")
    st.markdown(f"""
        <style>
                .float-container {{  padding: 5px;   }}
                .float-bd {{width: 20%; font-size:1rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.4rem; border: 1px solid black; overflow:hidden;
                }}
                .float-hd {{width: 20%; font-size:1rem; color:black; float: left; word-wrap:break-word; height:8rem; text-align:center; padding-top: 2.5rem; line-height:1rem; border: 1px solid black; overflow:hidden;
                }}
                .float-icu {{width: 100%; font-size:1rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.4rem; border: 1px solid black; overflow:hidden;
                }}
                .float-hcu {{width: 46%; font-size:1rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:7rem; text-align:center; padding: 10px; line-height:1rem; border: 1px solid black; overflow:hidden;
                }}
                .float-hcd {{width: 20%; font-size:1rem; color:black; font-weight:bold; float: left; word-wrap:break-word; height:15rem; text-align:center; padding: 10px; border: 1px solid black; overflow:hidden;}}
                .float-dcd {{width: 20%; font-size:1rem; color:black; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 10px; border: 1px solid black; overflow:hidden;}}
                .par {{padding-top:1rem; font-size:1rem; color:black; overflow:hidden; }}
                hr{{ margin:0em; }}
        </style>
        <div class="float-container">
            <div class="float-bd">BUDGETED SALE (B)</div>
            <div class="float-bd">ORDER BOOK (O)</div>
            <div class="float-bd">ACTUAL SALE (S)</div>
            <div class="float-bd">DELTA (S-B)</div>
            <div class="float-bd">DELTA (S-O)</div>
        </div>
        <div class="float-container">
            <div class="float-hd">{Total_month_budget}</div>
            <div class="float-hd">{Total_month_order}</div>
            <div class="float-hd">{Total_month_actual_sale}</div>
            <div class="float-hd">{Total_delta_sb}</div>
            <div class="float-hd">{Total_delta_so}</div>
        </div>
    """,unsafe_allow_html=True)
    
    del_issue = fetch_data("DELIVERY ISSUEs")
    delivery_issue = []
    del_issue['DATE'] = pd.to_datetime(del_issue['DATE']) # Convert the "DATE" column to datetime
    current_month = datetime.datetime.now().month
    filtered_del_issue = del_issue[del_issue['DATE'].dt.month == current_month]
    length = len(filtered_del_issue)
    ftp_max_issues = 3
    for index, row in filtered_del_issue.iterrows():
        issue = {
            "PART_NO": row["PART NO"],
            "ISSUE": row["ISSUE RAISED"],
            "ACTION": row["ACTION"],
            "T_DATE": row["TARGET DATE"]
        }
        delivery_issue.append(issue)
        pass
    while length < ftp_max_issues:
        dummy_issue = {
            "PART_NO": "N/A",
            "ISSUE": "N/A",
            "ACTION": "N/A",
            "T_DATE": "N/A"
        }
        delivery_issue.append(dummy_issue)
        ftp_max_issues = ftp_max_issues-1

    st.markdown(f"""
            <div class="float-container">
                <div class="float-icu">Costomer Urgencies/Issues</div>
            </div>
            <div class="float-container">
                <div class="float-hcd">Part No <hr>
                    <p class="par">{delivery_issue[0]["PART_NO"]}</p>
                    <p class="par">{delivery_issue[1]["PART_NO"]}</p>
                    <p class="par">{delivery_issue[2]["PART_NO"]}</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Issue Raised <hr>
                    <p class="par">{delivery_issue[0]["ISSUE"]}</p>
                    <p class="par">{delivery_issue[1]["ISSUE"]}</p>
                    <p class="par">{delivery_issue[2]["ISSUE"]}</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Action to be Taken <hr>
                    <p class="par">{delivery_issue[0]["ACTION"]}</p>
                    <p class="par">{delivery_issue[1]["ACTION"]}</p>
                    <p class="par">{delivery_issue[2]["ACTION"]}</p>
                </div>
                <div class="float-hcd">Target Date <hr>
                    <p class="par">{delivery_issue[0]["T_DATE"]}</p>
                    <p class="par">{delivery_issue[1]["T_DATE"]}</p>
                    <p class="par">{delivery_issue[2]["T_DATE"]}</p>
                </div>
            </div>
    """,unsafe_allow_html=True)

    col1,col2,col3 = st.columns((1,1,1))
    with col1:  # ****** Daily_Data ****** #
        hp_data = hp_data[hp_data['DATE'].dt.strftime('%U') == current_week_number]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        new_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        new_df['color'] = np.where(new_df['BUDGETED SALE'] >= new_df['ACTUAL SALE'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(new_df['Day'], new_df['ACTUAL SALE'], new_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=35), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=new_df['Day'], y=new_df['BUDGETED SALE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Values')
        st.plotly_chart(fig, use_container_width=True)
    with col2:  # ****** Weekly_Data ****** #
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL SALE', 'BUDGETED SALE']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL SALE'] >= weekly_data['BUDGETED SALE'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL SALE'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    with col3:  # ****** Monthly_Data ****** 
        monthly_data = d_data.groupby(d_data['DATE'].dt.to_period('M'))[['BUDGETED SALE', 'ACTUAL SALE']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL SALE'] >= monthly_data['BUDGETED SALE'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL SALE'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

def critcal_customer_pdi():
    msil = cmp(0,0)
    honda = cmp(0,0)
    gm = cmp(0,0)
    hd = cmp(0,0)
    rnaipl = cmp(0,0)
    ford = cmp(0,0)
    d_data = fetch_data("OTIF_CC PDI")
    today = current_date()
    for index, row in d_data.iterrows():
        date = pd.Timestamp(row["DATE"]).strftime('%Y-%m-%d')
        if date == f"{today}":
            if row["CATEGORY"] == "MSIL":
                msil = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "Honda":
                honda = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "GM":
                gm = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "HD":
                hd = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "RNAIPL":
                rnaipl = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "Ford":
                ford = cmp(row["TARGET"], row["ACTUAL"])
            pass
    # CRITICAL COSTOMER PDI
    bl1,bl2,bl3=st.columns((1,1,1))
    with bl1:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>MSIL<hr style='margin:0em;'>
                            <div style='content: "";height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{msil.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{msil.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>HD<hr style='margin:0em;'>
                            <div style='content: center; height:72%; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{hd.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{hd.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl2:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HONDA<hr style='margin:0em;'>
                            <div style='content: ""; height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{honda.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{honda.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>RNAIPL<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{rnaipl.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{rnaipl.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl3:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>GM<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{gm.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{gm.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>FORD<hr style='margin:0em;'>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{ford.target}%</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{ford.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)

    d_data['DATE'] = pd.to_datetime(d_data['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    # col1,col2,col3,col4 = st.columns((1,1,1,1))
    # with col1:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>MSIL</center>""",unsafe_allow_html=True)
    # with col2:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>HD</center>""",unsafe_allow_html=True)
    # with col3:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>HONDA</center>""",unsafe_allow_html=True)
    # with col4:
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>GM</center>""",unsafe_allow_html=True)

    msil_data = d_data[(d_data['CATEGORY'] == 'MSIL') & (d_data['DATE'].dt.to_period('M') == current_month)]
    hd_data = d_data[(d_data['CATEGORY'] == 'HD') & (d_data['DATE'].dt.to_period('M') == current_month)]
    honda = d_data[(d_data['CATEGORY'] == 'Honda') & (d_data['DATE'].dt.to_period('M') == current_month)]
    gm = d_data[(d_data['CATEGORY'] == 'GM') & (d_data['DATE'].dt.to_period('M') == current_month)]
    st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
    cc_month_data = fetch_month_data("OTIF_CC PDI")
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    d1,d2,d3,d4 = st.columns((1,1,1,1))
    with d1:    # ****** Daily_Data ****** #
        # daily_data = msil_data.groupby(msil_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data.index = daily_data.index.strftime('%a') 
        # st.bar_chart(daily_data, color=["#fa2323","#5fe650"])

        # Filter the DataFrame for the desired month and week number
        desired_data = cc_month_data[cc_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "MSIL"]
        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='MSIL', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)

    with d2:    # ****** Daily_Data ****** #
        # daily_data = hd_data.groupby(hd_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data.index = daily_data.index.strftime('%a') 
        # st.bar_chart(daily_data, color=["#fa2323","#5fe650"])

        # Filter the DataFrame for the desired month and week number
        desired_data = cc_month_data[cc_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "HD"]
        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='HD', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)

    with d3:    # ****** Daily_Data ****** #
        # daily_data = honda.groupby(honda['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data.index = daily_data.index.strftime('%a') 
        # st.bar_chart(daily_data, color=["#fa2323","#5fe650"])

        # Filter the DataFrame for the desired month and week number
        desired_data = cc_month_data[cc_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "Honda"]
        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='HONDA', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)

    with d4:    # ****** Daily_Data ****** #
        # daily_data = gm.groupby(gm['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data.index = daily_data.index.strftime('%a') 
        # st.bar_chart(daily_data, color=["#fa2323","#5fe650"])

        # Filter the DataFrame for the desired month and week number
        desired_data = cc_month_data[cc_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "GM"]
        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Actual', line=dict(color=my_color, width=25), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='GM', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("___")
    st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Weekly Trend</center>""",unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns((1,1,1,1))
    with m1:    # ****** Weekly_Data ****** #
        # weekly_data = msil_data.groupby(msil_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = cc_month_data[cc_month_data["CATEGORY"] == "MSIL"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="MSIL",
        )
        st.plotly_chart(fig, use_container_width=True)

    with m2:    # ****** Weekly_Data ****** #
        # weekly_data = hd_data.groupby(hd_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = cc_month_data[cc_month_data["CATEGORY"] == "HD"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="HD",
        )
        st.plotly_chart(fig, use_container_width=True)

    with m3:    # ****** Weekly_Data ****** #
        # weekly_data = honda.groupby(honda['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = cc_month_data[cc_month_data["CATEGORY"] == "Honda"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="HONDA",
        )
        st.plotly_chart(fig, use_container_width=True)

    with m4:    # ****** Weekly_Data ****** #
        # weekly_data = gm.groupby(gm['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = cc_month_data[cc_month_data["CATEGORY"] == "GM"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="GM",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("___")
    st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Yearly Trend</center>""",unsafe_allow_html=True)
    y1,y2,y3,y4 = st.columns((1,1,1,1))
    with y1:    # ****** Monthly_Data ****** #
        # msil_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        # monthly_data = msil_data_month.groupby(msil_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="MSIL",
        )
        st.plotly_chart(fig, use_container_width=True)

    with y2:    # ****** Monthly_Data ****** #
        # hd_data_month = d_data[d_data['CATEGORY'] == 'HD']
        # monthly_data = hd_data_month.groupby(hd_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'HD']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="HD",
        )
        st.plotly_chart(fig, use_container_width=True)

    with y3:    # ****** Monthly_Data ****** #
        # honda_month = d_data[d_data['CATEGORY'] == 'Honda']
        # monthly_data = honda_month.groupby(honda_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'Honda']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="HONDA",
        )
        st.plotly_chart(fig, use_container_width=True)

    with y4:    # ****** Monthly_Data ****** #
        # gm_month = d_data[d_data['CATEGORY'] == 'GM']
        # monthly_data = gm_month.groupby(gm_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'GM']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="GM",
        )
        st.plotly_chart(fig, use_container_width=True)

#************************** Delivery_FTD End **************************#


#************************** Quality_FTD Start **************************#
def quality_ftd():
    # st.subheader(f"Status as on: {on_date}",divider="gray")
    st.markdown(f"""
            <div>
                <h3 style='position:absolute; bottom:0rem;'>Status as on: {on_date}</h3>
            </div>
            <hr>
        """, unsafe_allow_html=True)
        
    # st.markdown("___")
    plant_ppm = cmp(0,0)
    supplier_ppm = cmp(0,0)
    complaint_data = fetch_data("CUSTOMER COMPLAINTS")
    df = complaint_data[complaint_data["DATE"] == f"{on_date}"]
    ppm_data = fetch_data("PLANT PPM & SUPPLIER PPM")
    ppm_problem = fetch_data("PPM PROBLEMS")

    for index, row in ppm_data.iterrows():
        date = pd.Timestamp(row["DATE"]).strftime('%Y-%m-%d')
        if date == f"{on_date}":
            if row["CATEGORY"] == "PLANT PPM":
                plant_ppm = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "SUPPLIER PPM":
                supplier_ppm = cmp(row["TARGET"], row["ACTUAL"])
        pass
    col1,col2=st.columns((1,1.8))
    with col1:  # ********** Dynamic Q Letter ********** #
        tree = ET.parse('resources\Q.svg')
        root = tree.getroot()
        current_date = datetime.date.today()
        total_days = (current_date.day)
        row_data = fetch_month_data("CUSTOMER COMPLAINTS")
        first_day_of_month = current_date.replace(day=1)
        days_to_add = 0
        for i in range(1, 32):
            if i < 10:
                target_element = root.find(f".//*[@id='q-u-day{i}']")
            else:
                target_element = root.find(f".//*[@id='q-u-day{i}_']")
            new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
            days_to_add += 1
            new_df = row_data[row_data["DATE"] == f"{new_date}"]
            if len(row_data) == 0:
                if new_date.weekday() == 6: color = "#2f52ed"
                else:
                    color = '#d2dbed'
            else:
                if new_date.weekday() == 6: color = "#2f52ed"
                elif i <= total_days:
                    count_problem = len(new_df["COMPLAINT"])
                    if new_date.weekday() == 6: color = "#2f52ed"
                    else:
                        if count_problem > 0: color = '#fa3232'
                        else: color = '#4cf02b'
                else: color = "#d2dbed"
            target_element.set('fill', color)
            tree.write('daily_q.svg')
        # Display the modified SVG using Streamlit
        with open('daily_q.svg', 'r') as f:
            svg = f.read()
            b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
            html = r'<img src="data:image/svg+xml;base64,%s" style="height:20rem;"/>' % b64
            st.write(f"""
                <style>
                    .daily_q{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
                </style>
                <div>{html}
                    <p class="daily_q" style='left:20rem; top:4rem; color:black;'>LEGEND:</p>
                    <p class="daily_q" style='left:20rem; top:6.5rem; color:#4cf02b;'>TARGET ACHIEVED</p>
                    <p class="daily_q" style='left:20rem; top:9rem; color:#fa3232;'>TARGET MISSED</p>
                    <p class="daily_q" style='left:20rem; top:11.5rem; color:#2f52ed;'>PLANT OFF</p>
                </div>""", unsafe_allow_html=True)


        # tree = ET.parse('resources\Q.svg')
        # root = tree.getroot()
        # # current_date = datetime.date.today()
        # # total_days = (current_date.day)
        # row_data = fetch_data("CUSTOMER COMPLAINTS")
        # daily_data = row_data[row_data["DATE"] == f"{on_date}"]
        # color = 'gray'
        # count_problem = len(daily_data["COMPLAINT"])
        # if on_date.weekday() == 6: color = "blue"
        # else:
        #     if count_problem > 1: color = 'red'
        #     elif count_problem <= 1: color = 'green'
        #     # else: color = '#d2dbed'
        # for i in range(1,32):
        #     if i<10:
        #         target_element = root.find(f".//*[@id='q-u-day{i}']")
        #     else:
        #         target_element = root.find(f".//*[@id='q-u-day{i}_']")
        #     # Change the color of the element
        #     if i == on_date.day:
        #         target_element.set('fill', color)
        #     else:
        #         target_element.set('fill', '#d2dbed')
        #     # Save the modified SVG file
        #     tree.write('daily_q.svg')
        # # Display the modified SVG using Streamlit
        # with open('daily_q.svg', 'r') as f:
        #     svg = f.read()
        #     b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        #     html = r'<img src="data:image/svg+xml;base64,%s" style="height:18rem;"/>' % b64
        #     st.write(f"""
        #         <style>
        #             .daily_d{{ font-size:1rem; margin:0rem; position:absolute; font-weight:bold;}}
        #         </style>
        #         <div>{html}
        #             <p class="daily_d" style='left:17rem; top:7rem; color:black;'>LEGEND:</p>
        #             <p class="daily_d" style='left:17rem; top:8.5rem; color:green;'>TARGET ACHIEVED</p>
        #             <p class="daily_d" style='left:17rem; top:10rem; color:red;'>TARGET MISSED</p>
        #             <p class="daily_d" style='left:17rem; top:11.5rem; color:blue;'>PLANT OFF</p>
        #         </div>""", unsafe_allow_html=True)

    with col2:  # **************** Customer Complaints **************** #
        if len(df) == 0:
            pass
        else:
            st.markdown(f"##### Today'S Customer Complaints: {len(df)}")
            data_df = df[["COMPLAINT", "RAISE DATE", "RESPONSIBILITY", "TARGET DATE", "STATUS"]]
            def format_status(status):
                if status == "Open":
                    return 'background-color: #fa4d4d'
                elif status == "Closed":
                    return 'background-color: #5fe650'
                elif status == "Inprocess":
                    return 'background-color: #e9f76a'
                else:
                    return ''
            # data_df['STATUS'] = data_df['STATUS'].apply(lambda x: f'<span style="{format_status(x)}">{x}</span>')
            data_df = data_df.style.applymap(format_status, subset=['STATUS'])
            st.write(data_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # **************** Plant PPM & Supplier PPM **************************#
        # st.markdown("""<div style='padding-top:1.5rem;'><h5>PLANT PPM & SUPPLIER PPM</h5></div>""",unsafe_allow_html=True)
        plant_prob = []
        supplier_prob = []
        plant_filter = ppm_problem[(ppm_problem["DATE"] == f"{on_date}") & (ppm_problem["CATEGORY"] == "PLANT PPM")]
        supplier_filter = ppm_problem[(ppm_problem["DATE"] == f"{on_date}") & (ppm_problem["CATEGORY"] == "SUPPLIER PPM")]
        plant_length = len(plant_filter)
        supplier_length = len(supplier_filter)
        plant_max_issues = 3
        supplier_max_issues = 3
        for index, row in plant_filter.iterrows():
            issue = {
                "PROBLEM": row["PROBLEM"],
                "PART_LINE": row["PART_LINE"],
                "REJ_QTY": row["REJ_QTY"]
            }
            plant_prob.append(issue)
            pass
        while plant_length < plant_max_issues:
            dummy_issue = {
                "PROBLEM": "N/A",
                "PART_LINE": "N/A",
                "REJ_QTY": "N/A"
            }
            plant_prob.append(dummy_issue)
            plant_max_issues = plant_max_issues-1

        for index, row in supplier_filter.iterrows():
            issue = {
                "PROBLEM": row["PROBLEM"],
                "PART_LINE": row["PART_LINE"],
                "REJ_QTY": row["REJ_QTY"]
            }
            supplier_prob.append(issue)
            pass
        while supplier_length < supplier_max_issues:
            dummy_issue = {
                "PROBLEM": "N/A",
                "PART_LINE": "N/A",
                "REJ_QTY": "N/A"
            }
            supplier_prob.append(dummy_issue)
            supplier_max_issues = supplier_max_issues-1

        cl1,cl2=st.columns((1,2))
        with cl1:   # ********** PPM Actual & Target ********** #
            st.markdown(f"""<div style='margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>PLANT PPM<hr style='margin:0em;'>
                        <div style='content: ""; height:72%; display: table;display:flex;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                <h6>{plant_ppm.target}</h6>
                            </div>
                            <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                            <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                <h6>{plant_ppm.actual}</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style='margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>SUPPLIER PPM<hr style='margin:0em;'>
                        <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                <h6>{supplier_ppm.target}</h6>
                            </div>
                            <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                <h6>{supplier_ppm.actual}</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
        with cl2:
            st.markdown(f"""
            <style>
                .float-container {{ padding: 5px; }}
                .ftp_prb {{ font-size:1rem; float: left;font-weight:bold;height:8.5rem;text-align:center;padding: 10px;border: 1px solid black;
                }}
                .ftp_prb p {{ width: 100%; font-size:0.8rem; height:0.5rem; text-align:center; padding: 5px;
                }}
                .ftp_prb hr{{ margin: 0.2rem; }}
            </style>
            <div style='padding-top:0.5rem;'>
                <div class="float-container">
                <div class="ftp_prb" style='width:50%'>Problems<hr>
                    <p >{plant_prob[0]["PROBLEM"]}</p>
                    <p >{plant_prob[1]["PROBLEM"]}</p>
                    <p >{plant_prob[2]["PROBLEM"]}</p>
                </div>
                <div class="ftp_prb" style='width:25%'>Part/Line<hr>
                    <p >{plant_prob[0]["PART_LINE"]}</p>
                    <p >{plant_prob[1]["PART_LINE"]}</p>
                    <p >{plant_prob[2]["PART_LINE"]}</p>
                </div>
                <div class="ftp_prb" style='width:25%'>Rej Qty<hr>
                    <p >{plant_prob[0]["REJ_QTY"]}</p>
                    <p >{plant_prob[1]["REJ_QTY"]}</p>
                    <p >{plant_prob[2]["REJ_QTY"]}</p>
                </div>
            </div>
            """,unsafe_allow_html=True)
            st.markdown(f"""
                <div style='padding-top:0.5rem;'>
                    <div class="float-container">
                    <div class="ftp_prb" style='font-weight:bold; width:50%'>Problems<hr>
                        <p >{supplier_prob[0]["PROBLEM"]}</p>
                        <p >{supplier_prob[1]["PROBLEM"]}</p>
                        <p >{supplier_prob[2]["PROBLEM"]}</p>
                    </div>
                    <div class="ftp_prb" style='font-weight:bold; width:25%'>Part/Line<hr>
                        <p >{supplier_prob[0]["PART_LINE"]}</p>
                        <p >{supplier_prob[1]["PART_LINE"]}</p>
                        <p >{supplier_prob[2]["PART_LINE"]}</p>
                    </div>
                    <div class="ftp_prb" style='font-weight:bold; width:25%'>Rej Qty<hr>
                        <p >{supplier_prob[0]["REJ_QTY"]}</p>
                        <p >{supplier_prob[1]["REJ_QTY"]}</p>
                        <p >{supplier_prob[2]["REJ_QTY"]}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        pass
    ftp_rej = fetch_data("FTP AND REPORTED REJECTION")
    # st.table(ftp_rej[["CATEGORY", "TARGET", "ACTUAL", "PART NO", "ISSUE", "ACTION", "TARGET DATE"]])
    today_target = ftp_rej[ftp_rej["DATE"] == f'{on_date}']
    ftp_today = cmp(0,0)
    rej_inr = cmp(0,0)
    rej_per = cmp(0,0)
    for index, row in today_target.iterrows():
        if row["CATEGORY"] == "First Time Pass (%)":
            ftp_today = cmp(row["TARGET"], row["ACTUAL"])
        if row["CATEGORY"] == "Reported Rejection (%)":
            rej_per = cmp(row["TARGET"], row["ACTUAL"])
        if row["CATEGORY"] == "Reported Rejection (INR)":
            rej_inr = cmp(row["TARGET"], row["ACTUAL"])
    # st.write(ftp_today.show())
    # st.table(today_target)
    st.markdown(f"""
                <style>
                     .float-container {{ padding: 5px;   }}
                     .float-prb {{ width: 55%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }}
                    .float-prt {{ width: 20%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }}
                    .float-pn {{width: 20%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .float-ir {{width: 40%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .float-ca {{width: 20%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .float-td {{width: 15%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .par {{padding-top:0.6rem; font-size:0.8rem; color:black; }}
                    hr{{ margin:0em; }}
                </style>
                <div>
                     <div class="float-container">
                        <div class="float-prb" style='height:10rem; font-size:1rem;'>Particular <hr>
                        <p class="par" style='font-weight:bold;'>Firtst Time Pass % (FTP)</p>
                        <p class="par" style='font-weight:bold;'>Reported Rejection (%)</p>
                        <p class="par" style='font-weight:bold;'>Reported Rejection (INR)</p>
                    </div>
                        <div class="float-prt" style='height:10rem; font-size:1rem'>Target <hr>
                        <p class="par">{ftp_today.target}</p>
                        <p class="par">{rej_per.target}</p>
                        <p class="par">{rej_inr.target}</p>
                    </div>
                        <div class="float-prt" style='height:10rem; font-size:1rem'>Actual <hr>
                        <p class="par">{ftp_today.actual}</p>
                        <p class="par">{rej_per.actual}</p>
                        <p class="par">{rej_inr.actual}</p>
                    </div>
                </div>
                    
            """,unsafe_allow_html=True)

    # ftp rejection issue
    fr_issue = fetch_data("FTP REJECTION ISSUE")
    ftp_issue = []
    fr_issue = fr_issue[(fr_issue["DATE"] == f"{on_date}")]
    length = len(fr_issue)
    ftp_max_issues = 3
    for index, row in fr_issue.iterrows():
        issue = {
            "PART_NO": row["PART NO"],
            "ISSUE": row["ISSUE"],
            "ACTION": row["ACTION"],
            "T_DATE": row["TARGET DATE"]
        }
        ftp_issue.append(issue)
        pass
    while length < ftp_max_issues:
        dummy_issue = {
            "PART_NO": "N/A",
            "ISSUE": "N/A",
            "ACTION": "N/A",
            "T_DATE": "N/A"
        }
        ftp_issue.append(dummy_issue)
        ftp_max_issues = ftp_max_issues-1

    # st.write(fr_issue)
    st.markdown(f"""
        <div class="float-container">
            <div class="float-pn">Part number<hr>
                <p class="par">{ftp_issue[0]["PART_NO"]}</p>
                <p class="par">{ftp_issue[1]["PART_NO"]}</p>
                <p class="par">{ftp_issue[2]["PART_NO"]}</p>
            </div>
            <div class="float-ir">Issue Reported<hr>
                <p class="par">{ftp_issue[0]["ISSUE"]}</p>
                <p class="par">{ftp_issue[1]["ISSUE"]}</p>
                <p class="par">{ftp_issue[2]["ISSUE"]}</p>
            </div>
            <div class="float-ca">Corrective Action<hr>
                <p class="par">{ftp_issue[0]["ACTION"]}</p>
                <p class="par">{ftp_issue[1]["ACTION"]}</p>
                <p class="par">{ftp_issue[2]["ACTION"]}</p>
            </div>
            <div class="float-td">Targate Date<hr>
                <p class="par">{ftp_issue[0]["T_DATE"]}</p>
                <p class="par">{ftp_issue[1]["T_DATE"]}</p>
                <p class="par">{ftp_issue[2]["T_DATE"]}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def customer_complaint():
    current_date()
    datas = []
    df = fetch_data("CUSTOMER COMPLAINTS")
    df['DATE'] = pd.to_datetime(df['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    month_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    total_complaints = len(month_data)

    length = len(month_data)
    max_complaint = 6
    for index, row in month_data.iterrows():
        issue = {
            "COMPLAINT": row["COMPLAINT"],
            "RAISE_DATE": row["RAISE DATE"],
            "TARGET_DATE": row["TARGET DATE"],
            "STATUS": row["STATUS"],
            "RESPONSIBILITY": row["RESPONSIBILITY"]
        }
        datas.append(issue)
        pass
    while length < max_complaint:
        dummy_issue = {
            "COMPLAINT": "N/A",
            "RAISE_DATE": "N/A",
            "TARGET_DATE": "N/A",
            "STATUS": "N/A",
            "RESPONSIBILITY": "N/A"
        }
        datas.append(dummy_issue)
        max_complaint = max_complaint-1
    
    col1,col2,col3 = st.columns((1,1,1))
    with col1:
        st.subheader(f"Total Complaints: {total_complaints}")
    with col2:
        pass
    with col3:
        pass
    
    status_clr = []
    def stat_clr( clr_name):
        if clr_name == 'Open':
            clr = '#fa2323'
            return clr
        elif clr_name == 'Inprocess':
            clr = '#e9f76a'
            return clr
        elif clr_name == 'Closed':
            clr = '#5fe650'
            return clr
        else:
            clr = '#dff2dc'
            return clr
    
    statuses = [datas[0]["STATUS"], datas[1]["STATUS"], datas[2]["STATUS"], datas[3]["STATUS"], datas[4]["STATUS"], datas[5]["STATUS"]]
    for status in statuses:
        status_clr_value = stat_clr(status)
        status_clr.append(status_clr_value)

    st.markdown(f"""
        <style>
                .float-container {{  padding: 5px;   }}
                .float-cd {{width: 35%; font-size:1rem; font-weight:bold; float: left; font-weight:bold; height:20rem; text-align:center; padding: 10px; border: 1px solid black;}}
                .float-dr {{width: 16%; font-size:1rem; font-weight:bold; float: left; font-weight:bold; height:20rem; text-align:center; padding: 10px; border: 1px solid black;}}
                .float-dc {{width: 16%; font-size:1rem; font-weight:bold; float: left; font-weight:bold; height:20rem; text-align:center; padding: 10px; border: 1px solid black;}}
                .float-st {{width: 16%; font-size:1rem; font-weight:bold; float: left; font-weight:bold; height:20rem; text-align:center; padding: 10px; border: 1px solid black;}}
                .par {{padding-top:0.5rem; font-size:0.9rem; color:black; }}
                .color{{ background-color: red;}}
                hr{{ margin:0em; }}
                
        </style>
        <div class="float-container">
            <div class="float-cd">Complaint details<hr>
                <p class="par">{datas[0]["COMPLAINT"]}</p>
                <p class="par">{datas[1]["COMPLAINT"]}</p>
                <p class="par">{datas[2]["COMPLAINT"]}</p>
                <p class="par">{datas[3]["COMPLAINT"]}</p>
                <p class="par">{datas[4]["COMPLAINT"]}</p>
                <p class="par">{datas[5]["COMPLAINT"]}</p>
            </div>
            <div class="float-dr">Raised<hr>
                <p class="par">{datas[0]["RAISE_DATE"]}</p>
                <p class="par">{datas[1]["RAISE_DATE"]}</p>
                <p class="par">{datas[2]["RAISE_DATE"]}</p>
                <p class="par">{datas[3]["RAISE_DATE"]}</p>
                <p class="par">{datas[4]["RAISE_DATE"]}</p>
                <p class="par">{datas[5]["RAISE_DATE"]}</p>
            </div>
            <div class="float-dc">Responsibility<hr>
                <p class="par">{datas[0]["RESPONSIBILITY"]}</p>
                <p class="par">{datas[1]["RESPONSIBILITY"]}</p>
                <p class="par">{datas[2]["RESPONSIBILITY"]}</p>
                <p class="par">{datas[3]["RESPONSIBILITY"]}</p>
                <p class="par">{datas[4]["RESPONSIBILITY"]}</p>
                <p class="par">{datas[5]["RESPONSIBILITY"]}</p>
            </div>
            <div class="float-dc">Close<hr>
                <p class="par">{datas[0]["TARGET_DATE"]}</p>
                <p class="par">{datas[1]["TARGET_DATE"]}</p>
                <p class="par">{datas[2]["TARGET_DATE"]}</p>
                <p class="par">{datas[3]["TARGET_DATE"]}</p>
                <p class="par">{datas[4]["TARGET_DATE"]}</p>
                <p class="par">{datas[5]["TARGET_DATE"]}</p>
            </div>
            <div class="float-st">Status<hr>
                <p class="par" style='background-color:{status_clr[0]};'>{datas[0]["STATUS"]}</p>
                <p class="par" style='background-color:{status_clr[1]};'>{datas[1]["STATUS"]}</p>
                <p class="par" style='background-color:{status_clr[2]};'>{datas[2]["STATUS"]}</p>
                <p class="par" style='background-color:{status_clr[3]};'>{datas[3]["STATUS"]}</p>
                <p class="par" style='background-color:{status_clr[4]};'>{datas[4]["STATUS"]}</p>
                <p class="par" style='background-color:{status_clr[5]};'>{datas[5]["STATUS"]}</p>
            </div>
        </div>
    """,unsafe_allow_html=True)

    # st.subheader("Customer Complaints Trend:")
    target_data = fetch_data("SET DAILY TARGET")
    target_data = target_data[target_data["CATEGORY"] == 'Customer Complaint']
    monthly_target = target_data[((target_data["DATE"].dt.to_period("M")) == current_month)]
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:   # ****** Daily_Data ****** #
        desired_data = month_data[month_data['DATE'].dt.strftime('%U') == current_week_number]
        daily_data_count = desired_data.groupby(desired_data['DATE'].dt.to_period('D')).size().reset_index(name='data')
        desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')  # Day format in weekdays
        unique_desired_data = desired_data.drop_duplicates(subset='Day', keep='first')
        desired_trgt = monthly_target[monthly_target['DATE'].dt.strftime('%U') == current_week_number]
        desired_trgt['DATE'] = desired_trgt['DATE'].dt.strftime("%Y-%m-%d")
        daily_data_count['DATE'] = daily_data_count['DATE'].dt.strftime("%Y-%m-%d") # Convert 'DATE' to a string in both DataFrames for merging
        merged_data = pd.merge(daily_data_count, desired_trgt, on='DATE')  # Merge on the 'DATE' column
        merged_data['color'] = np.where(merged_data['data'] >= merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(unique_desired_data['Day'], merged_data['data'], merged_data['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='count', line=dict(color=my_color, width=30), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=unique_desired_data['Day'], y=merged_data['VALUE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)
    with cl2:   # ****** Weekly_Data ****** #
        weekly_data = month_data.groupby(month_data['DATE'].dt.to_period('W')).size()
        weekly_trgt = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum()
        weekly_data = pd.DataFrame({'my_data': weekly_data})
        merged_data = pd.merge(weekly_data, weekly_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        fig = go.Figure(data=[
            go.Bar(
                x=list(weekly_data['WEEKLY_NUMBER']),  # Convert range to list
                y=merged_data['my_data'],
                marker_color=[color for color in merged_data['color']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    with cl3:   # ****** Monthly_Data ****** #
        monthly_data = df.groupby(df['DATE'].dt.to_period('M')).size()
        monthly_target = target_data.groupby(target_data['DATE'].dt.to_period('M'))['VALUE'].sum()
        monthly_data = pd.DataFrame({'my_data': monthly_data})
        merged_data = pd.merge(monthly_data, monthly_target, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        monthly_data.index = monthly_data.index.strftime('%b')
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=merged_data['my_data'], marker_color=[color for color in merged_data['color']],)])
        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
        pass
    
    st.subheader("Get data acording to the status")
    col1,col2,col3,col4 = st.tabs(['Clear',':red[Open Status]',':green[Close Status]',':orange[Inprocessing]'])
    with col1:
        st.write("Please choose option for showing data!")
    with col2:
        open_data = df
        open_data = open_data[open_data["STATUS"] == "Open"]
        st.table(open_data[["DATE", "COMPLAINT", "RAISE DATE", "TARGET DATE", "RESPONSIBILITY", "STATUS"]])
    with col3:
        close_data = df
        close_data = close_data[close_data["STATUS"] == "Closed"]
        st.table(close_data[["DATE", "COMPLAINT", "RAISE DATE", "TARGET DATE", "RESPONSIBILITY", "STATUS"]])
    with col4:
        inprocessing = df
        inprocessing = inprocessing[inprocessing["STATUS"] == "Inprocess"]
        st.table(inprocessing[["DATE", "COMPLAINT", "RAISE DATE", "TARGET DATE", "RESPONSIBILITY", "STATUS"]])

def plant_supplier_ppm():   # ******** Plant PPM & Supplier PPM ******** #
    current_date()
    current_month = pd.Timestamp('now').to_period('M')
    d_data = fetch_data("PLANT PPM & SUPPLIER PPM")
    # d_data['DATE']=pd.to_datetime(d_data["DATE"])
    # hp_data = d_data[(d_data['CATEGORY'] == 'PLANT PPM') & (d_data['DATE'].dt.to_period('M') == current_month)]
    hp_data = fetch_month_data("PLANT PPM & SUPPLIER PPM")
    # hp_data['DATE']=pd.to_datetime(hp_data["DATE"])

    ppm_data = fetch_month_data("PLANT PPM & SUPPLIER PPM")
    filter_plant_data = ppm_data[ppm_data["CATEGORY"] == "PLANT PPM"]
    filter_supplier_data = ppm_data[ppm_data["CATEGORY"] == "SUPPLIER PPM"]
    # st.write(filter_supplier_data)
    total_plant_target = round(filter_plant_data['TARGET'].mean(), 2)    # Sum all the values in the "Value" column
    total_plant_quantity = filter_plant_data['QUANTITY'].sum()
    total_plant_rejection = filter_plant_data['REJECTION'].sum()
    if total_plant_rejection == 0 and total_plant_quantity == 0:
        total_plant_actual = 0
    else:
        total_plant_actual = round(((total_plant_rejection / total_plant_quantity) * 1000000), 2)
    total_supplier_target = round(filter_supplier_data['TARGET'].mean(), 2)
    total_supplier_quantity = filter_supplier_data['QUANTITY'].sum()
    total_supplier_rejection = filter_supplier_data['REJECTION'].sum()
    if total_plant_rejection == 0 and total_plant_quantity == 0:
        total_supplier_actual = 0
    else:
        total_supplier_actual = round(((total_supplier_rejection / total_supplier_quantity) * 1000000), 2)

    # st.write(f"total value is = {total_moth_target}")
    ppm_problem = fetch_month_data("PPM PROBLEMS")
    plant_prob = []
    supplier_prob = []
    plant_filter = ppm_problem[ppm_problem["CATEGORY"] == "PLANT PPM"]
    supplier_filter = ppm_problem[ppm_problem["CATEGORY"] == "SUPPLIER PPM"]
    plant_length = len(plant_filter)
    supplier_length = len(supplier_filter)
    plant_max_issues = 3
    supplier_max_issues = 3
    for index, row in plant_filter.iterrows():
        issue = {
            "PROBLEM": row["PROBLEM"],
            "PART_LINE": row["PART_LINE"],
            "REJ_QTY": row["REJ_QTY"]
        }
        plant_prob.append(issue)
        pass
    while plant_length < plant_max_issues:
        dummy_issue = {
            "PROBLEM": "N/A",
            "PART_LINE": "N/A",
            "REJ_QTY": "N/A"
        }
        plant_prob.append(dummy_issue)
        plant_max_issues = plant_max_issues-1

    for index, row in supplier_filter.iterrows():
        issue = {
            "PROBLEM": row["PROBLEM"],
            "PART_LINE": row["PART_LINE"],
            "REJ_QTY": row["REJ_QTY"]
        }
        supplier_prob.append(issue)
        pass
    while supplier_length < supplier_max_issues:
        dummy_issue = {
            "PROBLEM": "N/A",
            "PART_LINE": "N/A",
            "REJ_QTY": "N/A"
        }
        supplier_prob.append(dummy_issue)
        supplier_max_issues = supplier_max_issues-1
    cl1,cl2=st.columns((1,2))
    with cl1:
        st.markdown(f"""<div style='margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>PLANT PPM<hr style='margin:0em;'>
                    <div style='content: ""; height:72%; display: table;display:flex;clear: both;'>
                        <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                            <h6>{total_plant_target}</h6>
                        </div>
                        <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                        <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                            <h6>{total_plant_actual}</h6>
                        </div>
                    </div>
                    </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>SUPPLIER PPM<hr style='margin:0em;'>
                    <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                        <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                            <h6>{total_supplier_target}</h6>
                        </div>
                        <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                        <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                            <h6>{total_supplier_actual}</h6>
                        </div>
                    </div>
                    </div>""",unsafe_allow_html=True)
    with cl2:
        st.markdown(f"""
        <style>
            .float-container {{ padding: 5px; }}
            .ftp_prb {{ font-size:1rem; float: left;font-weight:bold;height:8.5rem;text-align:center;padding: 10px;border: 1px solid black;
            }}
            .ftp_prb p {{ width: 100%; font-size:0.8rem; height:0.5rem; text-align:center; padding: 5px;
            }}
        </style>
        <div style='padding-top:0.5rem;'>
            <div class="float-container">
            <div class="ftp_prb" style='width:50%'>Problems<hr style='margin:0.15rem;'>
                <p >{plant_prob[0]["PROBLEM"]}</p>
                <p >{plant_prob[1]["PROBLEM"]}</p>
                <p >{plant_prob[2]["PROBLEM"]}</p>
            </div>
            <div class="ftp_prb" style='width:25%'>Part/Line<hr style='margin:0.15rem;'>
                <p >{plant_prob[0]["PART_LINE"]}</p>
                <p >{plant_prob[1]["PART_LINE"]}</p>
                <p >{plant_prob[2]["PART_LINE"]}</p>
            </div>
            <div class="ftp_prb" style='width:25%'>Rej Qty<hr style='margin:0.15rem;'>
                <p >{plant_prob[0]["REJ_QTY"]}</p>
                <p >{plant_prob[1]["REJ_QTY"]}</p>
                <p >{plant_prob[2]["REJ_QTY"]}</p>
            </div>
        </div>
        """,unsafe_allow_html=True)
        st.markdown(f"""
            <div style='padding-top:0.5rem;'>
                <div class="float-container">
                <div class="ftp_prb" style='font-weight:bold; width:50%'>Problems<hr style='margin:0.15rem;'>
                    <p >{supplier_prob[0]["PROBLEM"]}</p>
                    <p >{supplier_prob[1]["PROBLEM"]}</p>
                    <p >{supplier_prob[2]["PROBLEM"]}</p>
                </div>
                <div class="ftp_prb" style='font-weight:bold; width:25%'>Part/Line<hr style='margin:0.15rem;'>
                    <p >{supplier_prob[0]["PART_LINE"]}</p>
                    <p >{supplier_prob[1]["PART_LINE"]}</p>
                    <p >{supplier_prob[2]["PART_LINE"]}</p>
                </div>
                <div class="ftp_prb" style='font-weight:bold; width:25%'>Rej Qty<hr style='margin:0.15rem;'>
                    <p >{supplier_prob[0]["REJ_QTY"]}</p>
                    <p >{supplier_prob[1]["REJ_QTY"]}</p>
                    <p >{supplier_prob[2]["REJ_QTY"]}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    

    st.subheader("Plant PPM")
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    col1,col2,col3 = st.columns((1,1,1))
    with col1:  # ****** Daily_Data ****** #
        desired_data = hp_data[hp_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "PLANT PPM"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        new_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        new_df['color'] = np.where(new_df['ACTUAL'] < new_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(new_df['Day'], new_df['ACTUAL'], new_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', line=dict(color=my_color, width=35), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=new_df['Day'], y=new_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Actual vs Target Values', xaxis_title='Day', yaxis_title='Values')
        st.plotly_chart(fig, use_container_width=True)


        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)

    with col2:  # ****** Weekly_Data ****** #
        hp_data = hp_data[hp_data["CATEGORY"] == "PLANT PPM"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum() / 7
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=week,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:  # ****** Monthly_Data ****** #
        hp_data_month = d_data[d_data['CATEGORY'] == 'PLANT PPM']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum() / 30
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Supplier PPM")
    hp_data = d_data[(d_data['CATEGORY'] == 'SUPPLIER PPM') & (d_data['DATE'].dt.to_period('M') == current_month)]
    col1,col2,col3 = st.columns((1,1,1))
    with col1:  # ****** Daily_Data ****** #
        # hp_data = hp_data[hp_data["CATEGORY"] == "SUPPLIER PPM"]
        # st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data.index = daily_data.index.strftime('%a') 
        # st.bar_chart(daily_data, color=["#fa2323","#5fe650"])
        desired_data = hp_data[hp_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "SUPPLIER PPM"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        new_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        new_df['color'] = np.where(new_df['ACTUAL'] < new_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(new_df['Day'], new_df['ACTUAL'], new_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', line=dict(color=my_color, width=35), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=new_df['Day'], y=new_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Actual vs Target Values', xaxis_title='Day', yaxis_title='Values')
        st.plotly_chart(fig, use_container_width=True)


        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)
    
    with col2:  # ****** Weekly_Data ****** #
        # hp_data = hp_data[hp_data["CATEGORY"] == "SUPPLIER PPM"]
        # st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Weekly Trend</center>""",unsafe_allow_html=True)
        # weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        # weekly_data.index = range(1, len(weekly_data) + 1)
        # st.bar_chart(weekly_data, color=["#fa2323","#5fe650"])

        hp_data = hp_data[hp_data["CATEGORY"] == "SUPPLIER PPM"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=week,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:  # ****** Monthly_Data ****** #
        # st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Yearly Trend</center>""",unsafe_allow_html=True)
        # hp_data_month = d_data[d_data['CATEGORY'] == 'SUPPLIER PPM']
        # monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        # monthly_data.index = monthly_data.index.strftime('%b')
        # st.bar_chart(monthly_data, color=["#fa2323","#5fe650"])

        hp_data_month = d_data[d_data['CATEGORY'] == 'SUPPLIER PPM']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

    pass

def ftp_rejection():    # ******** FTP And Reported Rejection ******** #
    # st.subheader("FTP and Reported Rejection Trend")
    current_month = pd.Timestamp('now').to_period('M')
    d_data = fetch_data("FTP AND REPORTED REJECTION")
    # hp_data = d_data[(d_data['CATEGORY'] == 'First Time Pass (%)') & (d_data['DATE'].dt.to_period('M') == current_month)]
    ftp_month_data = fetch_month_data("FTP AND REPORTED REJECTION")
    st.subheader("FTP Trend")
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    d1,d2,d3,d4 = st.columns((1,1,1,1))
    col1,col2,col3 = st.columns((1,1,1))
    with col1:  # ****** Daily_Data ****** #
        desired_data = ftp_month_data[ftp_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "First Time Pass (%)"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', line=dict(color=my_color, width=40), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Values')
        st.plotly_chart(fig, use_container_width=True)

        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)
    with col2:  # ****** Weekly_Data ****** #
        hp_data = ftp_month_data[ftp_month_data["CATEGORY"] == "First Time Pass (%)"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) + 1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
            # fig.add_annotation(
            #     x=week,
            #     y=actual + 10,  # Adjust the vertical position of the text annotation
            #     text=str(target),
            #     showarrow=False,
            #     font=dict(color='black', size=15)
            # )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    with col3:  # ****** Monthly_Data ****** #
        hp_data_month = d_data[d_data['CATEGORY'] == 'First Time Pass (%)']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Reported Rejection")
    # hp_data = d_data[(d_data['CATEGORY'] == 'Reported Rejection (%)') & (d_data['DATE'].dt.to_period('M') == current_month)]
    col1,col2,col3 = st.columns((1,1,1))
    with col1:  # ****** Daily_Data ****** #
        desired_data = ftp_month_data[ftp_month_data['DATE'].dt.strftime('%U') == current_week_number]
        hp_data = desired_data[desired_data["CATEGORY"] == "Reported Rejection (%)"]

        hp_data['Day'] = hp_data['DATE'].dt.strftime('%a')  # Add a 'Day' column with abbreviated day names
        start_of_week = today_date - timedelta(days=today_date.weekday()+1)
        end_of_week = start_of_week + timedelta(days=6)
        filtered_df = hp_data[(hp_data['DATE'] >= start_of_week) & (hp_data['DATE'] <= end_of_week)]
        filtered_df['color'] = np.where(filtered_df['ACTUAL'] < filtered_df['TARGET'], '#fa2323', '#5fe650' )
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(filtered_df['Day'], filtered_df['ACTUAL'], filtered_df['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', line=dict(color=my_color, width=40), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=filtered_df['Day'], y=filtered_df['TARGET'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Values')
        st.plotly_chart(fig, use_container_width=True)


        # daily_data = hp_data.groupby(hp_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        # daily_data['COLOR'] = np.where(daily_data['ACTUAL'] >= daily_data['TARGET'], 'green', 'red')
        # # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        # colors = {'green': '#5fe650', 'red': '#fa2323'}
        # fig = go.Figure(data=[
        #     go.Bar(
        #         x=daily_data.index.strftime('%a'),
        #         y=daily_data['ACTUAL'],
        #         marker_color=[colors[color] for color in daily_data['COLOR']],
        #     ),
        # ])
        # for i, (date, target, actual) in enumerate(zip(daily_data.index, daily_data['TARGET'], daily_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date.strftime('%a'),
        #         y=actual + 5,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        # if not daily_data['ACTUAL'].empty:
        #     max_actual = daily_data['ACTUAL'].max()
        # else:
        #     max_actual = 0
        # if not daily_data['TARGET'].empty:
        #     max_target = daily_data['TARGET'].max()
        # else:
        #     max_target = 0
        # fig.update_layout(
        #     xaxis_title='Date',
        #     yaxis_title='Actual',
        #     title="Daily Trend",
        #     yaxis_range=[0, max(max_actual, max_target)]  # Set y-axis range
        # )
        # st.plotly_chart(fig, use_container_width=True)
    with col2:  # ****** Weekly_Data ****** #
        hp_data = ftp_month_data[ftp_month_data["CATEGORY"] == "Reported Rejection (%)"]
        weekly_data = hp_data.groupby(hp_data['DATE'].dt.to_period('W'))[['ACTUAL', 'TARGET']].sum()
        weekly_data['COLOR'] = np.where(weekly_data['ACTUAL'] >= weekly_data['TARGET'], 'green', 'red')
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) + 1)
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=weekly_data['WEEKLY_NUMBER'],
                y=weekly_data['ACTUAL'],
                marker_color=[colors[color] for color in weekly_data['COLOR']],
            ),
        ])
        # for i, (week, target, actual) in enumerate(zip(weekly_data['WEEKLY_NUMBER'], weekly_data['TARGET'], weekly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=week,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    with col3:  # ****** Monthly_Data ****** #
        hp_data_month = d_data[d_data['CATEGORY'] == 'Reported Rejection (%)']
        monthly_data = hp_data_month.groupby(hp_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data['COLOR'] = np.where(monthly_data['ACTUAL'] >= monthly_data['TARGET'], 'green', 'red')
        monthly_data.index = monthly_data.index.strftime('%b')
        colors = {'green': '#5fe650', 'red': '#fa2323'}
        fig = go.Figure(data=[
            go.Bar(
                x=monthly_data.index,
                y=monthly_data['ACTUAL'],
                marker_color=[colors[color] for color in monthly_data['COLOR']],
            ),
        ])
        # for i, (date, target, actual) in enumerate(zip(monthly_data.index, monthly_data['TARGET'], monthly_data['ACTUAL'])):
        #     fig.add_annotation(
        #         x=date,
        #         y=actual + 10,  # Adjust the vertical position of the text annotation
        #         text=str(target),
        #         showarrow=False,
        #         font=dict(color='black', size=15)
        #     )
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

    ftp_rej = fetch_data("FTP AND REPORTED REJECTION")
    current_month = datetime.datetime.now().month
    ftp_rej['DATE'] = pd.to_datetime(ftp_rej['DATE']) # Convert the "DATE" column to datetime
    filtered_ftp_rej = ftp_rej[ftp_rej['DATE'].dt.month == current_month]
    sum_ftp_target = filtered_ftp_rej[filtered_ftp_rej["CATEGORY"] == "First Time Pass (%)"]["TARGET"].sum()
    sum_ftp_actual = filtered_ftp_rej[filtered_ftp_rej["CATEGORY"] == "First Time Pass (%)"]["ACTUAL"].sum()
    sum_rrp_target = filtered_ftp_rej[filtered_ftp_rej["CATEGORY"] == "Reported Rejection (%)"]["TARGET"].sum()
    sum_rrp_actual = filtered_ftp_rej[filtered_ftp_rej["CATEGORY"] == "Reported Rejection (%)"]["ACTUAL"].sum()
    sum_rri_target = filtered_ftp_rej[filtered_ftp_rej["CATEGORY"] == "Reported Rejection (INR)"]["TARGET"].sum()
    sum_rri_actual = filtered_ftp_rej[filtered_ftp_rej["CATEGORY"] == "Reported Rejection (INR)"]["ACTUAL"].sum()
    
    st.markdown(f"""
                <style>
                     .float-container {{ padding: 5px;   }}
                     .float-prb {{ width: 55%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }}
                    .float-prt {{ width: 20%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }}
                    .float-pn {{width: 20%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .float-ir {{width: 40%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .float-ca {{width: 20%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .float-td {{width: 15%;font-size:0.8rem; float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }}
                    .par {{padding-top:0.6rem; font-size:0.8rem; color:black; }}
                    hr{{ margin:0em; }}
                </style>
                <div>
                     <div class="float-container">
                        <div class="float-prb" style='height:10rem; font-size:1rem;'>Particular <hr>
                        <p class="par" style='font-weight:bold;'>Firtst Time Pass % (FTP)</p>
                        <p class="par" style='font-weight:bold;'>Reported Rejection (Percntage)</p>
                        <p class="par" style='font-weight:bold;'>Reported Rejection (INR)</p>
                    </div>
                        <div class="float-prt" style='height:10rem; font-size:1rem'>Target <hr>
                        <p class="par">{sum_ftp_target}</p>
                        <p class="par">{sum_rrp_target}</p>
                        <p class="par">{sum_rri_target}</p>
                    </div>
                        <div class="float-prt" style='height:10rem; font-size:1rem'>Actual <hr>
                        <p class="par">{sum_ftp_actual}</p>
                        <p class="par">{sum_rrp_actual}</p>
                        <p class="par">{sum_rri_actual}</p>
                    </div>
                </div>
                    
            """,unsafe_allow_html=True)

    fr_issue = fetch_data("FTP REJECTION ISSUE")
    fr_issue['DATE'] = pd.to_datetime(fr_issue['DATE']) # Convert the "DATE" column to datetime
    filtered_fr_issue = fr_issue[fr_issue['DATE'].dt.month == current_month]
    myfr_issue = []
    length = len(filtered_fr_issue)
    fr_max_issues = 3
    for index, row in filtered_fr_issue.iterrows():
        issue = {
            "PART_NO": row["PART NO"],
            "ISSUE": row["ISSUE"],
            "ACTION": row["CORRECTIVE ACTION"],
            "T_DATE": row["TARGET DATE"]
        }
        myfr_issue.append(issue)
        pass
    while length < fr_max_issues:
        dummy_issue = {
            "PART_NO": "N/A",
            "ISSUE": "N/A",
            "ACTION": "N/A",
            "T_DATE": "N/A"
        }
        myfr_issue.append(dummy_issue)
        fr_max_issues = fr_max_issues-1
    st.markdown(f"""
        <div class="float-container">
            <div class="float-pn">Part number<hr>
                <p class="par">{myfr_issue[0]["PART_NO"]}</p>
                <p class="par">{myfr_issue[1]["PART_NO"]}</p>
                <p class="par">{myfr_issue[2]["PART_NO"]}</p>
            </div>
            <div class="float-ir">Issue Reported<hr>
                <p class="par">{myfr_issue[0]["ISSUE"]}</p>
                <p class="par">{myfr_issue[1]["ISSUE"]}</p>
                <p class="par">{myfr_issue[2]["ISSUE"]}</p>
            </div>
            <div class="float-ca">Corrective Action<hr>
                <p class="par">{myfr_issue[0]["ACTION"]}</p>
                <p class="par">{myfr_issue[1]["ACTION"]}</p>
                <p class="par">{myfr_issue[2]["ACTION"]}</p>
            </div>
            <div class="float-td">Targate Date<hr>
                <p class="par">{myfr_issue[0]["T_DATE"]}</p>
                <p class="par">{myfr_issue[1]["T_DATE"]}</p>
                <p class="par">{myfr_issue[2]["T_DATE"]}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

#************************** Quality_FTD End **************************#


#************************** Letters Start **************************#
def S_letter():
    # Parse the existing SVG file
    tree = ET.parse('resources\S.svg')
    root = tree.getroot()
    current_date = datetime.date.today()

    row_data = fetch_month_data("INCIDENCES DETAILS")
    first_day_of_month = current_date.replace(day=1)
    days_to_add = 0
    for i in range(1, 32):
        colors = {
                "record_lost_time": False, "record_accident": False,
                "first_aid": False, "near_mis": False, "fire_mtd": False
            }
        if i < 10:
            target_element = root.find(f".//*[@id='untitled-u-day{i}']")
        else:
            target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
        new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
        days_to_add += 1
        df = row_data[row_data["DATE"] == f"{new_date}"]
        if len(row_data) == 0:
            if new_date.weekday() == 6:
                target_element.set('fill', '#2f52ed')
                tree.write('s_out.svg')
            else:
                target_element.set('fill', '#4cf02b')
                tree.write('s_out.svg')
        elif new_date.weekday() == 6:
                target_element.set('fill', '#2f52ed')
                tree.write('s_out.svg')
        else:
            for index, row in df.iterrows():
                if row["CATEGORY"] == "Recordable Loss Time Injury":
                    colors["record_lost_time"] = True
                if row["CATEGORY"] == "Recordable Accident":
                    colors["record_accident"] = True
                if row["CATEGORY"] == "First Aid":
                    colors["first_aid"] = True
                if row["CATEGORY"] == "Near MIS":
                    colors["near_mis"] = True
                if row["CATEGORY"] == "Fire":
                    colors["fire_mtd"] = True
                
                if new_date.weekday() == 6: color = "#2f52ed"
                else:
                    if colors["record_lost_time"] == True: color = "#fa3232"
                    elif colors["record_accident"] == True: color = "#ed77a4"
                    elif colors["first_aid"] == True: color = "orange"
                    elif colors["near_mis"] == True: color = "yellow"
                    elif colors["fire_mtd"] == True: color = "#2f52ed"
                    else: color = "green"
                target_element.set('fill', color)
                tree.write('s_out.svg')

    # Display the modified SVG using Streamlit
    with open('s_out.svg', 'r') as f:
        svg = f.read()
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s" style="height:12rem;"/>' % b64
        st.write(f"""
                 <style>
                    .s{{ font-size:0.6rem; margin:0rem; position:absolute; font-weight:bold;}}
                 </style>
                 <div>{html}
                    <p class="s" style='left:15rem; top:1rem; color:black;'>LEGEND:</p>
                    <p class="s" style='left:15rem; top:2.5rem; color:#fa3232;'>RECORDABLE LOST TIME ENJURY</p>
                    <p class="s" style='left:15rem; top:4rem; color:#ed77a4;'>RECORDABLE ACCIDENT</p>
                    <p class="s" style='left:15rem; top:5.5rem; color:orange;'>FIRST AID</p>
                    <p class="s" style='left:15rem; top:7rem; color:yellow;'>NEAR MISS</p>
                    <p class="s" style='left:15rem; top:8.5rem; color:blue;'>FIRE</p>
                    <p class="s" style='left:15rem; top:10rem; color:green;'>NO INCIDENT</p>
                 </div>""", unsafe_allow_html=True)
        df = fetch_data("INCIDENCES DETAILS")
        lti_events = df[df["CATEGORY"] == "Recordable Loss Time Injury"]
        if not lti_events.empty:
            # Get the most recent event date
            last_event_date = lti_events["DATE"].max()
            # Calculate the number of days since the last event
            last_event_date = pd.Timestamp(last_event_date).to_pydatetime()
            # last_event_date = datetime.datetime.strptime(last_event_date, "%Y-%m-%d")
            today = datetime.datetime.today()
            days_since_last_event = (today - last_event_date).days
            st.markdown(
                    f"""<center style = "height:2rem;">
                    <br>
                    <p style = "font-size:13px;"><b>{days_since_last_event}</b> days without any recordable lost time injury.</p>
                    </center>
                    """, unsafe_allow_html=True
                )
        else:
            st.markdown(
                    f"""<center style = "height:2rem;">
                    <br>
                    <p style = "font-size:13px;"><b>0</b> days without any recordable lost time injury.</p>
                    </center>
                    """, unsafe_allow_html=True
                )

def Q_letter():
    # Parse the existing SVG file
    tree = ET.parse('resources\Q.svg')
    root = tree.getroot()
    current_date = datetime.date.today()
    total_days = (current_date.day)
    row_data = fetch_month_data("CUSTOMER COMPLAINTS")
    first_day_of_month = current_date.replace(day=1)
    days_to_add = 0
    for i in range(1, 32):
        if i < 10:
            target_element = root.find(f".//*[@id='q-u-day{i}']")
        else:
            target_element = root.find(f".//*[@id='q-u-day{i}_']")
        new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
        days_to_add += 1
        df = row_data[row_data["DATE"] == f"{new_date}"]
        if len(row_data) == 0:
            if new_date.weekday() == 6: color = "#2f52ed"
            else:
                color = '#d2dbed'
        else:
            if new_date.weekday() == 6: color = "#2f52ed"
            elif i <= total_days:
                count_problem = len(df["COMPLAINT"])
                if new_date.weekday() == 6: color = "#2f52ed"
                else:
                    if count_problem > 0: color = '#fa3232'
                    else: color = '#4cf02b'
            else: color = "#d2dbed"
        target_element.set('fill', color)
        tree.write('q.svg')
    # Display the modified SVG using Streamlit
    with open('q.svg', 'r') as f:
        svg = f.read()
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s" style="height:12rem;"/>' % b64
        st.write(f"""
            <style>
                .s{{ font-size:0.6rem; margin:0rem; position:absolute; font-weight:bold;}}
            </style>
            <div>{html}
                <p class="s" style='left:15rem; top:1rem; color:black;'>LEGEND:</p>
                <p class="s" style='left:15rem; top:2.5rem; color:#4cf02b;'>TARGET ACHIEVED</p>
                <p class="s" style='left:15rem; top:4rem; color:#fa3232;'>TARGET MISSED</p>
                <p class="s" style='left:15rem; top:5.5rem; color:#2f52ed;'>PLANT OFF</p>
            </div>""", unsafe_allow_html=True)
        
        df = fetch_data("CUSTOMER COMPLAINTS")
        # lti_events = df[df["CATEGORY"]]
        if not df.empty:
            # Get the most recent event date
            last_event_date = df["DATE"].max()
            # Calculate the number of days since the last event
            last_event_date = pd.Timestamp(last_event_date).to_pydatetime()
            # last_event_date = datetime.datetime.strptime(last_event_date, "%Y-%m-%d")
            today = datetime.datetime.today()
            days_since_last_event = (today - last_event_date).days
            st.markdown(f"""
                        <center style = "height:2rem;"> <br> <p style = "font-size:13px;"><b>{days_since_last_event}</b> days since customer complaint.</p> </center>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                        <center style = "height:2rem;"> <br> <p style = "font-size:13px;"><b>0</b> days since customer complaint.</p> </center>
                    """, unsafe_allow_html=True)

def D_letter():
    # Parse the existing SVG file
    tree = ET.parse('resources\D.svg')
    root = tree.getroot()
    current_date = datetime.date.today()
    # total_days = (current_date.day)
    row_data = fetch_month_data("OTIF_CC PDI")
    first_day_of_month = current_date.replace(day=1)
    days_to_add = 0
    for i in range(1, 32):
        if i < 10:
            target_element = root.find(f".//*[@id='d-u-day{i}']")
        else:
            target_element = root.find(f".//*[@id='d-u-day{i}_']")
        new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
        days_to_add += 1
        if len(row_data) == 0:
            if new_date.weekday() == 6:
                target_element.set('fill', '#2f52ed')
                tree.write('d.svg')
            else:
                target_element.set('fill', '#d2dbed')
                tree.write('d.svg')
        else:
            df = row_data[row_data["DATE"] == f"{new_date}"]
            filter_data = df[df["CATEGORY"] == "OE"]
            oe_target = filter_data["TARGET"]
            oe_actual = filter_data["ACTUAL"]
            comparison = np.where(oe_target > oe_actual, '#fa3232', '#4cf02b')
            if new_date.weekday() == 6: target_element.set('fill', "#2f52ed")
            else:
                for result in comparison:
                    # st.write(result)
                    color = result
                    target_element.set('fill', color)
                tree.write('d.svg')
    # Display the modified SVG using Streamlit
    with open('d.svg', 'r') as f:
        svg = f.read()
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s" style="height:12rem;"/>' % b64
        st.write(f"""
            <style>
                .s{{ font-size:0.6rem; margin:0rem; position:absolute; font-weight:bold;}}
            </style>
            <div>{html}
                <p class="s" style='left:15rem; top:1rem; color:black;'>LEGEND:</p>
                <p class="s" style='left:15rem; top:2.5rem; color:#4cf02b;'>TARGET ACHIEVED</p>
                <p class="s" style='left:15rem; top:4rem; color:#fa3232;'>TARGET MISSED</p>
                <p class="s" style='left:15rem; top:5.5rem; color:#2f52ed;'>PLANT OFF</p>
            </div>""", unsafe_allow_html=True)
        
        df = fetch_data("OTIF_CC PDI")
        oe = df[(df["CATEGORY"] == "OE") & (df["ACTUAL"] < df["TARGET"])]
        # st.write(oe)
        if not oe.empty:
            # Get the most recent event date
            last_event_date = oe["DATE"].max()
            # Calculate the number of days since the last event
            last_event_date = pd.Timestamp(last_event_date).to_pydatetime()
            # last_event_date = datetime.datetime.strptime(last_event_date, "%Y-%m-%d")
            today = datetime.datetime.today()
            days_since_last_event = (today - last_event_date).days
            st.markdown(f"""
                    <center style = "height:2rem;">
                        <br>
                        <p style = "font-size:13px;"><b>{days_since_last_event}</b> days since OE delivery failure. </p>
                    </center>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                    <center style = "height:2rem;">
                        <br>
                        <p style = "font-size:13px;"><b>0</b> days since OE delivery failure. </p>
                    </center>
                    """, unsafe_allow_html=True)

def C_letter():
    # Parse the existing SVG file
    tree = ET.parse('resources\C.svg')
    root = tree.getroot()
    current_date = datetime.date.today()
    total_days = (current_date.day)
    row_data = fetch_month_data("PRODUCTIVITY AND OEE")
    first_day_of_month = current_date.replace(day=1)
    days_to_add = 0
    for i in range(1, 32):
        if i < 10:
            target_element = root.find(f".//*[@id='untitled-u-day{i}']")
        else:
            target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
        # st.write(days_to_add)
        new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
        days_to_add += 1
        if len(row_data) == 0:
            if new_date.weekday() == 6:
                target_element.set('fill', '#2f52ed')
                tree.write('c.svg')
            else:
                target_element.set('fill', '#d2dbed')
                tree.write('c.svg')
        else:
            df = row_data[row_data["DATE"] == f"{new_date}"]
            filter_data = df[df["CATEGORY"] == "HUMAN PRODUCTIVITY"]
            oe_target = filter_data["TARGET"]
            oe_actual = filter_data["ACTUAL"]
            comparison = np.where(oe_target > oe_actual, '#fa3232', '#4cf02b')
            if new_date.weekday() == 6: target_element.set('fill', "#2f52ed")
            else:
                for result in comparison:
                    color = result
                    target_element.set('fill', color)
                tree.write('c.svg')
    # Display the modified SVG using Streamlit
    with open('c.svg', 'r') as f:
        svg = f.read()
        b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
        html = r'<img src="data:image/svg+xml;base64,%s" style="height:12rem;"/>' % b64
        st.write(f"""
            <style>
                .s{{ font-size:0.6rem; margin:0rem; position:absolute; font-weight:bold;}}
            </style>
            <div>{html}
                <p class="s" style='left:15rem; top:1rem; color:black;'>LEGEND:</p>
                <p class="s" style='left:15rem; top:2.5rem; color:#4cf02b;'>TARGET ACHIEVED</p>
                <p class="s" style='left:15rem; top:4rem; color:#fa3232;'>TARGET MISSED</p>
                <p class="s" style='left:15rem; top:5.5rem; color:#2f52ed;'>PLANT OFF</p>
            </div>""", unsafe_allow_html=True)
        
        df = fetch_data("PRODUCTIVITY AND OEE")
        human_productivity_missed = df[(df["CATEGORY"] == "HUMAN PRODUCTIVITY") & (df["ACTUAL"] < df["TARGET"])]
        # st.write(oe)
        if not human_productivity_missed.empty:
            # Get the most recent event date
            last_event_date = human_productivity_missed["DATE"].max()
            # Calculate the number of days since the last event
            last_event_date = pd.Timestamp(last_event_date).to_pydatetime()
            # last_event_date = datetime.datetime.strptime(last_event_date, "%Y-%m-%d")
            today = datetime.datetime.today()
            days_since_last_event = (today - last_event_date).days
            st.markdown(f"""
                        <center style = "height:2rem;">
                        <br>
                <p style = "font-size:13px;"><b>{days_since_last_event}</b> days since productivity target missed. </p>
                    </center>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                        <center style = "height:2rem;">
                        <br>
                <p style = "font-size:13px;"><b>0</b> days since productivity target missed. </p>
                    </center>
                    """, unsafe_allow_html=True)

#************************** Letters End **************************#


#************************** Personal Start **************************#
def personal_gap():
    pg_data = fetch_data("PERSONAL GAP")
    pg_data['DATE'] = pd.to_datetime(pg_data['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    current_day = pd.Timestamp('now').to_period('D')
    month_pg = pg_data[((pg_data['DATE'].dt.to_period('M')) == current_month)]
    daily_data = pg_data[((pg_data['DATE'].dt.to_period('D')) == current_day)]
    required = daily_data.iloc[0]['PLANNED MANPOWER']
    available = daily_data.iloc[0]['ACTUAL MANPOWER']
    # total_req = month_pg["PLANNED MANPOWER"].sum()
    # total_avail = month_pg["ACTUAL MANPOWER"].sum()
    total_pg = round(((required-available)/required)*100, 2)
    days = datetime.date.today()
    total_days_in_month = calendar.monthrange(days.year, days.month)[1]
    # st.write(total_pg)
    my_issue = []
    issue_len = len(month_pg)
    max_issue = 3
    for index, row in month_pg.iterrows():
        issue = row["ISSUE"]
        my_issue.append(issue)
    while(issue_len < max_issue):
        dummy_issue = "N/A"
        my_issue.append(dummy_issue)
        max_issue = max_issue-1
    
    col1, col2 = st.columns((1,1))
    with col1:
        st.markdown(f"""
                <style>
                .custom {{
                    margin: 0.7rem;
                    padding-top: 1rem;
                    border: 1px solid black;
                    height: 8rem;
                    font-size:1.15rem;
                    border-radius: 0.7rem;
                    font-weight: bold;
                    box-shadow: 5px 5px 10px;
                    text-align: center;
                }}
                .custom h4{{ font-weight:bold; }}
                @media (min-width: 1920px) and (max-width: 2860px){{
                    .custom {{ font-size:1.35rem; height:10rem; }}
                    .custom h4{{ font-size:1.3rem; font-weight:bold; padding-top:1rem}}
                }}
                </style>
                """,
                unsafe_allow_html=True
            )   #custom css for columns
        cr11,cr12,cr3=st.columns((1,1,1))
        with cr11:
            st.markdown(f"""<div class="custom">Planned Manpower Required
                        <h4>{required}</h4></div>""",unsafe_allow_html=True)
        with cr12:
            st.markdown(f"""<div class="custom">Actual Manpower Available
                        <h4>{available}</h4></div>""",unsafe_allow_html=True)
        with cr3:
            st.markdown(f"""<div class="custom">Personal Gap (PG)
                        <h4>{total_pg}</h4></div>""",unsafe_allow_html=True)
        pass
    with col2:
        st.markdown(f"""<style>
                    .head{{height:12rem; width:100%; border:1px solid black;}} .head h5{{padding-top:0.7rem}} .head hr{{margin:0.1em;}} .head p{{padding-top:0.3rem; overflow-wrap:break-word;}}
                    </style><div class="head"><center><h5>Top 3 Problems</h5><hr><p>{my_issue[0]}</p><p>{my_issue[1]}</p><p>{my_issue[2]}</p></center></div>""",unsafe_allow_html=True)

    st.subheader("Personal Gap Trend")
    pg_target = fetch_data("SET DAILY TARGET")
    pg_target = pg_target[pg_target["CATEGORY"] == 'Personal Gap']
    monthly_target = pg_target[((pg_target["DATE"].dt.to_period("M")) == current_month)]
    today_date = datetime.datetime.now()
    current_week_number = today_date.strftime('%U')
    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:   # ****** Daily_Data ****** #
        desired_data = month_pg[month_pg['DATE'].dt.strftime('%U') == current_week_number] #Data of current week
        desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')    #Day format in weekdays
        desired_trgt = monthly_target[monthly_target['DATE'].dt.strftime('%U') == current_week_number] #Target data of current week
        merged_data = pd.merge(desired_data, desired_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['PERSONAL GAP'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        # st.write(merged_data)
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(merged_data['Day'], merged_data['PERSONAL GAP'], merged_data['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='Personal Gap', line=dict(color=my_color, width=30), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=merged_data['Day'], y=merged_data['VALUE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Personal Gap')
        st.plotly_chart(fig, use_container_width=True)

    with cl2:   # ****** Weekly_Data ****** #
        weekly_data = month_pg.groupby(month_pg['DATE'].dt.to_period('W'))[['ACTUAL MANPOWER', 'PLANNED MANPOWER']].sum()
        weekly_data['NEW_PG'] = round(((weekly_data['PLANNED MANPOWER'] - weekly_data['ACTUAL MANPOWER'])/weekly_data['PLANNED MANPOWER'])*100, 2)
        weekly_target = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum() / 6
        merged_data = pd.merge(weekly_data, weekly_target, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['NEW_PG'] < merged_data['VALUE'], "#fa2323", "#5fe650")
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        fig = go.Figure(data=[
            go.Bar(
                x=list(weekly_data['WEEKLY_NUMBER']),  # Convert range to list
                y=merged_data['NEW_PG'],
                marker_color=[color for color in merged_data['color']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

    with cl3:   # ****** Monthly_Data ****** #
        monthly_data = pg_data.groupby(pg_data['DATE'].dt.to_period('M'))[['ACTUAL MANPOWER', 'PLANNED MANPOWER']].sum()
        monthly_target = pg_target.groupby(pg_target['DATE'].dt.to_period('M'))['VALUE'].sum() / total_days_in_month
        monthly_data['NEW_PG'] = round(((monthly_data['PLANNED MANPOWER'] - monthly_data['ACTUAL MANPOWER'])/monthly_data['PLANNED MANPOWER'])*100, 2)
        merged_data = pd.merge(monthly_data, monthly_target, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['NEW_PG'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        monthly_data.index = monthly_data.index.strftime('%b')
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=merged_data['NEW_PG'], marker_color=[color for color in merged_data['color']],)])
        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)

def visits():
    visit = fetch_month_data("VISITS OR AUDITS")
    visit_len = len(visit)
    max_visit = 7
    visit_data = []
    for index, row in visit.iterrows():
        data = {
            "date": row["DATE"],
            "purpose": row["PURPOSE"],
            "visited_by": row["VISITED BY"],
            "risponsible": row["RESPONSIBILITY"]
        }
        visit_data.append(data)
    while visit_len < max_visit:
        dummy_data = {
            "date": "N/A",
            "purpose": "N/A",
            "visited_by": "N/A",
            "risponsible": "N/A"
        }
        visit_data.append(dummy_data)
        max_visit = max_visit - 1
    # st.write(visit.to_html(escape=False, index=False), unsafe_allow_html=True)
    # st.table(visit)
    st.markdown(f"""
            <style>
                .category{{border:1px solid black; width:25%; padding-top:1rem; float:left; height: 4rem; text-align:center; font-weight:bold;}}
                .content{{border:1px solid black; width:25%; padding-top:1rem; height: 4rem; float:left; text-align:center;}}
            </style>
            <div>
                <div class="category">DATE</div>
                <div class="category">PURPOSE</div>
                <div class="category">VISITED BY</div>
                <div class="category">RESPONSIBILITY</div>
            </div>
            <div>
                <div class="content">{visit_data[0]["date"]}</div>
                <div class="content">{visit_data[0]["purpose"]}</div>
                <div class="content">{visit_data[0]["visited_by"]}</div>
                <div class="content">{visit_data[0]["risponsible"]}</div>
            </div>
            <div>
                <div class="content">{visit_data[1]["date"]}</div>
                <div class="content">{visit_data[1]["purpose"]}</div>
                <div class="content">{visit_data[1]["visited_by"]}</div>
                <div class="content">{visit_data[1]["risponsible"]}</div>
            </div>
            <div>
                <div class="content">{visit_data[2]["date"]}</div>
                <div class="content">{visit_data[2]["purpose"]}</div>
                <div class="content">{visit_data[2]["visited_by"]}</div>
                <div class="content">{visit_data[2]["risponsible"]}</div>
            </div>
            <div>
                <div class="content">{visit_data[3]["date"]}</div>
                <div class="content">{visit_data[3]["purpose"]}</div>
                <div class="content">{visit_data[3]["visited_by"]}</div>
                <div class="content">{visit_data[3]["risponsible"]}</div>
            </div>
            <div>
                <div class="content">{visit_data[4]["date"]}</div>
                <div class="content">{visit_data[4]["purpose"]}</div>
                <div class="content">{visit_data[4]["visited_by"]}</div>
                <div class="content">{visit_data[4]["risponsible"]}</div>
            </div>
            <div>
                <div class="content">{visit_data[5]["date"]}</div>
                <div class="content">{visit_data[5]["purpose"]}</div>
                <div class="content">{visit_data[5]["visited_by"]}</div>
                <div class="content">{visit_data[5]["risponsible"]}</div>
            </div>
            <div>
                <div class="content">{visit_data[6]["date"]}</div>
                <div class="content">{visit_data[6]["purpose"]}</div>
                <div class="content">{visit_data[6]["visited_by"]}</div>
                <div class="content">{visit_data[6]["risponsible"]}</div>
            </div>
        """, unsafe_allow_html=True)
    pass

def attendance_sheet():
    employees = [
        { 'date': ['2023-11-19','2023-11-20','2023-11-21','2023-11-22'], 'color': ['red', 'blue', 'yellow', 'green'] },
        { 'date': ['2023-11-20','2023-11-21','2023-11-22','2023-11-23'], 'color': ['red', 'blue', 'yellow', 'green'] },
        { 'date': ['2023-11-20','2023-11-21','2023-11-22','2023-11-23'], 'color': ['red', 'blue', 'yellow', 'green'] },
        { 'date': ['2023-11-20','2023-11-21','2023-11-22','2023-11-23'], 'color': ['red', 'blue', 'yellow', 'green'] },
        { 'date': ['2023-11-20','2023-11-21','2023-11-22','2023-11-23'], 'color': ['red', 'blue', 'yellow', 'green'] },
        { 'date': ['2023-11-20','2023-11-21','2023-11-22','2023-11-23'], 'color': ['red', 'blue', 'yellow', 'green'] },
        { 'date': ['2023-11-20','2023-11-21','2023-11-22','2023-11-23'], 'color': ['red', 'blue', 'yellow', 'green'] },
        { 'date': ['2023-11-20','2023-11-21','2023-11-22','2023-11-23'], 'color': ['red', 'blue', 'yellow', 'green'] }
    ]
    person_1 = employees[0]
    person_2 = employees[1]
    # st.dataframe(person_2['color'])
    st.markdown(f"""
        <style>
            th {{
                background-color: #001f3f;  color: #fff;  padding: 0.5em 1em;
            }}
            td {{
                border-top: 1px solid black;    padding: 0.5em 1em;
            }}
            input {{
                cursor: pointer;
            }}
            /* Column types */
            th.missed-col {{
                background-color: #f00;
            }}
            td.missed-col {{
                background-color: #ffecec;  color: #f00;  text-align: center;
            }}
            .name-col {{
                text-align: left;
            }}
        </style>
        <table>
            <thead>
                <tr>
                <th class="name-col">Employee Name</th>
                <th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th>
                <th>11</th><th>12</th><th>13</th><th>14</th><th>15</th><th>16</th><th>17</th><th>18</th><th>19</th><th>20</th>
                <th>21</th><th>22</th><th>23</th><th>24</th><th>25</th><th>26</th><th>27</th><th>28</th><th>29</th><th>30</th><th>31</th>
                </tr>
            </thead>
            <tbody>
                <tr class="student">
                    <td class="name-col">Slappy the Frog</td>
                    <td class="attend-col" style="background-color:red;">A</td> <td class="attend-col" style="background-color:yellow;">L</td>
                    <td class="attend-col" style="background-color:green;">P</td> <td class="attend-col" style="background-color:blue;">H</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Lilly the Lizard</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Paulrus the Walrus</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Gregory the Goat</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Adam the Anaconda</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Slappy the Frog</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Lilly the Lizard</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Paulrus the Walrus</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Gregory the Goat</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
                <tr class="student">
                    <td class="name-col">Adam the Anaconda</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                    <td class="attend-col">P</td> <td class="attend-col">P</td> <td class="attend-col">P</td>
                </tr>
            </tbody>
        </table>
    """, unsafe_allow_html=True)
    pass
#************************** Personal End **************************#

#************************** PSP Start **************************#
def psp_competency():
    df = fetch_data("PROBLEM SOLVING COMPETENCY")
    current_month = pd.Timestamp('now').to_period('M')
    current_month_data = fetch_month_data("PROBLEM SOLVING COMPETENCY")
    today_date = datetime.datetime.now()
    days = datetime.date.today()
    # Get the total number of days in the current month
    total_days_in_month = calendar.monthrange(days.year, days.month)[1]
    current_week_number = today_date.strftime('%U')
    desired_data = current_month_data[current_month_data['DATE'].dt.strftime('%U') == current_week_number]
    my_data = []
    data1 = []
    data2 = []
    data_length = len(desired_data)
    max_data = 6
    for index, row in desired_data.iterrows():
        if row['DATE'].weekday() == 6:
            # print("This is Sunday!")
            pass
        else:
            psc = {
                "problem_raised": row["PROBLEM RAISED"],
                "problem_solved": row["PROBLEM SOLVED"],
                "problem_wip":    row["PROBLEM WIP"],
                "psp_competency": row["PSP COMPETENCY"]
            }
            my_data.append(psc)
            data1.append(row['PSP COMPETENCY'])
            pass
        pass
    while data_length < max_data:
        dummy_psc = {
            "problem_raised": "N/A",
            "problem_solved": "N/A",
            "problem_wip": "N/A",
            "psp_competency": "N/A"
        }
        my_data.append(dummy_psc)
        max_data = max_data - 1
    st.markdown(f"""
        <style>
            .category{{border:1px solid black; width:12%; padding-top:1rem; float:left; height: 3rem; text-align:center; font-weight:bold;}}
            .content{{border:1px solid black; width:12%; padding-top:1rem; float:left; height: 3rem; text-align:center;}}
            .main_category{{border:1px solid black; width:28%; padding-top:1rem; float:left; height: 3rem; text-align:center; font-weight:bold;}}
        </style>
        <div>
            <div class="main_category">Days in Week</div>
            <div class="category">Monday</div>
            <div class="category">Tuesday</div>
            <div class="category">Wednesday</div>
            <div class="category">Thursday</div>
            <div class="category">Friday</div>
            <div class="category">Saturday</div>
        </div>
        <div>
            <div class="main_category">Problem Raised (A)</div>
            <div class="content">{my_data[0]["problem_raised"]}</div>
            <div class="content">{my_data[1]["problem_raised"]}</div>
            <div class="content">{my_data[2]["problem_raised"]}</div>
            <div class="content">{my_data[3]["problem_raised"]}</div>
            <div class="content">{my_data[4]["problem_raised"]}</div>
            <div class="content">{my_data[5]["problem_raised"]}</div>
        </div>
        <div>
            <div class="main_category">Problem Solved (B)</div>
            <div class="content">{my_data[0]["problem_solved"]}</div>
            <div class="content">{my_data[1]["problem_solved"]}</div>
            <div class="content">{my_data[2]["problem_solved"]}</div>
            <div class="content">{my_data[3]["problem_solved"]}</div>
            <div class="content">{my_data[4]["problem_solved"]}</div>
            <div class="content">{my_data[5]["problem_solved"]}</div>
        </div>
        <div>
            <div class="main_category">Problem WIP</div>
            <div class="content">{my_data[0]["problem_wip"]}</div>
            <div class="content">{my_data[1]["problem_wip"]}</div>
            <div class="content">{my_data[2]["problem_wip"]}</div>
            <div class="content">{my_data[3]["problem_wip"]}</div>
            <div class="content">{my_data[4]["problem_wip"]}</div>
            <div class="content">{my_data[5]["problem_wip"]}</div>
        </div>
        <div>
            <div class="main_category">PSP Competency %</div>
            <div class="content">{my_data[0]["psp_competency"]}%</div>
            <div class="content">{my_data[1]["psp_competency"]}%</div>
            <div class="content">{my_data[2]["psp_competency"]}%</div>
            <div class="content">{my_data[3]["psp_competency"]}%</div>
            <div class="content">{my_data[4]["psp_competency"]}%</div>
            <div class="content">{my_data[5]["psp_competency"]}%</div>
        </div>
    """, unsafe_allow_html=True)
    
    psc_target = fetch_data("SET DAILY TARGET")
    psc_target = psc_target[psc_target["CATEGORY"] == "Problem Solving Competency %"]
    monthly_target = psc_target[((psc_target["DATE"].dt.to_period('M')) == current_month)]

    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:   # ****** Daily_Data ****** #
        desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')    #Day format in weekdays
        desired_trgt = monthly_target[monthly_target['DATE'].dt.strftime('%U') == current_week_number] #Target data of current week
        merged_data = pd.merge(desired_data, desired_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['PSP COMPETENCY'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        # st.write(merged_data)
        fig = go.Figure()
        # Add a trace for each target value
        for day, actual_value, my_color in zip(merged_data['Day'], merged_data['PSP COMPETENCY'], merged_data['color']):
            fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='BD Time', line=dict(color=my_color, width=30), showlegend=False))
        # Plotting the line chart using Plotly Express
        fig.add_trace(go.Scatter(x=merged_data['Day'], y=merged_data['VALUE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
        # Update layout
        fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Actual')
        st.plotly_chart(fig, use_container_width=True)
    with cl2:   # ****** Weekly_Data ****** #
        P_raised = current_month_data.groupby(current_month_data['DATE'].dt.to_period('W'))['PROBLEM RAISED'].sum()
        P_solved = current_month_data.groupby(current_month_data['DATE'].dt.to_period('W'))['PROBLEM SOLVED'].sum()
        weekly_trgt = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum() / 6
        weekly_data = round((P_solved / P_raised) * 100, 2)
        weekly_data = pd.DataFrame({'psp_data': weekly_data})
        merged_data = pd.merge(weekly_data, weekly_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['psp_data'] < merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        weekly_data.index = weekly_data.index.astype(str)
        weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
        fig = go.Figure(data=[
            go.Bar(
                x=list(weekly_data['WEEKLY_NUMBER']),  # Convert range to list
                y=merged_data['psp_data'],
                marker_color=[color for color in merged_data['color']],
            ),
        ])
        fig.update_layout(
            xaxis_title='Week',
            yaxis_title='Total Actual',
            title="Weekly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
    with cl3:   # ****** Monthly_Data ****** #
        P_raised = df.groupby(df['DATE'].dt.to_period('M'))['PROBLEM RAISED'].sum()
        P_solved = df.groupby(df['DATE'].dt.to_period('M'))['PROBLEM SOLVED'].sum()
        weekly_trgt = monthly_target.groupby(monthly_target['DATE'].dt.to_period('M'))['VALUE'].sum() / total_days_in_month
        monthly_data = round((P_solved / P_raised) * 100, 2)
        monthly_data = pd.DataFrame({'psp_data': monthly_data})
        merged_data = pd.merge(monthly_data, weekly_trgt, on='DATE')   #Merge actual and target data in single table
        merged_data['color'] = np.where(merged_data['psp_data'] < merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
        monthly_data.index = monthly_data.index.strftime('%b')
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=merged_data['psp_data'], marker_color=[color for color in merged_data['color']],)])
        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Total Actual',
            title="Monthly Trend",
        )
        st.plotly_chart(fig, use_container_width=True)
        pass
    pass

#************************** PSP End **************************#