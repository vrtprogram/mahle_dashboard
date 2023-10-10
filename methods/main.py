import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
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
            <div style="margin-bottom:0.6rem; font-family:fantasy"><i><u><h1>heading</h1></u></i></div>
        </center>""".replace("heading",str(head)),unsafe_allow_html=True
    )
    st.markdown("___")

def current_updates():
    d_col1, d_col2=st.columns((1,0.3))
    with d_col1:
        st.link_button("Home","/App")
    with d_col2:
        global on_date
        on_date = st.date_input(":green[Select Date:]")
#************ Body layout End ************#


#************ Safety_FTD Start ************#
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

def incident_tracking():
    try:
        new_dict = {
            "Recordable Lost Time": 0,
            "Recordable Accident": 0,
            "First Aid": 0,
            "Near MIS": 0,
            "Fire": 0
        }
        rows = fatch_incident_data()
        for i in rows:
            # print(i)
            date_from_db = i[1]
            category = i[2]
            if date_from_db == f"{on_date}":
                if category == "Recordable Loss Time Injury MTD":
                    new_dict["Recordable Lost Time"] +=1
                if category == "First Aid MTD":
                    new_dict["First Aid"] +=1
                if category == "Recordable Accident MTD": 
                    new_dict["Recordable Accident"] +=1
                if category == "Near MIS MTD":
                    new_dict["Near MIS"] +=1
                if category == "Fire MTD":
                    new_dict["Fire"] +=1
        cl1,cl2,cl3=st.columns((1,4,1))
        with cl2:
            st.markdown(""" <center><div style='font-size:1.5rem;font-weight:bold;'><u>SAFETY INCIDENTS TRACKING</u></div></center>""",unsafe_allow_html=True)
        # on_date = st.date_input("Data on:")
        # st.write(on_date)
        cr11,cr12,cr13,cr14,cr15=st.columns((1,1,1,1,1))
        with cr11:
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:1rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Lost Time Injury FTD:
                        <h4 style='color:white;font-weight:bold;'>{new_dict["Recordable Lost Time"]}</h4></div>""",unsafe_allow_html=True)
        with cr12:
            st.markdown(f"""<div style='background-color:red;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Accident FTD:
                        <h4 style='color:white;font-weight:bold;'>{new_dict["Recordable Accident"]}</h4></div>""",unsafe_allow_html=True)
        with cr13:
            st.markdown(f"""<div style='background-color:orange;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>First Aid FTD:
                        <h4 style='color:white;font-weight:bold;'>{new_dict["First Aid"]}</h4></div>""",unsafe_allow_html=True)
        with cr14:
            st.markdown(f"""<div style='background-color:yellow;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Near MIS FTD:
                        <h4 style='color:white;font-weight:bold;'>{new_dict["Near MIS"]}</h4></div>""",unsafe_allow_html=True)
        with cr15:
            st.markdown(f"""<div style='background-color:skyblue;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Fire FTD:
                        <h4 style='color:white;font-weight:bold;'>{new_dict["Fire"]}</h4></div>""",unsafe_allow_html=True)
        pass
    except Exception as e:
        print("An error: ", str(e))
        pass


def incident_detail():
    try:
        Record_lost_time = data("Incident", "time", "location", "medical", "action")
        First_aid = data("Incident", "time", "location", "medical", "action")
        Near_mis = data("Incident", "time", "location", "medical", "action")
        Fire_mtd = data("Incident", "time", "location", "medical", "action")
        rows = fatch_incident_data()
        for i in rows:
            # print(i)
            date_from_db = i[1]
            category = i[2]
            incident = data(i[3], i[8], i[4], i[5], i[6])
            if date_from_db == f"{on_date}":
                if category == "Recordable Loss Time Injury MTD":
                    Record_lost_time = incident
                if category == "First Aid MTD":
                    First_aid = incident
                if category == "Near MIS MTD":
                    Near_mis = incident
                if category == "Fire MTD":
                    Fire_mtd = incident
        col1,col2=st.columns((1,1.7))
        with col1:
            st.subheader(f":green[Status as on: {on_date}]",divider="rainbow")
            st.image(
                "resources\ssafety.png",
                use_column_width=True,
                output_format="auto",
            )
            # with colr2:
            #     st.write("""<div style='padding-top:10rem;'></div>""",unsafe_allow_html=True)  
            #     annotated_text(annotation("Rec Lost Time Injury:",color="red",background="skyblue"))
            #     annotated_text(annotation("Rec Accident:",color="brown",background="skyblue"))
            #     annotated_text(annotation("First Aid:",color="orange",background="skyblue"))
            #     annotated_text(annotation("Near MIS:",color="yellow",background="skyblue"))
            #     annotated_text(annotation("Fire:",color="blue",background="skyblue"))
            #     annotated_text(annotation("No Incident:",color="green",background="skyblue"))
            # with colr3:
            #     st.write("""<div style='padding-top:10rem;'></div>""",unsafe_allow_html=True)
            #     st.write(f"{new_dict['Recordable Lost Time']}")
            #     st.write(f"{new_dict['Recordable Accident']}")
            #     st.write(f"{new_dict['First Aid']}")
            #     st.write(f"{new_dict['Near MIS']}")
            #     st.write(f"{new_dict['Fire']}")
            #     st.write("0")
        with col2:
            st.subheader(":green[Safety Incident Details]",divider="rainbow")
            st.markdown(f"""
                        <style>
                            .float-container {{ padding: 5px; }}
                            .float-cat {{ width: 15%; font-size:0.7rem; float: left; height:8rem; text-align:center; padding: 10px; border: 2px solid black;
                            }}
                            .float-inc {{ width: 40%; font-size:0.7rem; float: left; height:8rem; text-align:center; padding: 2.5rem; border: 2px solid black;
                            }}
                            .float-date {{ width: 15%; font-size:0.7rem; float: left; font-weight:bold; height:8rem; text-align:center; padding: 10px; border: 2px solid black;
                            }}
                            .float-loc {{ width: 18%; font-size:0.7rem; float: left; font-weight:bold; height:8rem; text-align:center; padding: 10px; border: 2px solid black;
                            }}
                            .float-med {{ width: 12%; font-size:0.7rem; float: left; font-weight:bold; height:8rem; text-align:center; padding: 10px; border: 2px solid black;
                            }}
                            .float-pact {{ width: 20%; font-size:0.8rem; float: left; height:8rem; text-align:center; padding: 1rem; font-weight:bold; border: 2px solid black;
                            }}
                            .float-act {{ width: 80%; font-size:0.7rem; float: left; height:8rem; text-align:center; padding: 2rem; border: 2px solid black;
                            }}
                            hr{{ margin:0rem; }}
                        </style>
                <div class="float-container">
                    <div class="float-cat" style='background-color:red;color:white; font-weight:bold;'>
                        <div class="green">Recordable Lost Time Injury, Recordable Accident (Latest)</div>
                    </div>
                    <div class="float-inc">
                        <div class="blue">{Record_lost_time.incident}</div>
                    </div>
                    <div class="float-date">
                        <div style='color:red;'>Time<hr>
                            <h6 style=' font-size:0.65rem; padding-top:1rem'>{Record_lost_time.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div style='color:red;'>Location<hr>
                            <h6 style=' font-size:0.65rem; padding-top:1rem'>{Record_lost_time.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div style='color:red;'>Medical<hr>
                            <h6 style=' font-size:0.65rem; padding-top:1rem'>{Record_lost_time.medical}</h6>
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
                        <div style='color:red;'>Time<hr>
                            <h6 style=' font-size:0.65rem; padding-top:1rem'>{First_aid.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div style='color:red;'>Location<hr>
                            <h6 style=' font-size:0.65rem; padding-top:1rem'>{First_aid.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div style='color:red;'>Medical<hr>
                            <h6 style=' font-size:0.65rem; padding-top:1rem'>{First_aid.medical}</h6>
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
                        <div style='color:red;'>Time<hr>
                            <h6 style='font-size:0.65rem; padding-top:1rem'>{Near_mis.time}</h6>
                            <h6 style='font-size:0.65rem; padding-top:1rem'>{Fire_mtd.time}</h6>
                        </div>
                    </div>
                    <div class="float-loc">
                        <div style='color:red;'>Location<hr>
                            <h6 style='font-size:0.65rem; padding-top:1rem'>{Near_mis.location}</h6>
                            <h6 style='font-size:0.65rem; padding-top:1rem'>{Fire_mtd.location}</h6>
                        </div>
                    </div>
                    <div class="float-med">
                        <div style='color:red;'>Medical<hr>
                            <h6 style='font-size:0.65rem; padding-top:1rem'>{Near_mis.medical}</h6>
                            <h6 style='font-size:0.65rem; padding-top:1rem'>{Fire_mtd.medical}</h6>
                        </div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pact">
                        Preventive Measures Implemented and Lesson Learned
                    </div>
                    <div class="float-act">
                        <p style='font-size:0.7rem;'>Near Mis: {Near_mis.action}</p>
                        <p style='font-size:0.7rem;'>Fire details: {Fire_mtd.action}</p>
                    </div>
                </div>
            """,unsafe_allow_html=True)
            pass
    except Exception as e:
        print("An error: ", str(e))
        pass

#************ Unsafe_Incidences & Practice_Tracking Start ************#
def unsafe_incident_tracking():
    sconn = sqlite3.connect("database/safety.db")
    month = datetime.now().month
    year = datetime.now().year
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
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Lost Time Injury FTD:
                <h4 style='color:white;font-weight:bold; padding-top:2rem;'>{Record_lost_time}</h4></div>""",unsafe_allow_html=True)
    with col_indices_B:
        st.markdown(f"""<div style='background-color:red;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Recordable Accident FTD:
                <h4 style='color:white;font-weight:bold; padding-top:2.3rem;'>{record_accident}</h4></div>""",unsafe_allow_html=True)
    with col_indices_C:
        st.markdown(f"""<div style='background-color:orange;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>First Aid FTD:
                <h4 style='color:white;font-weight:bold; padding-top:3.5rem;'>{First_aid}</h4></div>""",unsafe_allow_html=True)
    with col_indices_D:
        st.markdown(f"""<div style='background-color:yellow;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Near MIS FTD:
                <h4 style='color:white;font-weight:bold; padding-top:3.5rem;'>{Near_mis}</h4></div>""",unsafe_allow_html=True)
    with col_indices_E:
        st.markdown(f"""<div style='background-color:skyblue;margin:1rem;padding-top:0.7rem;border:1px solid black;height:12rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Fire FTD:
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

    st.markdown("## Open Observations :")
    df_new = pd.read_sql_query("""SELECT * FROM 'UNSAFE INCIDENCES' WHERE STATUS='Open' ORDER BY DATE DESC """, sconn)
    # df1 = pd.read_sql_query("""SELECT * FROM 'UNSAFE INCIDENCES'""",sconn)   
    # print(df_new)
    sconn.close()
    st.table(df_new[["DATE", "CATEGORY", "EVENT", "ACTION", "LOCATION", "STATUS"]])

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
    st.markdown("## Open Observations :")
    df_new = pd.read_sql_query("""SELECT * FROM 'UNSAFE PRACTICES TRACKING' WHERE STATUS='Open' ORDER BY DATE DESC """, sconn)
    # print(df_new)
    sconn.close()
    st.table(df_new[["DATE", "EVENT", "LOCATION", "STATUS"]])

#************ Unsafe_Practice & Practice_Tracking End ************#

#************ Safety_FTD End ************#


#************ Cost_FTD Start ************#
def cost_ftd():
    col1,col2=st.columns((1,1.9))
    with col1:
        # date=datetime.now().date().strftime("%d-%m-%Y")
        st.subheader(f":blue[Status as on: {on_date}]",divider="rainbow")
        st.image(
            "resources\ctest.png",
            use_column_width=True,
            output_format="auto",
        )
    with col2:
        st.subheader(":blue[PRODUCTIVITY AND OEE]",divider="rainbow")
        blk1,blk2=st.columns((1,1))
        with blk1:
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HUMAN PRODUCTIVITY<hr>
                            <div style='content: "";display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>$1</h6>
                                </div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>$2</h6>
                                </div>
                            </div>
                            </div>""".replace("$1",str("0")).replace("$2",str("0")),unsafe_allow_html=True)
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>PLANT AGGREGATE OEE<hr>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>$1</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>$2</h6>
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
        
        st.subheader(":blue[MACHINE BREAKDOWN TIME]",divider="rainbow")
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
    
    st.subheader(":blue[RAW MATERIAL P.D.I.]",divider="rainbow")
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
    h1_col1, h1_col2 = st.columns((1,1.5))
    with h1_col1:
        st.subheader(":blue[PRODUCTIVITY AND OEE]",divider="rainbow")
    with h1_col2:
        pass
    blk1,blk2=st.columns((1,1))
    with blk1:
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HUMAN PRODUCTIVITY<hr>
                        <div style='content: "";display: table; display:flex;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>$1</h6>
                            </div>
                            <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>$2</h6>
                            </div>
                        </div>
                        </div>""".replace("$1",str("0")).replace("$2",str("0")),unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>PLANT AGGREGATE OEE<hr>
                        <div style='content: center;display: table;display:flex;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>$1</h6>
                            </div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>$2</h6>
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
    h1_col1, h1_col2 = st.columns((1,1.1))
    with h1_col1:
        st.subheader(":blue[RAW MATERIAL P.D.I.]",divider="rainbow")
    with h1_col2:
        pass
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

#************ Cost_FTD End ************#


#************ Delivery_FTD Start ************#
class cmp():
    def __init__(self, target, actual):
        self.target = target
        self.actual = actual
    def show(self):
        return f"Target was {self.target}% and achived {self.actual}%"

def delivery_data_fetch():
    fconn = sqlite3.connect("database/delivery.db")
    cursor = fconn.cursor()
    specific_date = on_date
    query = "SELECT * FROM Delivery WHERE Date = ?"
    cursor.execute(query, (specific_date,))
    rows = cursor.fetchall()
    fconn.close()
    # print(rows)
    # print(type(rows[0]))
    # st.write(rows[0][3])
    return rows
     
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
    rows = delivery_data_fetch()
    for i in rows:
        # print(i)
        if i[1] == f"{on_date}":
            # oe = cmp(i[2],i[3])
            # st.write(oe.show())
            # print(oe.show())
            if i[5] == "OE":
                oe = cmp(i[2],i[3])
            if i[5] == "AFM":
                aftermarket = cmp(i[2],i[3])
            if i[5] == "OES":
                oe_spares = cmp(i[2],i[3])
            if i[5] == "EXP":
                export = cmp(i[2],i[3])
            if i[5] == "MSIL":
                msil = cmp(i[2],i[3])
            if i[5] == "HD":
                hd = cmp(i[2],i[3])
            if i[5] == "HONDA":
                honda = cmp(i[2],i[3])
            if i[5] == "RNAIPL":
                rnaipl = cmp(i[2],i[3])
            if i[5] == "GM":
                gm = cmp(i[2],i[3])
            if i[5] == "FORD":
                ford = cmp(i[2],i[3])
    col1,col2=st.columns((1,1.9))
    with col1:
        # date=datetime.now().date().strftime("%d-%m-%Y")
        st.subheader(f":blue[Status as on: {on_date}]",divider="rainbow")
        st.image(
            "resources\dtest.png",
            use_column_width=True,
            output_format="auto",
        )
    with col2:
        st.subheader(":blue[ON TIME IN FULL (OTIF)]",divider="rainbow")
        blk1,blk2=st.columns((1,1))
        with blk1:
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>OE<hr style='margin:0em;'>
                            <div style='content: "";display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{oe.target}%</h6>
                                </div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{oe.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>OE SPARES<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{oe_spares.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{oe_spares.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
        with blk2:
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>AFTERMARKET<hr style='margin:0em;'>
                            <div style='content: "";display: table;display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{aftermarket.target}%</h6>
                                </div>
                                <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{aftermarket.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>EXPORT<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{export.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{export.actual}%</h6>
                                </div>
                            </div>
                            </div>""",unsafe_allow_html=True)
        h1_col1, h1_col2 = st.columns((1,1.1))
        with h1_col1:
            st.subheader(":blue[SALE PLAN VS ACTUAL]",divider="rainbow")
        with h1_col2:
            pass
        st.markdown("""
            <style>
                    .float-container {  padding: 5px;   }
                    .float-bd {width: 9%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                    }
                    .float-hd {width: 9%; font-size:0.7rem; color:black; float: left; word-wrap:break-word; height:7rem; text-align:center; padding: 10px; line-height:1rem; border: 1px solid black;
                    }
                    .float-icu {width: 46%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                    }
                    .float-hcu {width: 46%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:7rem; text-align:center; padding: 10px; line-height:1rem; border: 1px solid black;
                    }
                    .float-hcd {width: 8%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 10px; border: 1px solid black;}
                    .float-dcd {width: 8%; font-size:0.7rem; color:black; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 10px; border: 1px solid black;}
                    .par {padding-top:1rem; font-size:0.7rem; color:black; }
                    hr{ margin:0em; }
            </style>
            <div class="float-container">
                <div class="float-bd">Perticulars</div>
                <div class="float-bd">BUDGETED SALE (B)</div>
                <div class="float-bd">ORDER BOOK (O)</div>
                <div class="float-bd">ACTUAL SALE (S)</div>
                <div class="float-bd">DELTA (S-B)</div>
                <div class="float-bd">DELTA (S-O)</div>
                <div class="float-icu">Costomer Urgencies/Issues</div>
            </div>
            <div class="float-container">
                <div class="float-hd">Perticula</div>
                <div class="float-hd">BUDGETED SALE (B)</div>
                <div class="float-hd">ORDER BOOK (O)</div>
                <div class="float-hd">ACTUAL SALE (S)</div>
                <div class="float-hd">DELTA (S-B)</div>
                <div class="float-hd">DELTA (S-O)</div>
                <div class="float-hcd">Part No</div>
                <div class="float-hcd" style='width:15%;'>Issue Raised</div>
                <div class="float-hcd" style='width:15%;'>Action to be Taken</div>
                <div class="float-hcd">Trgt Date</div>
                <div class="float-dcd">prtn</div>
                <div class="float-dcd" style='width:15%;'>isrs</div>
                <div class="float-dcd" style='width:15%;'>actt</div>
                <div class="float-dcd">trgd</div>
            </div>
        """,unsafe_allow_html=True)
    # CRITICAL COSTOMER PDI
    st.subheader(":blue[CRITICAL COSTOMER P.D.I.]",divider="rainbow")
    bl1,bl2,bl3=st.columns((1,1,1))
    with bl1:
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>MSIL<hr style='margin:0em;'>
                            <div style='content: "";display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{msil.target}%</h6>
                                </div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{msil.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>HD<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{hd.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{hd.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl2:
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HONDA<hr style='margin:0em;'>
                            <div style='content: "";display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{honda.target}%</h6>
                                </div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{honda.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>RNAIPL<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{rnaipl.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{rnaipl.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl3:
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>GM<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{gm.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{gm.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>FORD<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{ford.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{ford.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)

def otif():
    oe = cmp(0,0)
    aftermarket = cmp(0,0)
    oe_spares = cmp(0,0)
    export = cmp(0,0)
    rows = delivery_data_fetch()
    for i in rows:
        # print(i)
        if i[1] == f"{on_date}":
            if i[5] == "OE":
                oe = cmp(i[2],i[3])
            if i[5] == "AFM":
                aftermarket = cmp(i[2],i[3])
            if i[5] == "OES":
                oe_spares = cmp(i[2],i[3])
            if i[5] == "EXP":
                export = cmp(i[2],i[3])
    h1_col1, h1_col2 = st.columns((1,1.2))
    with h1_col1:
        st.subheader(":blue[ON TIME IN FULL (OTIF)]",divider="rainbow")
    with h1_col2:
        pass
    blk1,blk2=st.columns((1,1))
    with blk1:
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>OE<hr style='margin:0em;'>
                        <div style='content: "";display: table; display:flex;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>{oe.target}%</h6>
                            </div>
                            <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>{oe.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>OE SPARES<hr style='margin:0em;'>
                        <div style='content: center;display: table;display:flex;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>{oe_spares.target}%</h6>
                            </div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>{oe_spares.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
    with blk2:
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>AFTERMARKET<hr style='margin:0em;'>
                        <div style='content: "";display: table;display:flex;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>{aftermarket.target}%</h6>
                            </div>
                            <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>{aftermarket.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>EXPORT<hr style='margin:0em;'>
                        <div style='content: center;display: table;display:flex;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>{export.target}%</h6>
                            </div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>{export.actual}%</h6>
                            </div>
                        </div>
                        </div>""",unsafe_allow_html=True)

def sale_actual():
    # Sale Plan vs Actual Plan
    h1_col1, h1_col2 = st.columns((1,1.1))
    with h1_col1:
        st.subheader(":blue[SALE PLAN VS ACTUAL]",divider="rainbow")
    with h1_col2:
        pass
    st.markdown("""
        <style>
                .float-container {  padding: 5px;   }
                .float-bd {width: 9%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                }
                .float-hd {width: 9%; font-size:0.7rem; color:black; float: left; word-wrap:break-word; height:7rem; text-align:center; padding: 10px; line-height:1rem; border: 1px solid black;
                }
                .float-icu {width: 46%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:3rem; text-align:center; padding-top: 0.4rem; border: 1px solid black;
                }
                .float-hcu {width: 46%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:7rem; text-align:center; padding: 10px; line-height:1rem; border: 1px solid black;
                }
                .float-hcd {width: 8%; font-size:0.7rem; color:red; float: left; word-wrap:break-word; height:3rem; text-align:center; padding: 10px; border: 1px solid black;}
                .float-dcd {width: 8%; font-size:0.7rem; color:black; float: left; word-wrap:break-word; height:4rem; text-align:center; padding: 10px; border: 1px solid black;}
                .par {padding-top:1rem; font-size:0.7rem; color:black; }
                hr{ margin:0em; }
        </style>
        <div class="float-container">
            <div class="float-bd">Perticulars</div>
            <div class="float-bd">BUDGETED SALE (B)</div>
            <div class="float-bd">ORDER BOOK (O)</div>
            <div class="float-bd">ACTUAL SALE (S)</div>
            <div class="float-bd">DELTA (S-B)</div>
            <div class="float-bd">DELTA (S-O)</div>
            <div class="float-icu">Costomer Urgencies/Issues</div>
        </div>
        <div class="float-container">
            <div class="float-hd">Perticula</div>
            <div class="float-hd">BUDGETED SALE (B)</div>
            <div class="float-hd">ORDER BOOK (O)</div>
            <div class="float-hd">ACTUAL SALE (S)</div>
            <div class="float-hd">DELTA (S-B)</div>
            <div class="float-hd">DELTA (S-O)</div>
            <div class="float-hcd">Part No</div>
            <div class="float-hcd" style='width:15%;'>Issue Raised</div>
            <div class="float-hcd" style='width:15%;'>Action to be Taken</div>
            <div class="float-hcd">Trgt Date</div>
            <div class="float-dcd">prtn</div>
            <div class="float-dcd" style='width:15%;'>isrs</div>
            <div class="float-dcd" style='width:15%;'>actt</div>
            <div class="float-dcd">trgd</div>
        </div>
    """,unsafe_allow_html=True)

def critcal_customer_pdi():
    msil = cmp(0,0)
    honda = cmp(0,0)
    gm = cmp(0,0)
    hd = cmp(0,0)
    rnaipl = cmp(0,0)
    ford = cmp(0,0)
    rows = delivery_data_fetch()
    for i in rows:
        # print(i)
        if i[1] == f"{on_date}":
            # oe = cmp(i[2],i[3])
            # st.write(oe.show())
            # print(oe.show())
            if i[5] == "MSIL":
                msil = cmp(i[2],i[3])
            if i[5] == "HD":
                hd = cmp(i[2],i[3])
            if i[5] == "HONDA":
                honda = cmp(i[2],i[3])
            if i[5] == "RNAIPL":
                rnaipl = cmp(i[2],i[3])
            if i[5] == "GM":
                gm = cmp(i[2],i[3])
            if i[5] == "FORD":
                ford = cmp(i[2],i[3])

    # CRITICAL COSTOMER PDI
    h1_col1, h1_col2 = st.columns((1,1.1))
    with h1_col1:
        st.subheader(":blue[CRITICAL COSTOMER P.D.I.]",divider="rainbow")
    with h1_col2:
        pass
    bl1,bl2,bl3=st.columns((1,1,1))
    with bl1:
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>MSIL<hr style='margin:0em;'>
                            <div style='content: "";display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{msil.target}%</h6>
                                </div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{msil.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>HD<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{hd.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{hd.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl2:
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>HONDA<hr style='margin:0em;'>
                            <div style='content: "";display: table; display:flex;clear: both;'>
                                <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{honda.target}%</h6>
                                </div>
                                <div style='float: left; width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{honda.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>RNAIPL<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{rnaipl.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{rnaipl.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
    with bl3:
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>GM<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{gm.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{gm.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:mediumseagreen;margin:1rem;padding-top:0.5rem;border:1px solid black;height:8rem;border-radius:0.8rem;font-size:1.2rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>FORD<hr style='margin:0em;'>
                            <div style='content: center;display: table;display:flex;clear: both;'>
                                <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                    <h6 style='color:white;'>{ford.target}%</h6>
                                </div>
                                <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                    <h6 style='color:white;'>{ford.actual}%</h6>
                                </div>
                            </div>
                        </div>""",unsafe_allow_html=True)

#************ Delivery_FTD End ************#


#************ Quality_FTD Start ************#
def quality_ftd():
    col1,col2=st.columns((1,1.8))
    with col1:
        # date=datetime.now().date().strftime("%d-%m-%Y")
        st.subheader(f":blue[Status as on: {on_date}]",divider="rainbow")
        st.image(
            "resources\qtest.png",
            use_column_width=True,
            output_format="auto",
        )
    with col2:
        # **************** Customer Complaints **************************#
        st.subheader(":blue[CUSTOMER COMPLAINTS]",divider="rainbow")
        st.markdown("""
            <style>
                    .float-container {  padding: 5px;   }
                    .float-cn {width: 22%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-cd {width: 35%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-dr {width: 15%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-dc {width: 15%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-st {width: 13%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .par {padding-top:1rem; font-size:0.7rem; color:black; }
                    hr{ margin:0em; }
                    
            </style>
            <div class="float-container">
                <div class="float-cn">Complaints Number<hr>
                <p class="par" style='padding-top:35%;'>comp_no</p>
                </div>
                <div class="float-cd">Complaint details<hr>
                <p class="par">comp_det1</p>
                <p class="par">comp_det2</p>
                <p class="par">comp_det3</p>
                </div>
                <div class="float-dr">Raised<hr>
                <p class="par">comp_rais1</p>
                <p class="par">comp_rais2</p>
                <p class="par">comp_rais3</p>
                </div>
                <div class="float-dc">Close<hr>
                <p class="par">comp_cls1</p>
                <p class="par">comp_cls2</p>
                <p class="par">comp_cls3</p>
                </div>
                <div class="float-st">Status<hr>
                <p class="par">comp_sts1</p>
                <p class="par">comp_sts2</p>
                <p class="par">comp_sts3</p>
                </div>
            </div>
        """.replace("comp_no",(str("test_no")))
        .replace("comp_det1",(str("test_complaint1"))).replace("comp_rais1",(str("test_ris1"))).replace("comp_cls1",(str("test_cls1"))).replace("comp_sts1",(str("CLOSE1")))
        .replace("comp_det2",(str("test_complaint2"))).replace("comp_rais2",(str("test_ris2"))).replace("comp_cls2",(str("test_cls2"))).replace("comp_sts2",(str("CLOSE2")))
        .replace("comp_det3",(str("test_complaint3"))).replace("comp_rais3",(str("test_ris3"))).replace("comp_cls3",(str("test_cls3"))).replace("comp_sts3",(str("CLOSE3"))),unsafe_allow_html=True)
        # **************** Plant PPM & Supplier PPM **************************#
        st.subheader(":blue[PLANT PPM & SUPPLIER PPM]",divider="rainbow")
        cl1,cl2=st.columns((1,2))
        with cl1:
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>PLANT PPM<hr style='margin:0em;'>
                        <div style='content: "";display: table;display:flex;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>$1</h6>
                            </div>
                            <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>$2</h6>
                            </div>
                        </div>
                        </div>""".replace("$1",str("32")).replace("$2",str("13")),unsafe_allow_html=True)
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>SUPPLIER PPM<hr style='margin:0em;'>
                        <div style='content: center;display: table;display:flex;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                                <h6 style='color:white;'>$1</h6>
                            </div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                                <h6 style='color:white;'>$2</h6>
                            </div>
                        </div>
                        </div>""".replace("$1",str("42")).replace("$2",str("52")),unsafe_allow_html=True)
        with cl2:
            st.write("""
                <style>
                        .float-container { padding: 5px;   }
                        .float-prb { width: 50%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                    .float-prt { width: 25%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                </style>
                <div style='padding-top:0.8rem;'>
                        <div class="float-container">
                        <div class="float-prb" style='color:red;height:2rem;'>Problems</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Part/Line</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Rej Qty</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">ppm_prb1</div>
                        <div class="float-prt">ppm_prt1</div>
                        <div class="float-prt">ppm_qty1</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">ppm_prb1</div>
                        <div class="float-prt">ppm_prt1</div>
                        <div class="float-prt">ppm_qty1</div>
                    </div>
                </div>
                <div style='padding-top:0.8rem;'>
                        <div class="float-container">
                        <div class="float-prb" style='color:red;height:2rem;'>Problems</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Part/Line</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Rej Qty</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">spm_prb1</div>
                        <div class="float-prt">spm_prt1</div>
                        <div class="float-prt">spm_qty1</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">spm_prb1</div>
                        <div class="float-prt">spm_prt1</div>
                        <div class="float-prt">spm_qty1</div>
                    </div>
                </div>
            """.replace("ppm_prb1",str("nppb1"))
            .replace("ppm_prt1",str("nppt1"))
            .replace("ppm_qty1",str("nppq1"))
            .replace("ppm_prb2",str("nppb2"))
            .replace("ppm_prt2",str("nppt2"))
            .replace("ppm_qty2",str("nppq2"))
            .replace("spm_prb1",str("sppb1"))
            .replace("spm_prt1",str("sppt1"))
            .replace("spm_qty1",str("sppq1"))
            .replace("spm_prb2",str("sppb2"))
            .replace("spm_prt2",str("sppt2"))
            .replace("spm_qty2",str("sppq2")),unsafe_allow_html=True)

def customer_complaint():
    # **************** Customer Complaints **************************#
    h1_col1, h1_col2 = st.columns((1,1.1))
    with h1_col1:
        st.subheader(":blue[CUSTOMER COMPLAINTS]",divider="rainbow")
    with h1_col2:
        pass
    st.markdown("""
        <style>
                .float-container {  padding: 5px;   }
                .float-cn {width: 22%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                }
                .float-cd {width: 35%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                }
                .float-dr {width: 15%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                }
                .float-dc {width: 15%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                }
                .float-st {width: 13%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:15rem; text-align:center; padding: 10px; border: 1px solid black;
                }
                .par {padding-top:1rem; font-size:0.7rem; color:black; }
                hr{ margin:0em; }
                
        </style>
        <div class="float-container">
            <div class="float-cn">Complaints Number<hr>
            <p class="par" style='padding-top:35%;'>comp_no</p>
            </div>
            <div class="float-cd">Complaint details<hr>
            <p class="par">comp_det1</p>
            <p class="par">comp_det2</p>
            <p class="par">comp_det3</p>
            </div>
            <div class="float-dr">Raised<hr>
            <p class="par">comp_rais1</p>
            <p class="par">comp_rais2</p>
            <p class="par">comp_rais3</p>
            </div>
            <div class="float-dc">Close<hr>
            <p class="par">comp_cls1</p>
            <p class="par">comp_cls2</p>
            <p class="par">comp_cls3</p>
            </div>
            <div class="float-st">Status<hr>
            <p class="par">comp_sts1</p>
            <p class="par">comp_sts2</p>
            <p class="par">comp_sts3</p>
            </div>
        </div>
    """.replace("comp_no",(str("test_no")))
    .replace("comp_det1",(str("test_complaint1"))).replace("comp_rais1",(str("test_ris1"))).replace("comp_cls1",(str("test_cls1"))).replace("comp_sts1",(str("CLOSE1")))
    .replace("comp_det2",(str("test_complaint2"))).replace("comp_rais2",(str("test_ris2"))).replace("comp_cls2",(str("test_cls2"))).replace("comp_sts2",(str("CLOSE2")))
    .replace("comp_det3",(str("test_complaint3"))).replace("comp_rais3",(str("test_ris3"))).replace("comp_cls3",(str("test_cls3"))).replace("comp_sts3",(str("CLOSE3"))),unsafe_allow_html=True)

def plant_supplier_ppm():
    # **************** Plant PPM & Supplier PPM **************************#
    h1_col1, h1_col2 = st.columns((1,1.5))
    with h1_col1:
        st.subheader(":blue[PLANT PPM & SUPPLIER PPM]",divider="rainbow")
    with h1_col2:
        pass
    cl1,cl2=st.columns((1,2))
    with cl1:
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>PLANT PPM<hr style='margin:0em;'>
                    <div style='content: "";display: table;display:flex;clear: both;'>
                        <div style='float: left;width: 50%;padding: 1rem 2rem;font-size:1rem;'>Target
                            <h6 style='color:white;'>$1</h6>
                        </div>
                        <div style='float: left;width: 50%;padding: 1rem 1.5rem;font-size:1rem;'>Actual
                            <h6 style='color:white;'>$2</h6>
                        </div>
                    </div>
                    </div>""".replace("$1",str("32")).replace("$2",str("13")),unsafe_allow_html=True)
        st.markdown(f"""<div style='background-color:tomato;margin:1rem;font-size:1.3rem;padding-top:0.7rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>SUPPLIER PPM<hr style='margin:0em;'>
                    <div style='content: center;display: table;display:flex;clear: both;'>
                        <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;font-size:1rem;'>Target
                            <h6 style='color:white;'>$1</h6>
                        </div>
                        <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;font-size:1rem;'>Actual
                            <h6 style='color:white;'>$2</h6>
                        </div>
                    </div>
                    </div>""".replace("$1",str("42")).replace("$2",str("52")),unsafe_allow_html=True)
    with cl2:
        st.write("""
            <style>
                    .float-container { padding: 5px;   }
                    .float-prb { width: 50%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                }
                .float-prt { width: 25%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                }
            </style>
            <div style='padding-top:0.8rem;'>
                    <div class="float-container">
                    <div class="float-prb" style='color:red;height:2rem;'>Problems</div>
                    <div class="float-prt" style='color:red;height:2rem;'>Part/Line</div>
                    <div class="float-prt" style='color:red;height:2rem;'>Rej Qty</div>
                </div>
                <div class="float-container">
                    <div class="float-prb">ppm_prb1</div>
                    <div class="float-prt">ppm_prt1</div>
                    <div class="float-prt">ppm_qty1</div>
                </div>
                <div class="float-container">
                    <div class="float-prb">ppm_prb1</div>
                    <div class="float-prt">ppm_prt1</div>
                    <div class="float-prt">ppm_qty1</div>
                </div>
            </div>
            <div style='padding-top:0.8rem;'>
                    <div class="float-container">
                    <div class="float-prb" style='color:red;height:2rem;'>Problems</div>
                    <div class="float-prt" style='color:red;height:2rem;'>Part/Line</div>
                    <div class="float-prt" style='color:red;height:2rem;'>Rej Qty</div>
                </div>
                <div class="float-container">
                    <div class="float-prb">spm_prb1</div>
                    <div class="float-prt">spm_prt1</div>
                    <div class="float-prt">spm_qty1</div>
                </div>
                <div class="float-container">
                    <div class="float-prb">spm_prb1</div>
                    <div class="float-prt">spm_prt1</div>
                    <div class="float-prt">spm_qty1</div>
                </div>
            </div>
        """.replace("ppm_prb1",str("nppb1"))
        .replace("ppm_prt1",str("nppt1"))
        .replace("ppm_qty1",str("nppq1"))
        .replace("ppm_prb2",str("nppb2"))
        .replace("ppm_prt2",str("nppt2"))
        .replace("ppm_qty2",str("nppq2"))
        .replace("spm_prb1",str("sppb1"))
        .replace("spm_prt1",str("sppt1"))
        .replace("spm_qty1",str("sppq1"))
        .replace("spm_prb2",str("sppb2"))
        .replace("spm_prt2",str("sppt2"))
        .replace("spm_qty2",str("sppq2")),unsafe_allow_html=True)
    pass

def ftp_rejection():
    #**************** FTP And Reported Rejection **********************#
    h1_col1, h1_col2 = st.columns((1,1.5))
    with h1_col1:
        st.subheader(":blue[FTP And Reported Rejection]",divider="rainbow")
    with h1_col2:
        pass
    st.write("""
                <style>
                     .float-container { padding: 5px;   }
                     .float-prb { width: 55%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                    .float-prt { width: 20%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                    .float-pn {width: 20%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .float-ir {width: 40%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .float-ca {width: 20%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .float-td {width: 15%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .par {padding-top:1rem; font-size:0.7rem; color:black; }
                    hr{ margin:0em; }
                </style>
                <div>
                     <div class="float-container">
                        <div class="float-prb" style='color:red;height:2rem;'>Particular</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Target</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Actual</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">Firtst Time Pass % (FTP)</div>
                        <div class="float-prt">tftp</div>
                        <div class="float-prt">aftp</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">Reported Rejection (Percntage)</div>
                        <div class="float-prt">trp</div>
                        <div class="float-prt">arp</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">Reported Rejection (INR)</div>
                        <div class="float-prt">tri</div>
                        <div class="float-prt">tri</div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pn">Part number<hr><p class="par">prn</p></div>
                    <div class="float-ir">Issue Reported<hr><p class="par">irp</p></div>
                    <div class="float-ca">Corrective Action<hr><p class="par">cra</p></div>
                    <div class="float-td">Targate Date<hr><p class="par">tda</p></div>
                </div>
            """.replace("tftp",(str("Tar_FTP")))
            .replace("aftp",(str("Act_FTP")))
            .replace("trp",(str("Tar_TRP")))
            .replace("trp",(str("Act_TRP")))
            .replace("tri",(str("Tar_TRI")))
            .replace("tri",(str("Act_TRI")))
            .replace("prn",(str("Part_No")))
            .replace("irp",(str("Issue_Repo")))
            .replace("cra",(str("Crt_Act")))
            .replace("tda",(str("Trg_Date"))),unsafe_allow_html=True)
    
def complaint_trend():
    h1_col1, h1_col2 = st.columns((1,1.1))
    with h1_col1:
        st.subheader(":blue[Customer Complaints Trend]",divider="rainbow")
    with h1_col2:
        pass
    st.markdown("weekly and early Graph")
#************ Quality_FTD End ************#