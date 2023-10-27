import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


#************ Body layout Start ************#
on_date = "%y-%m-%d"    #Date define for all pages
tm = "%H-%M-%S"

def  layout(head):
    st.set_page_config(layout="wide", page_title="Safety FTD", initial_sidebar_state="collapsed")
    st.markdown("""<style>.block-container { padding: 0.5rem; }</style>""", unsafe_allow_html=True)
    hide_streamlit_style = """<style># MainMenu { visibility: hidden;}footer { visibility: hidden;}</style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown("""
        <center>
            <div style="margin-bottom:0.6rem; background-color:darkblue; font-family:fantasy"><i><h1 style='color:white';>heading</h1></i></div>
        </center>""".replace("heading",str(head)),unsafe_allow_html=True
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
        }
        th {
            text-align: center;
            background-color: #f2f2f2;
        }
        </style>
    """, unsafe_allow_html=True)

def current_updates():
    d_col1, d_col2=st.columns((1,0.3))
    with d_col1:
        st.link_button("Home","/App")
    with d_col2:
        global on_date
        on_date = st.date_input(":green[Select Date:]")

def current_date():
    d_col1, d_col2=st.columns((1,0.3))
    with d_col1:
        st.link_button("Home","/App")
    with d_col2:
        date = datetime.now().date().strftime("%d-%m-%y")
        st.markdown(f"""<center style='padding-top:1rem;'><div style=' width:75%;background-color:lightgray;'>Date: {date}</center></div>""",unsafe_allow_html=True)
    st.markdown("___")
#************ Body layout End ************#

#************ Bar Graph Start ************#
def bar_graph(table_name):
    df = fetch_data(f"{table_name}")
    df['DATE'] = pd.to_datetime(df['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    cmplnt_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    total_complaints = len(cmplnt_data)
    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:
        # ****** Daily_Data ****** #
        st.markdown("")
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
        daily_data = cmplnt_data.groupby(cmplnt_data['DATE'].dt.to_period('D')).size()
        daily_data.index = daily_data.index.strftime('%b %d')
        daily_color = ["#fa2323" if value > 3 else "#5fe650" for value in daily_data]
        fig = go.Figure(data=[go.Bar(x=daily_data.index, y=daily_data, marker_color=daily_color)])
        # Customize the chart layout
        fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Days', yaxis_title='Values')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
        # st.bar_chart(daily_data, color=daily_color, height=387)
    with cl2:
        # ****** Weekly_Data ****** #
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Weekly Trend</center>""",unsafe_allow_html=True)
        weekly_data = cmplnt_data.groupby(cmplnt_data['DATE'].dt.to_period('W')).size()
        weekly_data.index = range(1, len(weekly_data) + 1)
        weekly_color = ["#fa2323" if value > 3 else "#5fe650" for value in weekly_data]
        fig = go.Figure(data=[go.Bar(x=weekly_data.index, y=weekly_data, marker_color=weekly_color)])
        # Customize the chart layout
        fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Weeks', yaxis_title='Values')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
        # st.bar_chart(weekly_data, color="#ff0000")
    with cl3:
        # ****** Monthly_Data ****** #
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Monthly Trend</center>""",unsafe_allow_html=True)
        monthly_data = df.groupby(df['DATE'].dt.to_period('M')).size()
        monthly_data.index = monthly_data.index.strftime('%b')
        monthly_color = ["#fa2323" if value > 3 else "#5fe650" for value in monthly_data]
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=monthly_data, marker_color=monthly_color)])
        # Customize the chart layout
        fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Months', yaxis_title='Values')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
        # st.bar_chart(monthly_data, color="#ff0000", height=363)
    pass

#************ Bar Graph End ************#

#************ Main Data Fetch Start ************#
def fetch_data(table_name):
    with sqlite3.connect("database/main_database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        table_names = [table[0] for table in table_names]
        query = f"SELECT * FROM \"{table_name}\";"
        dataframe = pd.read_sql_query(query, conn)
    return dataframe
    
# class fetch_data():
#     """Main database fetch.
        
#         Parameters:
#             table_name (str): Table name where from want to get data. 
#             ex = 'INCIDENCES DETAILS'
#     """
#     def __init__(self, table_name): #Class is initialized with the name of a table
#         self.table_name = table_name
#         with sqlite3.connect("database/main_database.db") as conn:
#         # Get a list of all table names in the database
#             cursor = conn.cursor()
#             cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#             table_names = cursor.fetchall()
#             table_names = [table[0] for table in table_names]
#             # Create a dictionary to store DataFrames for each table
#             dataframes = {}
#             # Fetch data from each table and store it in a DataFrame
#             # st.write(table_names)
#             for table_name in table_names:
#                 query = f"SELECT * FROM \"{table_name}\";"
#                 dataframes[table_name] = pd.read_sql_query(query, conn)
#         if self.table_name in dataframes:
#             self.df = dataframes[self.table_name]
#             pass
#         else:
#             st.write("Table is not available from this name")
#         pass
#     def get_specific_data(self, clm_name, spec_data):   #Specific type of data
#         """Get specific data
        
#             Parameters:
#                 column_name (str): Column name want from which column's data.
#                 ex = 'DATE'

#                 specific_data (str): Specific data in the column.
#                 ex = '2023-10-16'
#         """
#         self.clm_name = clm_name
#         self.spec_data = spec_data
#         try:
#             self.filter_data = self.df[self.df[self.clm_name] == self.spec_data]
#             # st.table(filter_data)
#         except KeyError:
#             st.write("Column not found in the table.")
#         if hasattr(self, 'filter_data'):
#             if self.table_name == "INCIDENCES DETAILS":
#                 st.table(self.filter_data[["DATE", "TIME", "CATEGORY", "VALUE STREAM", "EVENT", "ACTION", "STATUS"]])
#             elif self.table_name == "OTIF_CC PDI":
#                 st.table(self.filter_data[["DATE", "CATEGORY", "TARGET", "ACTUAL"]])
#             elif self.table_name == "VISITS":
#                 st.table(self.filter_data[["DATE", "Purpose of Visit", "Visited by Customer or Auditor", "Remarks or Responsibility"]])
#             else:
#                 st.table(self.filter_data)
#         pass
#     def get_data(self): #Get complete data from table
#         return self.df

#************ Main Data Fetch End ************#

#************************** Safety_FTD Start **************************#
class data():
    def __init__(self, incident, time, location, medical, action):
        self.incident = incident
        self.time = time
        self.location = location
        self.medical = medical
        self.action = action
    def show(self):
        return f"incident{self.incident} at time {self.time} on location {self.location}, medical given {self.medical} and take action {self.action}"
 
def fatch_incident_data():
    try:
        sconn = sqlite3.connect("database/safety.db")
        cursor = sconn.cursor()
        specific_date = on_date
        query = "SELECT * FROM 'UNSAFE INCIDENCES' WHERE Date = ?"
        cursor.execute(query, (specific_date,))
        rows = cursor.fetchall()
        sconn.close()
        return rows
    except sqlite3.Error as e:
        print("Database error: ", str(e))

def safety_ftd():
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
            if row["DATE"] == f"{on_date}":
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

        st.subheader(f"Status as on: {on_date}", divider="gray")
        st.markdown(
            """
            <style>
            .custom {
                margin: 1rem;
                padding-top: 1.3rem;
                border: 1px solid black;
                height: 8rem;
                border-radius: 0.7rem;
                font-weight: bold;
                box-shadow: 5px 5px 10px;
                text-align: center;
            }
            .custom h4{ color:white;font-weight:bold; }
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
            st.markdown(f"""<div class="custom" style='background-color:tomato;'>Recordable Accident FTD:
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
        row_data = fetch_data("INCIDENCES DETAILS")
        for index, row in row_data.iterrows():
            #Insert columns data in incident 
            incident = data(row['EVENT'], row['TIME'], row['VALUE STREAM'], row['MEDICAL'], row['ACTION'])
            if row["DATE"] == f"{on_date}":
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
            elif colors["record_accident"] == True: color = "darkred"
            elif colors["first_aid"] == True: color = "orange"
            elif colors["near_mis"] == True: color = "yellow"
            elif colors["fire_mtd"] == True: color = "blue"
            else: color = "green"
        col1,col2=st.columns((1,1.7))
        with col1:
            st.markdown(f"""
                <style>
                    .svg-container {{
                        width: 100%;
                        max-width: 100%; /* Ensure the container is responsive */
                        overflow: hidden; /* Hide the overflowing content */
                        height: 100vh;
                        text-align: center;
                    }}
                </style>
                <div class="svg-container">
                    <svg height="100%" width="100%">
                        <text x="20%" y="50%" font-size="60vh" font-weight="bold" text-anchor="middle" alignment-baseline="middle" fill={color}>S</text>
                        <text x="50%" y="15%" font-size="2vh" font-weight="bold" fill="black">LEGEND:</text>
                        <text x="50%" y="25%" font-size="2vh" font-weight="bold" fill="red">RECORDABLE LOST TIME ENJURY</text>
                        <text x="50%" y="35%" font-size="2vh" font-weight="bold" fill="darkred">RECORDABLE ACCIDENT</text>
                        <text x="50%" y="45%" font-size="2vh" font-weight="bold" fill="orange">FIRST AID</text>
                        <text x="50%" y="56%" font-size="2vh" font-weight="bold" fill="yellow">NEAR MISS</text>
                        <text x="50%" y="65%" font-size="2vh" font-weight="bold" fill="blue">FIRE</text>
                        <text x="50%" y="75%" font-size="2vh" font-weight="bold" fill="green">NO INCIDENT</text>
                    </svg>
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                        <style>
                            .float-container {{ padding: 5px; }}
                            .float-cat {{ width: 15%; font-size:0.7rem; float: left; height:8rem; text-align:center; padding: 10px; border: 2px solid black;}}
                            .float-inc {{ width: 40%; font-size:0.7rem; float: left; height:8rem; text-align:center; padding: 2.5rem; border: 2px solid black;}}
                            .float-date {{ width: 15%; font-size:0.7rem; float: left; font-weight:bold; height:8rem; text-align:center; padding: 10px; border: 2px solid black;}}
                            .float-loc {{ width: 18%; font-size:0.7rem; float: left; font-weight:bold; height:8rem; text-align:center; padding: 10px; border: 2px solid black;}}
                            .float-med {{ width: 12%; font-size:0.7rem; float: left; font-weight:bold; height:8rem; text-align:center; padding: 10px; border: 2px solid black;}}
                            .float-pact {{ width: 20%; font-size:0.8rem; float: left; height:8rem; text-align:center; padding: 1rem; font-weight:bold; border: 2px solid black;}}
                            .float-act {{ width: 80%; font-size:0.7rem; float: left; height:8rem; text-align:center; padding: 2rem; border: 2px solid black;}}
                            .heading5 {{font-size:0.7rem; font-weight:bold;}}
                            .heading6 {{font-size:0.65rem; padding-top:0.8rem}}
                            hr{{ margin:0rem; }}
                            @media (min-width: 1920px) and (max-width: 2860px) {{
                                .float-container {{ padding: 5px; }}
                                .float-cat {{ width: 15%; font-size:1.1rem; float: left; height:10rem; text-align:center; padding: 10px; border: 2px solid black;}}
                                .float-inc {{ width: 40%; font-size:1rem; float: left; height:10rem; text-align:center; padding: 2.5rem; border: 2px solid black;}}
                                .float-date {{ width: 15%; font-size:0.7rem; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 2px solid black;}}
                                .float-loc {{ width: 18%; font-size:0.7rem; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 2px solid black;}}
                                .float-med {{ width: 12%; font-size:0.7rem; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 2px solid black;}}
                                .float-pact {{ width: 20%; font-size:1.1rem; float: left; height:10rem; text-align:center; padding: 1rem; font-weight:bold; border: 2px solid black;}}
                                .float-act {{ width: 80%; font-size:1.1rem; float: left; height:10rem; text-align:center; padding: 2rem; border: 2px solid black;}}
                                .heading6 {{font-size:1rem; padding-top:1rem}}
                                .heading5 {{font-size:1rem; font-weight:bold;}}
                                hr{{ margin:0rem; }}
                            }}
                        </style>
                <div class="float-container">
                    <div class="float-cat" style='background-color:red;color:white; font-weight:bold;'>
                        <div class="green">Recordable Lost Time Injury, Recordable Accident (Latest)</div>
                    </div>
                    <div class="float-inc">
                        <div class="blue">{Record_lost_time.incident}</div>
                    </div>
                    <div class="float-date">
                        <div class="heading5">Time<hr>
                            <h6 class="heading6">{Record_lost_time.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div class="heading5">Location<hr>
                            <h6 class="heading6">{Record_lost_time.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div class="heading5">Medical<hr>
                            <h6 class="heading6">{Record_lost_time.medical}</h6>
                        </div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pact">
                        Preventive Measures Implemented and Lesson Learned
                    </div>
                    <div class="float-act">
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
                            <h6 class="heading6">{First_aid.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div class="heading5">Location<hr>
                            <h6 class="heading6">{First_aid.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div class="heading5">Medical<hr>
                            <h6 class="heading6">{First_aid.medical}</h6>
                        </div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pact">
                        Preventive Measures Implemented and Lesson Learned
                    </div>
                    <div class="float-act">
                        {First_aid.action}
                    </div>
                </div>
                        
                <div class="float-container">
                    <div class="float-cat" style='background-color:yellow; font-weight:bold; padding-top:2rem;'>
                        <div>Near_MIS
                            Fire_Det
                        </div>
                    </div>
                    <div class="float-inc">
                        <p style='font-size:0.7rem;'>Near MIS: {Near_mis.incident}</p>
                        <p style='font-size:0.7rem;'>Fire Details: {Fire_mtd.incident}</p>
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
                    <div class="float-pact">
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
    month = datetime.now().month
    year = datetime.now().year
    sconn = sqlite3.connect("database/safety.db")
    cur = sconn.cursor()
    if month < 10:
        df = pd.read_sql_query(f"Select * From 'UNSAFE INCIDENCES' WHERE strftime('%Y-%m', date) = '{year}-0{month}' ", sconn)
    else:
        df = pd.read_sql_query(
            f"Select * From 'UNSAFE INCIDENCES' WHERE strftime('%Y-%m', date) = '{year}-{month}' AND strftime('%Y', date) = '{year}' ",
            sconn)
    # print(df.columns)
    Record_lost_time = 0
    record_accident = 0
    First_aid = 0
    Near_mis = 0
    Fire_mtd = 0
    for item in df["CATEGORY"]:
        if item == "Recordable Loss Time Injury MTD":
            Record_lost_time += 1
        if item == "Recordable Accident MTD":
            record_accident += 1
        if item == "First Aid MTD":
            First_aid += 1
        if item == "Near MIS MTD":
            Near_mis += 1
        if item == "Fire MTD":
            Fire_mtd += 1
    col_indices_A, col_indices_B, col_indices_C, col_indices_D, col_indices_E = st.columns((1,1,1,1,1))
    with col_indices_A:
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-size:1.5rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Lost Time Injury FTD:
                <h4 style='color:white;font-weight:bold; padding-top:2rem;'>{Record_lost_time}</h4></div>""",unsafe_allow_html=True)
    with col_indices_B:
        st.markdown(f"""<div style='background-color:red;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-size:1.5rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Accident FTD:
                <h4 style='color:white;font-weight:bold; padding-top:2.3rem;'>{record_accident}</h4></div>""",unsafe_allow_html=True)
    with col_indices_C:
        st.markdown(f"""<div style='background-color:orange;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-size:1.5rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>First Aid FTD:
                <h4 style='color:white;font-weight:bold; padding-top:3.5rem;'>{First_aid}</h4></div>""",unsafe_allow_html=True)
    with col_indices_D:
        st.markdown(f"""<div style='background-color:yellow;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-size:1.5rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Near MIS FTD:
                <h4 style='color:white;font-weight:bold; padding-top:3.5rem;'>{Near_mis}</h4></div>""",unsafe_allow_html=True)
    with col_indices_E:
        st.markdown(f"""<div style='background-color:skyblue;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-size:1.5rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Fire FTD:
                <h4 style='color:white;font-weight:bold; padding-top:3.5rem;'>{Fire_mtd}</h4></div>""",unsafe_allow_html=True)
    # st.markdown("---")
    st.markdown("## Unsafe Incidents Trend :")
    with st.container():
        col1, col2 = st.columns((1, 1), gap="small")
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
                    f"Select * from 'UNSAFE INCIDENCES' where date between '{start_of_week}' and '{end_of_week}'", sconn)

                week_count += 1
                lst_value.append(len(df_week))
                lst_week_no.append(week_count)

            df_weekly = pd.DataFrame()
            df_weekly['No. Of Events'] = lst_value
            df_weekly['Weeks'] = lst_week_no
            fig = px.bar(df_weekly, x='Weeks', y='No. Of Events', title="Monthly Trends", template='plotly_dark', width=600)
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
                    df_month = pd.read_sql_query(f"Select * From 'UNSAFE INCIDENCES' WHERE strftime('%m', date) = '0{i + 1}' ", sconn)
                else:
                    df_month = pd.read_sql_query(f"Select * From 'UNSAFE INCIDENCES' WHERE strftime('%m', date) = '{i + 1}' ", sconn)
                lst.append(len(df_month))

            new_df['No. Of Events'] = lst

            fig2 = px.bar(new_df, x='Month', y='No. Of Events', title="Yearly Trends", width=600)
            st.plotly_chart(fig2)

    st.markdown("""
        <style>
        .col_heading{
            background:"green";
        }
        
    """, unsafe_allow_html=True)
    # **********************
    st.subheader("Get data acording to the status")
    col1,col2,col3,col4 = st.tabs(['Clear',':red[Open Status]',':green[Close Status]',':orange[Inprocessing]'])
    with col1:
        st.write("Please choose option for showing data!")
    with col2:
        open_data = fetch_data("INCIDENCES DETAILS")
        open_data = open_data[open_data["STATUS"] == "Open"]
        st.table(open_data[["DATE", "TIME", "CATEGORY", "VALUE STREAM", "EVENT", "ACTION", "STATUS"]])
    with col3:
        close_data = fetch_data("INCIDENCES DETAILS")
        close_data = close_data[close_data["STATUS"] == "Closed"]
        st.table(close_data[["DATE", "TIME", "CATEGORY", "VALUE STREAM", "EVENT", "ACTION", "STATUS"]])
    with col4:
        inprocessing = fetch_data("INCIDENCES DETAILS")
        inprocessing = inprocessing[inprocessing["STATUS"] == "Inprocess"]
        st.table(inprocessing[["DATE", "TIME", "CATEGORY", "VALUE STREAM", "EVENT", "ACTION", "STATUS"]])
    # if open:
    #     open_data = fetch_data("INCIDENCES DETAILS", "STATUS", "Open")
    #     open_data.show()
    # elif close:
    #     close_data = fetch_data("INCIDENCES DETAILS", "STATUS", "Closed")
    #     close_data.show()
    # elif inprocess:
    #     inprocessing = fetch_data("INCIDENCES DETAILS", "STATUS", "Inprocess")
    #     inprocessing.show()
    # elif cls_:
    #     open = False
    #     close = False
    #     inprocess = False
    # st.markdown("## Open Observations :")
    # df_open = pd.read_sql_query("""SELECT * FROM 'UNSAFE INCIDENCES' WHERE STATUS='Open' ORDER BY DATE DESC """, sconn)
    # df_close = pd.read_sql_query("""SELECT * FROM 'UNSAFE INCIDENCES' WHERE STATUS='Closed' ORDER BY DATE DESC """, sconn)
    # # df1 = pd.read_sql_query("""SELECT * FROM 'UNSAFE INCIDENCES'""",sconn)   
    # # print(df_new)
    # sconn.close()
    # cl1, cl2 = st.columns((1,1))
    # with cl1:
    #     with st.expander("Show open"):
    #         st.table(df_open[["DATE", "CATEGORY", "EVENT", "ACTION", "LOCATION", "STATUS"]])
    # with cl2:
    #     with st.expander("Show close"):
    #         st.table(df_close[["DATE", "CATEGORY", "EVENT", "ACTION", "LOCATION", "STATUS"]])

def unsafe_practice_tracking():
    sconn = sqlite3.connect("database/safety.db")
    month = datetime.now().month
    year = datetime.now().year
    cur = sconn.cursor()
    if month < 10:
        df = pd.read_sql_query(f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%Y-%m', date) = '{year}-0{month}' ", sconn)
    else:
        df = pd.read_sql_query(
            f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%Y-%m', date) = '{year}-{month}' AND strftime('%Y', date) = '{year}' ",
            sconn)
    # st.write(df)
    closed = 0
    for item in df["STATUS"]:
        if item == "Close" or item == "Closed" or item == "close" or item == 'closed':
            closed += 1
    col_indices_1, col_indices_2, col_indices_3 = st.columns((0.5, 2, 0.5))
    with col_indices_2:
        col_indices_A, col_indices_B, col_indices_C = st.columns((2, 2, 2))
        with col_indices_A:
            st.metric(":blue[Unsafe Practices]", len(df))
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
                    f"Select * from 'UNSAFE PRACTICES TRACKING' where date between '{start_of_week}' and '{end_of_week}'", sconn)

                week_count += 1
                lst_value.append(len(df_week))
                lst_week_no.append(week_count)

            df_weekly = pd.DataFrame()
            df_weekly['No. Of Events'] = lst_value
            df_weekly['Weeks'] = lst_week_no
            fig = px.bar(df_weekly, x='Weeks', y='No. Of Events', title="Monthly Trends", template='plotly_dark', width=600)
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
                    df_month = pd.read_sql_query(f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%m', date) = '0{i + 1}' ", sconn)
                else:
                    df_month = pd.read_sql_query(f"Select * From 'UNSAFE PRACTICES TRACKING' WHERE strftime('%m', date) = '{i + 1}' ", sconn)
                lst.append(len(df_month))

            new_df['No. Of Events'] = lst

            fig2 = px.bar(new_df, x='Month', y='No. Of Events', title="Yearly Trends", width=600)
            st.plotly_chart(fig2)

    st.markdown("""
        <style>
        .col_heading{
            background:"green";
        }
        
    """, unsafe_allow_html=True)

    st.markdown("___")
    # st.markdown("## Open Observations :")
    df_open = pd.read_sql_query("""SELECT * FROM 'UNSAFE PRACTICES TRACKING' WHERE STATUS='Open' ORDER BY DATE DESC """, sconn)
    df_close = pd.read_sql_query("""SELECT * FROM 'UNSAFE PRACTICES TRACKING' WHERE STATUS='Closed' ORDER BY DATE DESC """, sconn)
    # print(df_new)
    sconn.close()
    st.subheader("Get data acording to the status: ")
    col1,col2,col3= st.tabs(['Clear',':red[Open Status]',':green[Close Status]'])
    with col1:
        st.write("Please choose option for showing data!")
    with col2:
        st.table(df_open[["DATE", "EVENT", "LOCATION", "STATUS"]])
    with col3:
        st.table(df_close[["DATE", "EVENT", "LOCATION", "STATUS"]])

#************************** Safety_FTD End **************************#


#************************** Cost_FTD Start **************************#

def productivity_data_fetch():
    rows = None
    with sqlite3.connect("database/cost.db") as conn:
        cur = conn.cursor()
        specific_date = on_date
        query = "SELECT * FROM 'PRODUCTIVITY AND OEE' WHERE Date = ?"
        cur.execute(query, (specific_date,))
        rows = cur.fetchall()
        # print(rows)
        # print(type(rows[0]))
        # st.write(rows[0][3])
    return rows

def breakdown_data_fetch():
    rows = None
    with sqlite3.connect("database/cost.db") as conn:
        cur = conn.cursor()
        specific_date = on_date
        query = "SELECT * FROM 'MACHINE BREAKDOWN TIME' WHERE Date = ?"
        cur.execute(query, (specific_date,))
        rows = cur.fetchall()
        # print(rows)
        # print(type(rows[0]))
        # st.write(rows[0][3])
    return rows

def cost_ftd():
    #******** Productivity and OEE Section ********#
    class prod():
        def __init__(self, target, actual, issue) -> None:
            self.target = target
            self.actual = actual
            self.issue = issue
            pass
    raw = productivity_data_fetch()
    human_prod = prod("no_data", "no_data", "['No issue',]")
    plant_oee = prod("no_data", "no_data", "['No issue',]")
    for i in raw:
        category = i[2]
        prod_data = prod(i[3], i[4], i[5])
        if i[1] == f"{on_date}":
            if category == 'HUMAN PRODUCTIVITY':
                human_prod = prod_data
            if category == 'PLANT AGGREGATE OEE':
                plant_oee = prod_data
    prs_human = eval(human_prod.issue)
    prs_plant = eval(plant_oee.issue)
    st.subheader(f"Status as on: {on_date}",divider="gray")
    col1,col2=st.columns((1,1.7))
    with col1:
        color = 'green'
        st.markdown(f"""
            <center><div>
                <svg class="svg-container" height="350" width="450">
                    <text x="15" y="320" font-size="20rem" font-weight="bold" font-family="Arial" fill={color}>C</text>
                    <text x="250" y="160" font-size="0.9rem" font-weight="bold" fill="black">LEGEND:</text>
                    <text x="250" y="190" font-size="0.9rem" font-weight="bold" fill="green">TARGET ACHIEVED</text>
                    <text x="250" y="220" font-size="0.9rem" font-weight="bold" fill="red">TARGET MISSED</text>
                    <text x="250" y="250" font-size="0.9rem" font-weight="bold" fill="blue">PLANT OFF</text>
                </svg>
            </center></div>
            """, unsafe_allow_html=True)
    with col2:
        st.subheader("PRODUCTIVITY AND OEE")
        blk1,blk2=st.columns((1,1))
        with blk1:
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HUMAN PRODUCTIVITY<hr>
                            <div style='content: "";height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>{human_prod.target}</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{human_prod.actual}</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>PLANT AGGREGATE OEE<hr>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>{plant_oee.target}</h6>
                                </div>
                                <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>{plant_oee.actual}</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
        with blk2:
            st.markdown(f"""
            <style>
                    .float-container {{  padding: 5px;   }}
                    .float-bd1 {{width: 100%; font-weight:bold; font-size:1rem; float: left; word-wrap:break-word; height:10rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                    }}
                    .float-hd1 {{width: 100%; font-size:1rem; color:black; float: left; word-wrap:break-word; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                    }}
                    .par {{padding-top:0.5rem; line-height:0.1rem; font-size:0.7rem; color:black; }}
                    hr{{ margin:0em; }}
            </style>
            <div class="float-container">
                <div class="float-bd1">Top 3 Productivity Problems<hr style='margin:0.6rem 0rem;'>
                        <p class="par">{prs_human}</p>
                </div>
            </div>
            <div class="float-container">
                <div class="float-bd1">Top 3 OEE Related Problems<hr style='margin:0.6rem 0rem;'>
                    <p class="par">{prs_plant}</p>
                </div>
            </div>
        """,unsafe_allow_html=True)
        
        #******** Machine Breakdown TIme Section ********#
        raw1 = breakdown_data_fetch()
        # st.table(raw1)
    st.subheader("MACHINE BREAKDOWN TIME")
    st.markdown("""
        <style>
                .float-container {  padding: 5px;   }
                .float-ln {width: 8%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}
                .float-icp {width: 24%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .float-msd {width: 12%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .float-ln1 {width: 8%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}
                .float-icp1 {width: 24%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .float-msd1 {width: 12%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .par {padding-top:1rem; font-size:0.7rem; color:black; }
                hr{ margin:0em; }
        </style>
        <div class="float-container">
            <div class="float-ln">Line</div><div class="float-msd">Machine</div>
            <div class="float-ln">B/D Time</div><div class="float-icp">Issue</div>
            <div class="float-icp">Action Points</div><div class="float-msd">Status</div>
            <div class="float-msd">Delivery Failure</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln1</div><div class="float-msd1">mch1</div>
            <div class="float-ln1">bdt1</div><div class="float-icp1">iss1</div>
            <div class="float-icp1">acp1</div><div class="float-msd1">sts1</div>
            <div class="float-msd1">df1</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln2</div><div class="float-msd1">mch2</div>
            <div class="float-ln1">bdt2</div><div class="float-icp1">iss2</div>
            <div class="float-icp1">acp2</div><div class="float-msd1">sts2</div>
            <div class="float-msd1">df2</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln3</div><div class="float-msd1">mch3</div>
            <div class="float-ln1">bdt3</div><div class="float-icp1">iss3</div>
            <div class="float-icp1">acp3</div><div class="float-msd1">sts3</div>
            <div class="float-msd1">df3</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln4</div><div class="float-msd1">mch4</div>
            <div class="float-ln1">bdt4</div><div class="float-icp1">iss4</div>
            <div class="float-icp1">acp4</div><div class="float-msd1">sts4</div>
            <div class="float-msd1">df4</div>
        </div>
    """.replace("ln1","line_1").replace("mch1","MCH_1").replace("bdt1","BDT_1").replace("iss1","ISS_1").replace("acp1","Acp_1").replace("sts1","STS_1").replace("df1","DF_1")
    .replace("ln2","line_2").replace("mch2","MCH_2").replace("bdt2","BDT_2").replace("iss2","ISS_2").replace("acp2","Acp_2").replace("sts2","STS_2").replace("df2","DF_2")
    .replace("ln3","line_3").replace("mch3","MCH_3").replace("bdt3","BDT_3").replace("iss3","ISS_3").replace("acp3","Acp_3").replace("sts3","STS_3").replace("df3","DF_3")
    .replace("ln4","line_4").replace("mch4","MCH_4").replace("bdt4","BDT_4").replace("iss4","ISS_4").replace("acp4","Acp_4").replace("sts4","STS_4").replace("df4","DF_4")
    ,unsafe_allow_html=True)

    #******** RAW Material Section ********#
    st.subheader("RAW MATERIAL P.D.I.")
    st.markdown("""
            <style>
                    .float-container {  padding: 5px;   }
                    .float-ct {width: 10%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.7rem; border: 1px solid black;}
                    .float-nop {width: 15%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.7rem; line-height:1rem; border: 1px solid black;}
                    .float-prb {width: 30%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.7rem; line-height:1rem; border: 1px solid black;}
                    .float-ct1 {width: 10%; font-weight:bold; font-size:3rem; float: left; word-wrap:break-word; height:6rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}
                    .float-nop1 {width: 15%; font-size:0.7rem; float: left; word-wrap:break-word; height:6rem; text-align:center; padding: 2rem; line-height:1rem; border: 1px solid black;}
                    .float-prb1 {width: 30%; font-size:0.7rem; float: left; word-wrap:break-word; height:6rem; text-align:center; padding: 2rem; line-height:1rem; border: 1px solid black;}
                    .par {padding-top:1rem; font-size:0.7rem; color:black; }
                    hr{ margin:0em; }
            </style>
            <div class="float-container">
                <div class="float-ct">Category</div><div class="float-nop">No of Parts</div>
                <div class="float-nop">Value (MINR)</div><div class="float-nop">Actual Value (MINR)</div>
                <div class="float-nop">P.D.I.</div><div class="float-prb">Top 3 Problems</div>
            </div>
            <div class="float-container">
                <div class="float-ct1">A</div><div class="float-nop1">npr1</div>
                <div class="float-nop1">vnr1</div><div class="float-nop1">avr1</div>
                <div class="float-nop1">pdi1</div><div class="float-prb1">tpr1</div>
            </div>
            <div class="float-container">
                <div class="float-ct1">B</div><div class="float-nop1">npr2</div>
                <div class="float-nop1">vnr2</div><div class="float-nop1">avr2</div>
                <div class="float-nop1">pdi2</div><div class="float-prb1">tpr2</div>
            </div>
            <div class="float-container">
                <div class="float-ct1">C</div><div class="float-nop1">npr3</div>
                <div class="float-nop1">vnr3</div><div class="float-nop1">avr3</div>
                <div class="float-nop1">pdi3</div><div class="float-prb1">tpr3</div>
            </div>
        """.replace("npr1","NOP_1").replace("vnr1","VNR_1").replace("avr1","AVR_1").replace("pdi1","PDI_1").replace("tpr1","TPR_1")
        .replace("npr2","NOP_2").replace("vnr2","VNR_2").replace("avr2","AVR_2").replace("pdi2","PDI_2").replace("tpr2","TPR_2")
        .replace("npr3","NOP_3").replace("vnr3","VNR_3").replace("avr3","AVR_3").replace("pdi3","PDI_3").replace("tpr3","TPR_3"),unsafe_allow_html=True)

def productivity_oee():
    current_date()

    blk1,blk2=st.columns((1,1))
    with blk1:
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HUMAN PRODUCTIVITY<hr>
                            <div style='content: ""; height:72%; display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6>$1</h6>
                                </div>
                                    <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>$2</h6>
                                </div>
                            </div>
                        </div>""".replace("$1",str("0")).replace("$2",str("0")),unsafe_allow_html=True)
        st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>PLANT AGGREGATE OEE<hr>
                            <div style='content: center; height:72%; display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6>$1</h6>
                                </div>
                                    <div style='border-left: 1px solid lightgray; height: 100%;'></div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6>$2</h6>
                                </div>
                            </div>
                        </div>""".replace("$1",str("0")).replace("$2",str("0")),unsafe_allow_html=True)
    with blk2:
        st.markdown("""
        <style>
                .float-container {  padding: 5px;   }
                .float-bd1 {width: 100%; font-weight:bold; font-size:1rem; float: left; word-wrap:break-word; height:10rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                }
                .float-hd1 {width: 100%; font-size:1rem; color:black; float: left; word-wrap:break-word; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                }
                .par {padding-top:0.5rem; line-height:0.1rem; font-size:0.7rem; color:black; }
                hr{ margin:0em; }
        </style>
        <div class="float-container">
            <div class="float-bd1">Top 3 Productivity Problems<hr style='margin:0.6rem 0rem;'>
                    <p class="par">Prod_prblm_1 here</p>
                    <p class="par">Prod_prblm_2 here</p>
                    <p class="par">Prod_prblm_3 here</p>
            </div>
        </div>
        <div class="float-container">
            <div class="float-bd1">Top 3 OEE Related Problems<hr style='margin:0.6rem 0rem;'>
                <p class="par">OEE_prblm_1 here</p>
                <p class="par">OEE_prblm_2 here</p>
                <p class="par">OEE_prblm_3 here</p>
            </div>
        </div>
    """.replace("Prod_prblm_1",(str("Productivity_Problem_1")))
    .replace("Prod_prblm_2",(str("Productivity_Problem_2")))
    .replace("Prod_prblm_3",(str("Productivity_Problem_3")))
    .replace("OEE_prblm_1",(str("OEE_Problem_1")))
    .replace("OEE_prblm_2",(str("OEE_Problem_2")))
    .replace("OEE_prblm_3",(str("OEE_Problem_3"))),unsafe_allow_html=True)

def mach_break_time():
    h1_col1, h1_col2 = st.columns((1,1.5))
    with h1_col1:
        st.subheader(":blue[MACHINE BREAKDOWN TIME]",divider="rainbow")
    with h1_col2:
        pass
    st.markdown("""
        <style>
                .float-container {  padding: 5px;   }
                .float-ln {width: 8%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}
                .float-icp {width: 24%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .float-msd {width: 12%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .float-ln1 {width: 8%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}
                .float-icp1 {width: 24%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .float-msd1 {width: 12%; font-size:0.7rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.4rem; line-height:1rem; border: 1px solid black;}
                .par {padding-top:1rem; font-size:0.7rem; color:black; }
                hr{ margin:0em; }
        </style>
        <div class="float-container">
            <div class="float-ln">Line</div><div class="float-msd">Machine</div>
            <div class="float-ln">B/D Time</div><div class="float-icp">Issue</div>
            <div class="float-icp">Action Points</div><div class="float-msd">Status</div>
            <div class="float-msd">Delivery Failure</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln1</div><div class="float-msd1">mch1</div>
            <div class="float-ln1">bdt1</div><div class="float-icp1">iss1</div>
            <div class="float-icp1">acp1</div><div class="float-msd1">sts1</div>
            <div class="float-msd1">df1</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln2</div><div class="float-msd1">mch2</div>
            <div class="float-ln1">bdt2</div><div class="float-icp1">iss2</div>
            <div class="float-icp1">acp2</div><div class="float-msd1">sts2</div>
            <div class="float-msd1">df2</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln3</div><div class="float-msd1">mch3</div>
            <div class="float-ln1">bdt3</div><div class="float-icp1">iss3</div>
            <div class="float-icp1">acp3</div><div class="float-msd1">sts3</div>
            <div class="float-msd1">df3</div>
        </div>
        <div class="float-container">
            <div class="float-ln1">ln4</div><div class="float-msd1">mch4</div>
            <div class="float-ln1">bdt4</div><div class="float-icp1">iss4</div>
            <div class="float-icp1">acp4</div><div class="float-msd1">sts4</div>
            <div class="float-msd1">df4</div>
        </div>
    """.replace("ln1","line_1").replace("mch1","MCH_1").replace("bdt1","BDT_1").replace("iss1","ISS_1").replace("acp1","Acp_1").replace("sts1","STS_1").replace("df1","DF_1")
    .replace("ln2","line_2").replace("mch2","MCH_2").replace("bdt2","BDT_2").replace("iss2","ISS_2").replace("acp2","Acp_2").replace("sts2","STS_2").replace("df2","DF_2")
    .replace("ln3","line_3").replace("mch3","MCH_3").replace("bdt3","BDT_3").replace("iss3","ISS_3").replace("acp3","Acp_3").replace("sts3","STS_3").replace("df3","DF_3")
    .replace("ln4","line_4").replace("mch4","MCH_4").replace("bdt4","BDT_4").replace("iss4","ISS_4").replace("acp4","Acp_4").replace("sts4","STS_4").replace("df4","DF_4")
    ,unsafe_allow_html=True)

def raw_metarial():
    current_date()

    st.markdown("""
            <style>
                    .float-container {  padding: 5px;   }
                    .float-ct {width: 10%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.7rem; border: 1px solid black;}
                    .float-nop {width: 15%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.7rem; line-height:1rem; border: 1px solid black;}
                    .float-prb {width: 30%; font-weight:bold; font-size:0.8rem; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 0.7rem; line-height:1rem; border: 1px solid black;}
                    .float-ct1 {width: 10%; font-weight:bold; font-size:3rem; float: left; word-wrap:break-word; height:6rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;}
                    .float-nop1 {width: 15%; font-size:0.7rem; float: left; word-wrap:break-word; height:6rem; text-align:center; padding: 2rem; line-height:1rem; border: 1px solid black;}
                    .float-prb1 {width: 30%; font-size:0.7rem; float: left; word-wrap:break-word; height:6rem; text-align:center; padding: 2rem; line-height:1rem; border: 1px solid black;}
                    .par {padding-top:1rem; font-size:0.7rem; color:black; }
                    hr{ margin:0em; }
            </style>
            <div class="float-container">
                <div class="float-ct">Category</div><div class="float-nop">No of Parts</div>
                <div class="float-nop">Value (MINR)</div><div class="float-nop">Actual Value (MINR)</div>
                <div class="float-nop">P.D.I.</div><div class="float-prb">Top 3 Problems</div>
            </div>
            <div class="float-container">
                <div class="float-ct1">A</div><div class="float-nop1">npr1</div>
                <div class="float-nop1">vnr1</div><div class="float-nop1">avr1</div>
                <div class="float-nop1">pdi1</div><div class="float-prb1">tpr1</div>
            </div>
            <div class="float-container">
                <div class="float-ct1">B</div><div class="float-nop1">npr2</div>
                <div class="float-nop1">vnr2</div><div class="float-nop1">avr2</div>
                <div class="float-nop1">pdi2</div><div class="float-prb1">tpr2</div>
            </div>
            <div class="float-container">
                <div class="float-ct1">C</div><div class="float-nop1">npr3</div>
                <div class="float-nop1">vnr3</div><div class="float-nop1">avr3</div>
                <div class="float-nop1">pdi3</div><div class="float-prb1">tpr3</div>
            </div>
        """.replace("npr1","NOP_1").replace("vnr1","VNR_1").replace("avr1","AVR_1").replace("pdi1","PDI_1").replace("tpr1","TPR_1")
        .replace("npr2","NOP_2").replace("vnr2","VNR_2").replace("avr2","AVR_2").replace("pdi2","PDI_2").replace("tpr2","TPR_2")
        .replace("npr3","NOP_3").replace("vnr3","VNR_3").replace("avr3","AVR_3").replace("pdi3","PDI_3").replace("tpr3","TPR_3"),unsafe_allow_html=True)

#************************** Cost_FTD End **************************#


#************************** Delivery_FTD Start **************************#
class cmp():
    def __init__(self, target, actual):
        self.target = target
        self.actual = actual
    def show(self):
        return f"Target was {self.target}% and achived {self.actual}%"

# def delivery_data_fetch():
#     fconn = sqlite3.connect("database/delivery.db")
#     cursor = fconn.cursor()
#     specific_date = on_date
#     query = "SELECT * FROM Delivery WHERE Date = ?"
#     cursor.execute(query, (specific_date,))
#     rows = cursor.fetchall()
#     fconn.close()
#     # print(rows)
#     # print(type(rows[0]))
#     # st.write(rows[0][3])
#     delivery_data = fetch_data("OTIF_CC PDI", "CATEGORY", "OE")
#     return delivery_data
     
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
        if row["DATE"] == f"{on_date}":
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

    st.subheader(f"Status as on: {on_date}", divider="gray")
    col1,col2=st.columns((1,1.9))
    with col1:
        color = 'blue'
        st.markdown(f"""
            <center><div>
                <svg class="svg-container" height="350" width="450">
                    <text x="20" y="320" font-size="20rem" font-weight="bold" font-family="Arial" fill={color}>D</text>
                    <text x="250" y="160" font-size="0.9rem" font-weight="bold" fill="black">LEGEND:</text>
                    <text x="250" y="190" font-size="0.9rem" font-weight="bold" fill="green">TARGET ACHIEVED</text>
                    <text x="250" y="220" font-size="0.9rem" font-weight="bold" fill="red">TARGET MISSED</text>
                    <text x="250" y="250" font-size="0.9rem" font-weight="bold" fill="blue">PLANT OFF</text>
                </svg>
            </center></div>
            """, unsafe_allow_html=True)
        # st.markdown(f"""
        #     <style>
        #         /* Define your custom CSS styles here */
        #         .svg-container {{
        #             width: 100%;
        #             max-width: 100%; /* Ensure the container is responsive */
        #             overflow: hidden; /* Hide the overflowing content */
        #             height: 100vh;
        #             text-align: center;
        #         }}
        #     </style>
        #     <div class="svg-container">
        #         <svg height="100%" width="100%">
        #             <text x="25%" y="50%" font-size="60vh" font-weight="bold" text-anchor="middle" alignment-baseline="middle" fill={color}>D</text>
        #             <text x="55%" y="35%" font-size="2vh" font-weight="bold" fill="black">LEGEND:</text>
        #             <text x="55%" y="45%" font-size="2vh" font-weight="bold" fill="green">TARGET ACHIEVED</text>
        #             <text x="55%" y="55%" font-size="2vh" font-weight="bold" fill="red">TARGET MISSED</text>
        #             <text x="55%" y="65%" font-size="2vh" font-weight="bold" fill="blue">PLANT OFF</text>
        #         </svg>
        #     </div>
        #     """, unsafe_allow_html=True)
    with col2:
        st.subheader("ON TIME IN FULL (OTIF)")
        blk1,blk2=st.columns((1,1))
        with blk1:
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>OE<hr style='margin:0em;'>
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
        with blk2:
            st.markdown(f"""<div style='margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>AFTERMARKET<hr style='margin:0em;'>
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
        for index, row in sale_plan.iterrows():
            if row["DATE"] == f'{on_date}':
                bs_today = row["BUDGETED SALE"]
                ord_book = row["ORDER BOOK"]
                act_sale = row["ACTUAL SALE"]
                dlt_sb = row["DELTA SB"]
                dlt_so = row["DELTA SO"]
        # budget_today = sale_plan[sale_plan["DATE"] == f'{on_date}']

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
            <div class="float-hd">{bs_today}</div>
            <div class="float-hd">{ord_book}</div>
            <div class="float-hd">{act_sale}</div>
            <div class="float-hd">{dlt_sb}</div>
            <div class="float-hd">{dlt_so}</div>
        </div>
    """,unsafe_allow_html=True)
    
    issue = fetch_data("DELIVERY ISSUES")
    # st.write(issue)
    # issue["DATE"] = pd.to_datetime(issue["DATE"])
    # issue = issue[issue['DATE'].dt.date == on_date]
    # issue = issue[["PART NO", "ISSUE RAISED", "ACTION", "TARGET DATE"]]
    
    
    # st.write(issue)
    st.markdown(f"""
            <div class="float-container">
                <div class="float-icu">Costomer Urgencies/Issues</div>
            </div>
            <div class="float-container">
                <div class="float-hcd">Part No <hr>
                    <p class="par">prt_no1</p>
                    <p class="par">prt_no2</p>
                    <p class="par">prt_no3</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Issue Raised <hr>
                    <p class="par">issue_ris1</p>
                    <p class="par">issue_ris2</p>
                    <p class="par">issue_ris3</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Action to be Taken <hr>
                    <p class="par">action_take1</p>
                    <p class="par">action_take2</p>
                    <p class="par">action_take3</p>
                </div>
                <div class="float-hcd">Trgt Date <hr>
                    <p class="par">trgt_dt1</p>
                    <p class="par">trgt_dt2</p>
                    <p class="par">trgt_dt3</p>
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
    d_data = fetch_data("OTIF_CC PDI")
    for index, row in d_data.iterrows():
        if row["DATE"] == f"{on_date}":
            if row["CATEGORY"] == "OE":
                oe = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "AfterMarket":
                aftermarket = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "OE_Spare":
                oe_spares = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "Export":
                export = cmp(row["TARGET"], row["ACTUAL"])
            pass
    current_date()
    blk1,blk2=st.columns((1,1))
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
    with blk2:
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
    cl1,cl2,cl3,cl4 = st.columns((1,1,1,1))
    with cl1:
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>OE</center>""",unsafe_allow_html=True)
        pass
    with cl2:
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>OE_SPARES</center>""",unsafe_allow_html=True)
        pass
    with cl3:
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>AFTERMARKET</center>""",unsafe_allow_html=True)
        pass
    with cl4:
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>EXPORT</center>""",unsafe_allow_html=True)
        pass
    st.markdown("___")
    col1,col2,col3,col4 = st.columns((1,1,1,1))
    with col1:
        oe_data = d_data[(d_data['CATEGORY'] == 'OE') & (d_data['DATE'].dt.to_period('M') == current_month)]
        # ****** Daily_Data ****** #
        daily_data = oe_data.groupby(oe_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = oe_data.groupby(oe_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        oe_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = oe_data_month.groupby(oe_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])
    with col2:
        oe_spare_data = d_data[(d_data['CATEGORY'] == 'OE_Spare') & (d_data['DATE'].dt.to_period('M') == current_month)]
        # ****** Daily_Data ****** #
        daily_data = oe_spare_data.groupby(oe_spare_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = oe_spare_data.groupby(oe_spare_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        oe_spare_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = oe_spare_data_month.groupby(oe_spare_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])
    with col3:
        aftermarket_data = d_data[(d_data['CATEGORY'] == 'AfterMarket') & (d_data['DATE'].dt.to_period('M') == current_month)]
        # ****** Daily_Data ****** #
        daily_data = aftermarket_data.groupby(aftermarket_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = aftermarket_data.groupby(aftermarket_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        aftermarket_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = aftermarket_data_month.groupby(aftermarket_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])
    with col4:
        export_data = d_data[(d_data['CATEGORY'] == 'Export') & (d_data['DATE'].dt.to_period('M') == current_month)]
        # ****** Daily_Data ****** #
        daily_data = export_data.groupby(export_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = export_data.groupby(export_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        export_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = export_data_month.groupby(export_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])

def sale_actual():
    # Sale Plan vs Actual Plan
    current_date()
    st.subheader("Sale Plan vs Actual Trend")
    bar_graph("SALE PLAN VS ACTUAL")
    sale_plan = fetch_data("SALE PLAN VS ACTUAL")
    bs_today = 0
    ord_book = 0
    act_sale = 0
    dlt_sb = 0
    dlt_so = 0
    sale_plan["DATE"] = pd.to_datetime(sale_plan["DATE"])
    month = datetime.now().month
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
    st.markdown(f"""
            <div class="float-container">
                <div class="float-icu">Costomer Urgencies/Issues</div>
            </div>
            <div class="float-container">
                <div class="float-hcd">Part No <hr>
                    <p class="par">prt_no1</p>
                    <p class="par">prt_no2</p>
                    <p class="par">prt_no3</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Issue Raised <hr>
                    <p class="par">issue_ris1</p>
                    <p class="par">issue_ris2</p>
                    <p class="par">issue_ris3</p>
                </div>
                <div class="float-hcd" style='width:30%;'>Action to be Taken <hr>
                    <p class="par">action_take1</p>
                    <p class="par">action_take2</p>
                    <p class="par">action_take3</p>
                </div>
                <div class="float-hcd">Trgt Date <hr>
                    <p class="par">trgt_dt1</p>
                    <p class="par">trgt_dt2</p>
                    <p class="par">trgt_dt3</p>
                </div>
            </div>
    """,unsafe_allow_html=True)

def critcal_customer_pdi():
    msil = cmp(0,0)
    honda = cmp(0,0)
    gm = cmp(0,0)
    hd = cmp(0,0)
    rnaipl = cmp(0,0)
    ford = cmp(0,0)
    d_data = fetch_data("OTIF_CC PDI")
    for index, row in d_data.iterrows():
        if row["DATE"] == f"{on_date}":
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
    current_date()
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
    month_data = d_data[d_data["DATE"].dt.month == 10]  # Filter data for the month
    # st.write(month_data)
    current_month = pd.Timestamp('now').to_period('M')
    col1,col2,col3,col4 = st.columns((1,1,1,1))
    with col1:
        msil_data = d_data[(d_data['CATEGORY'] == 'MSIL') & (d_data['DATE'].dt.to_period('M') == current_month)]
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>MSIL</center>""",unsafe_allow_html=True)
        # ****** Daily_Data ****** #
        daily_data = msil_data.groupby(msil_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = msil_data.groupby(msil_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        msil_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = msil_data_month.groupby(msil_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])
    with col2:
        hd_data = d_data[(d_data['CATEGORY'] == 'HD') & (d_data['DATE'].dt.to_period('M') == current_month)]
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>HD</center>""",unsafe_allow_html=True)
        # ****** Daily_Data ****** #
        daily_data = hd_data.groupby(hd_data['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = hd_data.groupby(hd_data['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        hd_data_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = hd_data_month.groupby(hd_data_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])
    with col3:
        honda = d_data[(d_data['CATEGORY'] == 'Honda') & (d_data['DATE'].dt.to_period('M') == current_month)]
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>HONDA</center>""",unsafe_allow_html=True)
        # ****** Daily_Data ****** #
        daily_data = honda.groupby(honda['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = honda.groupby(honda['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        honda_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = honda_month.groupby(honda_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])
    with col4:
        gm = d_data[(d_data['CATEGORY'] == 'GM') & (d_data['DATE'].dt.to_period('M') == current_month)]
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>GM</center>""",unsafe_allow_html=True)
        # ****** Daily_Data ****** #
        daily_data = gm.groupby(gm['DATE'].dt.to_period('D'))[['TARGET', 'ACTUAL']].sum()
        daily_data.index = daily_data.index.strftime('%b %d') 
        st.bar_chart(daily_data, color=["#00ff00","#ff0000"])
        # ****** Weekly_Data ****** #
        weekly_data = gm.groupby(gm['DATE'].dt.to_period('W'))[['TARGET', 'ACTUAL']].sum()
        weekly_data.index = range(1, len(weekly_data) + 1)
        st.bar_chart(weekly_data, color=["#00ff00", "#ff0000"])
        # ****** Monthly_Data ****** #
        gm_month = d_data[d_data['CATEGORY'] == 'MSIL']
        monthly_data = gm_month.groupby(gm_month['DATE'].dt.to_period('M'))[['TARGET', 'ACTUAL']].sum()
        monthly_data.index = monthly_data.index.strftime('%b')
        st.bar_chart(monthly_data, color=["#00ff00", "#ff0000"])
        # fig = px.bar(monthly_data, x=monthly_data.index, y=['TARGET', 'ACTUAL'], labels={'index': 'Year'}, width=450, height=350)
        # fig.update_layout(barmode='group', xaxis_title='Year', yaxis_title='Values')
        # st.plotly_chart(fig)

#************************** Delivery_FTD End **************************#


#************************** Quality_FTD Start **************************#
def quality_ftd():
    st.subheader(f"Status as on: {on_date}",divider="gray")
    plant_ppm = cmp(0,0)
    supplier_ppm = cmp(0,0)
    complaint_data = fetch_data("CUSTOMER COMPLAINTS")
    df = complaint_data[complaint_data["DATE"] == f"{on_date}"]
    ppm_data = fetch_data("PLANT PPM & SUPPLIER PPM")
    ppm_problem = fetch_data("PPM PROBLEMS")

    for index, row in ppm_data.iterrows():
        if row["DATE"] == f"{on_date}":
            if row["CATEGORY"] == "PLANT PPM":
                plant_ppm = cmp(row["TARGET"], row["ACTUAL"])
            if row["CATEGORY"] == "SUPPLIER PPM":
                supplier_ppm = cmp(row["TARGET"], row["ACTUAL"])
        pass
    col1,col2=st.columns((1,1.8))
    # ********** Dynamic Q Letter ********** #
    with col1:
        if on_date.weekday() == 6: day = "Sunday"
        else: day = "it's not sunday"
        # date=datetime.now().date().strftime("%d-%m-%Y")
        if len(df) > 0: color = 'red'
        elif day == "Sunday": color = 'blue'
        else: color = 'green'
        st.markdown(f"""
            <style>
                /* Define your custom CSS styles here */
                .svg-container {{
                    width: 100%;
                    max-width: 100%; /* Ensure the container is responsive */
                    overflow: hidden; /* Hide the overflowing content */
                    height: 100vh;
                    text-align: center;
                }}
            </style>
            <div class="svg-container">
                <svg height="100%" width="100%">
                    <text x="25%" y="50%" font-size="60vh" font-weight="bold" text-anchor="middle" alignment-baseline="middle" fill={color}>Q</text>
                    <text x="55%" y="35%" font-size="2vh" font-weight="bold" fill="black">LEGEND:</text>
                    <text x="55%" y="45%" font-size="2vh" font-weight="bold" fill="green">TARGET ACHIEVED</text>
                    <text x="55%" y="55%" font-size="2vh" font-weight="bold" fill="red">TARGET MISSED</text>
                    <text x="55%" y="65%" font-size="2vh" font-weight="bold" fill="blue">PLANT OFF</text>
                </svg>
            </div>
            """, unsafe_allow_html=True)
    with col2:
        # **************** Customer Complaints **************************#
        st.subheader(f"Today'S Customer Complaints: {len(df)}")
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
        data_df['STATUS'] = data_df['STATUS'].apply(lambda x: f'<span style="{format_status(x)}">{x}</span>')
        # data_df = data_df.style.applymap(format_status, subset=['STATUS'])
        st.write(data_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        # st.data_editor(df[["COMPLAINT", "RAISE DATE", "RESPONSIBILITY", "TARGET DATE", "STATUS"]], hide_index=True, width=1500, height=245)
        # st.data_editor(df[["COMPLAINT", "RAISE DATE", "CLOSING DATE", "STATUS"]], hide_index=True, width=1600)
        # st.markdown("""
        #     <style>
        #             .float-container {  padding: 5px;   }
        #             .float-cn {width: 22%; font-size:0.8rem; font-weight:bold; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
        #             }
        #             .float-cd {width: 35%; font-size:0.8rem; font-weight:bold; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
        #             }
        #             .float-dr {width: 15%; font-size:0.8rem; font-weight:bold; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
        #             }
        #             .float-dc {width: 15%; font-size:0.8rem; font-weight:bold; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
        #             }
        #             .float-st {width: 13%; font-size:0.8rem; font-weight:bold; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
        #             }
        #             .par {padding-top:1rem; font-size:0.7rem; color:black; }
        #             hr{ margin:0em; }
                    
        #     </style>
        #     <div class="float-container">
        #         <div class="float-cn">Complaints Number<hr>
        #         <p class="par" style='padding-top:35%;'>comp_no</p>
        #         </div>
        #         <div class="float-cd">Complaint details<hr>
        #         <p class="par">comp_det1</p>
        #         <p class="par">comp_det2</p>
        #         <p class="par">comp_det3</p>
        #         </div>
        #         <div class="float-dr">Raised<hr>
        #         <p class="par">comp_rais1</p>
        #         <p class="par">comp_rais2</p>
        #         <p class="par">comp_rais3</p>
        #         </div>
        #         <div class="float-dc">Close<hr>
        #         <p class="par">comp_cls1</p>
        #         <p class="par">comp_cls2</p>
        #         <p class="par">comp_cls3</p>
        #         </div>
        #         <div class="float-st">Status<hr>
        #         <p class="par">comp_sts1</p>
        #         <p class="par">comp_sts2</p>
        #         <p class="par">comp_sts3</p>
        #         </div>
        #     </div>
        # """.replace("comp_no",(str("test_no")))
        # .replace("comp_det1",(str("test_complaint1"))).replace("comp_rais1",(str("test_ris1"))).replace("comp_cls1",(str("test_cls1"))).replace("comp_sts1",(str("CLOSE1")))
        # .replace("comp_det2",(str("test_complaint2"))).replace("comp_rais2",(str("test_ris2"))).replace("comp_cls2",(str("test_cls2"))).replace("comp_sts2",(str("CLOSE2")))
        # .replace("comp_det3",(str("test_complaint3"))).replace("comp_rais3",(str("test_ris3"))).replace("comp_cls3",(str("test_cls3"))).replace("comp_sts3",(str("CLOSE3"))),unsafe_allow_html=True)
        
        # **************** Plant PPM & Supplier PPM **************************#
        st.markdown("""<div style='padding-top:1.5rem;'><h4>PLANT PPM & SUPPLIER PPM</h4></div>""",unsafe_allow_html=True)
        plant_prob = []
        supplier_prob = []
        for index, row in ppm_problem.iterrows():
            if row["DATE"] == f"{on_date}":
                if row["CATEGORY"] == "PLANT PPM":
                    issue = {
                        "PROBLEM": row["PROBLEM"],
                        "PART_LINE": row["PART_LINE"],
                        "REJ_QTY": row["REJ_QTY"]
                    }
                    plant_prob.append(issue)
                    # plant_prob.append(q_issue(row["PROBLEM"], row["PART_LINE"], row["REJ_QTY"]))
                if row["CATEGORY"] == "SUPPLIER PPM":
                    issue = {
                        "PROBLEM": row["PROBLEM"],
                        "PART_LINE": row["PART_LINE"],
                        "REJ_QTY": row["REJ_QTY"]
                    }
                    supplier_prob.append(issue)
                    # supplier_prob.append(q_issue(row["PROBLEM"], row["PART_LINE"], row["REJ_QTY"]))
        # st.write(plant_prob.show())
        cl1,cl2=st.columns((1,2))
        with cl1:
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
                        <p class="par" style='font-weight:bold;'>Reported Rejection (Percntage)</p>
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
    for index, row in fr_issue.iterrows():
        if row["DATE"] == f"{on_date}":
            issue_instance = {
                "PART_NO": row["PART NO"],
                "ISSUE": row["ISSUE"],
                "ACTION": row["CORRECTIVE ACTION"],
                "T_DATE": row["TARGET DATE"]
            }
            ftp_issue.append(issue_instance)
            # ftp_issue.append(ftp_issues(row["PART NO"], row["ISSUE"], row["CORRECTIVE ACTION"], row["TARGET DATE"]))
            pass
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
    class complaint():
        def __init__(self, comp, rais, resp, close, stat) -> None: 
            self.comp = comp
            self.rais = rais
            self.resp = resp
            self.close = close
            self.stat = stat
            pass
        def show(self):
            return st.write(f"Complaint is {self.comp} raise on date {self.rais} and will close on {self.close} and now status is {self.stat}")
    datas = []
    current_date()
    df = fetch_data("CUSTOMER COMPLAINTS")
    df['DATE'] = pd.to_datetime(df['DATE'])
    current_month = pd.Timestamp('now').to_period('M')
    cmplnt_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    total_complaints = len(cmplnt_data)
    # current_day = pd.Timestamp('now').day
    # monthly_data = df[df['RAISE DATE'].dt.month == current_month]
    # daily_data = df[df['RAISE DATE'].dt.day == 18]
    # complaints_per_day = df['RAISE DATE'].dt.day.value_counts().sort_index()
    
    for index, complaints in cmplnt_data.iterrows():
        datas.append(complaint(complaints["COMPLAINT"], complaints["RAISE DATE"], complaints["RESPONSIBILITY"], complaints["TARGET DATE"], complaints["STATUS"]))
        # st.write(complaints["COMPLAINT"])
    # st.write(datas[3].comp)
    
    st.subheader("Customer Complaints Trend:")
    cl1,cl2,cl3 = st.columns((1,1,1))
    with cl1:
        # ****** Daily_Data ****** #
        st.markdown("")
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.5rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
        daily_data = cmplnt_data.groupby(cmplnt_data['DATE'].dt.to_period('D')).size()
        daily_data.index = daily_data.index.strftime('%b %d')
        daily_color = ["#fa2323" if value > 3 else "#5fe650" for value in daily_data]
        fig = go.Figure(data=[go.Bar(x=daily_data.index, y=daily_data, marker_color=daily_color)])
        # Customize the chart layout
        fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Days', yaxis_title='Complaints')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
        # st.bar_chart(daily_data, color=daily_color, height=387)
    with cl2:
        # ****** Weekly_Data ****** #
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Weekly Trend</center>""",unsafe_allow_html=True)
        weekly_data = cmplnt_data.groupby(cmplnt_data['DATE'].dt.to_period('W')).size()
        weekly_data.index = range(1, len(weekly_data) + 1)
        weekly_color = ["#fa2323" if value > 3 else "#5fe650" for value in weekly_data]
        fig = go.Figure(data=[go.Bar(x=weekly_data.index, y=weekly_data, marker_color=weekly_color)])
        # Customize the chart layout
        fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Weeks', yaxis_title='Complaints')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
        # st.bar_chart(weekly_data, color="#ff0000")
    with cl3:
        # ****** Monthly_Data ****** #
        st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Monthly Trend</center>""",unsafe_allow_html=True)
        monthly_data = df.groupby(df['DATE'].dt.to_period('M')).size()
        monthly_data.index = monthly_data.index.strftime('%b')
        monthly_color = ["#fa2323" if value > 3 else "#5fe650" for value in monthly_data]
        fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=monthly_data, marker_color=monthly_color)])
        # Customize the chart layout
        fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Months', yaxis_title='Complaints')
        # Display the chart in Streamlit
        st.plotly_chart(fig)
        # st.bar_chart(monthly_data, color="#ff0000", height=363)
    

    col1,col2,col3 = st.columns((1,1,1))
    with col1:
        st.subheader(f"Total Complaints: {total_complaints}")
    with col2:
        pass
    with col3:
        pass
    
    # df = df[["COMPLAINT", "RAISE DATE", "RESPONSIBILITY", "TARGET DATE", "STATUS"]]
    # def my_color(status):
    #     if status == 'Open':
    #         color = 'background-color: #FB2D30; color: white;'
    #     elif status == 'Inprocess':
    #         color = 'background-color: #F3ED21; color: white;'
    #     elif status == 'Closed':
    #         color = 'background-color: #78E866; color: white;'
    #     # color = 'green' if target > actual else 'red'
    #     return f'{color}'
    # styled_df = df.style.applymap(my_color, subset=['STATUS'])
    # st.dataframe(styled_df, hide_index=True, width=2000)
    
    status_clr = []
    def stat_clr( clr_name):
        if clr_name == 'Open':
            clr = '#fa2323'
            return clr
        elif clr_name == 'Inprocess':
            clr = '#e9f76a'
            return clr
        else:
            clr = '#5fe650'
            return clr
    
    statuses = [datas[0].stat, datas[1].stat, datas[2].stat, datas[3].stat, datas[4].stat, datas[5].stat]
    for status in statuses:
        status_clr_value = stat_clr(status)
        status_clr.append(status_clr_value)
    # status_clr[0] = stat_clr(datas[0].stat)
    # status_clr[1] = stat_clr(datas[1].stat)
    # status_clr[2] = stat_clr(datas[2].stat)
    # status_clr[3] = stat_clr(datas[3].stat)
    # status_clr[4] = stat_clr(datas[4].stat)
    # status_clr[5] = stat_clr(datas[5].stat)

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
                <p class="par">{datas[0].comp}</p>
                <p class="par">{datas[1].comp}</p>
                <p class="par">{datas[2].comp}</p>
                <p class="par">{datas[3].comp}</p>
                <p class="par">{datas[4].comp}</p>
                <p class="par">{datas[5].comp}</p>
            </div>
            <div class="float-dr">Raised<hr>
                <p class="par">{datas[0].rais}</p>
                <p class="par">{datas[1].rais}</p>
                <p class="par">{datas[2].rais}</p>
                <p class="par">{datas[3].rais}</p>
                <p class="par">{datas[4].rais}</p>
                <p class="par">{datas[5].rais}</p>
            </div>
            <div class="float-dc">Responsibility<hr>
                <p class="par">{datas[0].resp}</p>
                <p class="par">{datas[1].resp}</p>
                <p class="par">{datas[2].resp}</p>
                <p class="par">{datas[3].resp}</p>
                <p class="par">{datas[4].resp}</p>
                <p class="par">{datas[5].resp}</p>
            </div>
            <div class="float-dc">Close<hr>
                <p class="par">{datas[0].close}</p>
                <p class="par">{datas[1].close}</p>
                <p class="par">{datas[2].close}</p>
                <p class="par">{datas[3].close}</p>
                <p class="par">{datas[4].close}</p>
                <p class="par">{datas[5].close}</p>
            </div>
            <div class="float-st">Status<hr>
                <p class="par" style='background-color:{status_clr[0]};'>{datas[0].stat}</p>
                <p class="par" style='background-color:{status_clr[1]};'>{datas[1].stat}</p>
                <p class="par" style='background-color:{status_clr[2]};'>{datas[2].stat}</p>
                <p class="par" style='background-color:{status_clr[3]};'>{datas[3].stat}</p>
                <p class="par" style='background-color:{status_clr[4]};'>{datas[4].stat}</p>
                <p class="par" style='background-color:{status_clr[5]};'>{datas[5].stat}</p>
            </div>
        </div>
    """,unsafe_allow_html=True)

def plant_supplier_ppm():
    # **************** Plant PPM & Supplier PPM **************************#
    current_date()
    st.subheader("Plant and Supplier PPM Trend")
    bar_graph("PLANT PPM & SUPPLIER PPM")
    ppm_data = fetch_data("PLANT PPM & SUPPLIER PPM")
    ppm_data['DATE'] = pd.to_datetime(ppm_data['DATE']) # Convert the "DATE" column to datetime
    current_month = datetime.now().month    # Get the current month
    filtered_ppm_data = ppm_data[ppm_data['DATE'].dt.month == current_month]  # Filter the DataFrame for the current month
    # st.write(ppm_data["DATE"][0])
    filter_plant_data = ppm_data[ppm_data["CATEGORY"] == "PLANT PPM"]
    filter_supplier_data = ppm_data[ppm_data["CATEGORY"] == "SUPPLIER PPM"]
    # st.write(filter_supplier_data)
    total_plant_target = filter_plant_data['TARGET'].sum()    # Sum all the values in the "Value" column
    total_plant_quantity = filter_plant_data['QUANTITY'].sum()
    total_plant_rejection = filter_plant_data['REJECTION'].sum()
    total_plant_actual = round(((total_plant_rejection / total_plant_quantity) * 1000000), 2)
    total_supplier_target = filter_supplier_data['TARGET'].sum()
    total_supplier_quantity = filter_supplier_data['QUANTITY'].sum()
    total_supplier_rejection = filter_supplier_data['REJECTION'].sum()
    total_supplier_actual = round(((total_supplier_rejection / total_supplier_quantity) * 1000000), 2)
    # st.write(total_supplier_actual)

    # st.write(f"total value is = {total_moth_target}")
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
                <p >{"plant_prob.problem"}</p>
                <p >prbl2</p>
                <p >prbl3</p>
            </div>
            <div class="ftp_prb" style='width:25%'>Part/Line<hr style='margin:0.15rem;'>
                <p >{"plant_prob.part_line"}</p>
                <p >prt_ln2</p>
                <p >prt_ln3</p>
            </div>
            <div class="ftp_prb" style='width:25%'>Rej Qty<hr style='margin:0.15rem;'>
                <p >{"plant_prob.rej_qty"}</p>
                <p >rjqt2</p>
                <p >rjqt3</p>
            </div>
        </div>
        """,unsafe_allow_html=True)
        st.markdown(f"""
            <div style='padding-top:0.5rem;'>
                <div class="float-container">
                <div class="ftp_prb" style='font-weight:bold; width:50%'>Problems<hr style='margin:0.15rem;'>
                    <p >{"supplier_prob.problem"}</p>
                    <p >a</p>
                    <p >a</p>
                </div>
                <div class="ftp_prb" style='font-weight:bold; width:25%'>Part/Line<hr style='margin:0.15rem;'>
                    <p >{"supplier_prob.part_line"}</p>
                    <p >a</p>
                    <p >a</p>
                </div>
                <div class="ftp_prb" style='font-weight:bold; width:25%'>Rej Qty<hr style='margin:0.15rem;'>
                    <p >{"supplier_prob.rej_qty"}</p>
                    <p >a</p>
                    <p >a</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    pass

def ftp_rejection():
    #**************** FTP And Reported Rejection **********************#
    st.subheader("FTP and Reported Rejection Trend")
    bar_graph("FTP AND REPORTED REJECTION")
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
                        <p class="par">{"ftp_today.target"}</p>
                        <p class="par">{"rej_per.target"}</p>
                        <p class="par">{"rej_inr.target"}</p>
                    </div>
                        <div class="float-prt" style='height:10rem; font-size:1rem'>Actual <hr>
                        <p class="par">{"ftp_today.actual"}</p>
                        <p class="par">{"rej_per.actual"}</p>
                        <p class="par">{"rej_inr.actual"}</p>
                    </div>
                </div>
                    
            """
            .replace("prn",(str("Part_No")))
            .replace("irp",(str("Issue_Repo")))
            .replace("cra",(str("Crt_Act")))
            .replace("tda",(str("Trg_Date"))),unsafe_allow_html=True)

    st.markdown(f"""
        <div class="float-container">
            <div class="float-pn">Part number<hr>
                <p class="par">prn</p>
                <p class="par">prn</p>
                <p class="par">prn</p>
            </div>
            <div class="float-ir">Issue Reported<hr>
                <p class="par">irp</p>
                <p class="par">irp</p>
                <p class="par">irp</p>
            </div>
            <div class="float-ca">Corrective Action<hr>
                <p class="par">cra</p>
                <p class="par">cra</p>
                <p class="par">cra</p>
            </div>
            <div class="float-td">Targate Date<hr>
                <p class="par">tda</p>
                <p class="par">tda</p>
                <p class="par">tda</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
#************************** Quality_FTD End **************************#