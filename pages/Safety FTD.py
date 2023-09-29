import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import plotly.express as px

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
         <div style="margin-bottom:1rem; font-family:fantasy">
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
    st.markdown("___")
    d_col1, d_col2=st.columns((1,0.3))
    with d_col2:
        on_date = st.date_input(":green[Select Date:]")
        on_time = datetime.now().time().strftime("%H:%M")
        # st.write(on_date)

    new_dict=dict()
    new_dict['Recordable Lost Time']=56
    new_dict['First Aid']=0
    new_dict['Recordable Accident']=0
    new_dict['Near MIS']=0
    new_dict['Fire']=0

    # data=dict()
    # data['INCIDENT_1'] = "testing incident"
    # data['DATETIME_1'] = on_date
    # data['LOCATION_1'] = "Location testing"
    # data['MEDICAL_1']  = True
    # data['ACTION_1']   = "Action taken"

    class data():
        def __init__(self, incident, time, location, medical, action):
            self.incident = incident
            self.time = time
            self.location = location
            self.medical = medical
            self.action = action
        def show(self):
            return f"incident{self.incident} at time {self.time} on location {self.location}, medical given {self.medical} and take action {self.action}"
    data1 = data("incident test",on_time,"tect_loc",True,"action taken")    #Example
    # st.write(data1.show())
    # query="SELECT * FROM 'UNSAFE INCIDENCES' WHERE DATE = ?"
    # cur.execute(query,(on_dat 
    # res=cur.fetchall()
    # st.table(res)
    # *** get data from db ***
    # if df["CATEGORY"] == "Recordable Lost Time":
    #     RLT = data(df["INCIDENT"],df["TIME"],df["LOCATION"],df["MEDICAL"],df["ACTION"])
    # if df["CATEGORY"] == "First Aid":
    #     FA = data(df["INCIDENT"],df["TIME"],df["LOCATION"],df["MEDICAL"],df["ACTION"])
    # if df["CATEGORY"] == "Near MIS" or "Fire":
    #     FNM = data(df["INCIDENT"],df["TIME"],df["LOCATION"],df["MEDICAL"],df["ACTION"])

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

    col1,col2=st.columns((1,1.7))
    with col1:
        # date=datetime.now().date().strftime("%d-%m-%Y")
        st.subheader(f":green[Status as on: {on_date}]",divider="rainbow")
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
        st.markdown("""
                    <style>
                        .float-container { padding: 5px; }
                        .float-cat { width: 15%; font-size:0.7rem; float: left; height:6rem; text-align:center; padding: 10px; border: 2px solid black;
                        }
                        .float-inc { width: 40%; font-size:0.7rem; float: left; height:6rem; text-align:center; padding: 1rem; border: 2px solid black;
                        }
                        .float-date { width: 15%; font-size:0.7rem; float: left; font-weight:bold; height:6rem; text-align:center; padding: 10px; border: 2px solid black;
                        }
                        .float-loc { width: 18%; font-size:0.7rem; float: left; font-weight:bold; height:6rem; text-align:center; padding: 10px; border: 2px solid black;
                        }
                        .float-med { width: 12%; font-size:0.7rem; float: left; font-weight:bold; height:6rem; text-align:center; padding: 10px; border: 2px solid black;
                        }
                        .float-pact { width: 20%; font-size:0.8rem; float: left; height:6rem; text-align:center; padding: 2rem; font-weight:bold; border: 2px solid black;
                        }
                        .float-act { width: 80%; font-size:0.7rem; float: left; height:6rem; text-align:center; padding: 2rem; border: 2px solid black;
                        }
                        hr{ margin:0rem; }
                    </style>
            <div class="float-container">
                <div class="float-cat" style='background-color:red;color:white; font-weight:bold;'>
                    <div class="green">Recordable Lost Time</div>
                </div>
                <div class="float-inc">
                    <div class="blue">rec_incident</div>
                </div>
                <div class="float-date">
                    <div class="blue">Time<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>rec_tm</h6>
                    </div>
                </div>
                <div class="float-loc">
                    <div class="blue">Location<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>rec_loc</h6>
                    </div>
                </div>
                <div class="float-med">
                    <div class="blue">Medical<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>rec_med</h6>
                    </div>
                </div>
            </div>
            <div class="float-container">
                <div class="float-pact">
                    Implement Action
                </div>
                <div class="float-act">
                    rec_action iidnfgnrfv nfgerrtr rtrign nfgwekntg
                </div>
            </div>

            <div class="float-container">
                <div class="float-cat" style='background-color:orange; font-weight:bold;'>
                    <div class="green">First Aid</div>
                </div>
                <div class="float-inc">
                    <div class="blue">incident_2</div>
                </div>
                <div class="float-date">
                    <div class="blue">Time<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>fa_tm</h6>
                    </div>
                </div>
                <div class="float-loc">
                    <div class="blue">Location<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>fa_loc</h6>
                    </div>
                </div>
                <div class="float-med">
                    <div class="blue">Medical<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>fa_med</h6>
                    </div>
                </div>
            </div>
            <div class="float-container">
                <div class="float-pact">
                    Implement Action
                </div>
                <div class="float-act">
                    fa_action
                </div>
            </div>
                    
            <div class="float-container">
                <div class="float-cat" style='background-color:yellow; font-weight:bold;'>
                    <div>Near MIS <input type="checkbox" >
                         Fire Det <input type="checkbox" >
                    </div>
                </div>
                <div class="float-inc">
                    <div class="blue">incident_3</div>
                </div>
                <div class="float-date">
                    <div class="blue">Time<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>nms_tm</h6>
                    </div>
                </div>
                <div class="float-loc">
                    <div class="blue">Location<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>nms_loc</h6>
                    </div>
                </div>
                <div class="float-med">
                    <div class="blue">Medical<hr>
                        <h6 style='color:red; font-size:0.65rem; padding-top:1rem'>nms_med</h6>
                    </div>
                </div>
            </div>
            <div class="float-container">
                <div class="float-pact">
                    Implement Action
                </div>
                <div class="float-act">
                    nms_action
                </div>
            </div>
        """.replace("rec_incident",str("this incident_1 for testing")) #Recordable Incident
        .replace("rec_tm",str(f"{on_time}"))    
        .replace("rec_loc",str("test_loc"))
        .replace("rec_med",str("yes"))
        .replace("rec_action",str("take action_1 and learn lession"))
        .replace("fa_incident",str("this incident_2 for testing"))  #First aid Incident
        .replace("fa_tm",str(f"{on_time}"))
        .replace("fa_loc",str("test_loc"))
        .replace("fa_med",str("yes"))
        .replace("fa_action",str("take action_2 and learn lession"))
        .replace("nms_incident",str("this incident_3 for testing")) #Near MIS Incident
        .replace("nms_tm",str(f"{on_time}"))
        .replace("nms_loc",str("test_loc"))
        .replace("nms_med",str("yes"))
        .replace("nms_action",str("take action_3 and learn lession"))
        ,unsafe_allow_html=True)
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
