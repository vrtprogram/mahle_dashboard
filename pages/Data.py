"""
THIS IS THE PROPERTY OF VR TECHNOLOGIES PLEASE TAKE PERMISSION BEFORE 
REDISTRIBUTION.

TIME UPDATED @
AUTHOR @ SWAPNIL DIWAKAR
"""


# ----------- IMPORTING THE MODULES ----------#
import streamlit as st
import st_aggrid as table
import streamlit_authenticator as stauth
import yaml
from annotated_text import annotated_text
from yaml.loader import SafeLoader
import sqlite3
from datetime import datetime
from methods.test import main
import pandas as pd

#  --- Initializing Database ----


# ---- SETTING BASIC PAGE PARAMETERS AND TOP LOGOS ---- #

st.set_page_config(layout="wide", page_title="Welcome", initial_sidebar_state='collapsed')
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)

# --------------------------------------------------------------#
with open('Assets/test.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # -------------------- Page Layout ----------------------------#
    with st.sidebar:
        authenticator.logout("Logout")
    st.write("<H1>Select From Below Options To Enter Data", unsafe_allow_html=True)

    options = ['', 'Personal', 'Delivery', 'Unsafe Incidences', 'Unsafe Practices Tracking', 'Quality', ]

    selected = st.selectbox('Menu', options=options)
    # -------Data Entry Pages --------------------------------#

    # **************** Personal **************************#
    if selected == 'Personal':
        conn = sqlite3.connect('database/personal.db')
        cur = conn.cursor()
        # PROVIDING OPTIONS
        option = ["", "UPDATE", 'LOG']
        selected = st.selectbox("Select Action To Perform", options=option, index=0)
        # ACTIONS ACCORDING TO OPTIONS
        if selected == 'LOG':
            with st.form("Personal Data", clear_on_submit=False):
                date = st.date_input("Date")
                col1, col2 = st.columns((1, 1), gap="small")
                with col1:
                    total_manpower_req = st.number_input('Planned Manpower Required', format='%d', step=1, min_value=0)
                with col2:
                    total_manpower_present = st.number_input("Total Manpower Present", format='%d', step=1, min_value=0)

                st.write("<u>Breakup of Manpower</u>:", unsafe_allow_html=True)
                col1, col2 = st.columns((2, 2), gap="small")
                with col1:
                    prod_casual = st.number_input("Production Casual", step=1, min_value=0)
                with col2:
                    non_prod_casual = st.number_input("Non Production Casual", step=1, min_value=0)

                summited = st.form_submit_button('Save')
                if summited:
                    # PERFORMING ALL THE CALCULATIONS FOR ON THE DATA
                    total_manpower_absent = total_manpower_req - total_manpower_present
                    total_casual = prod_casual + non_prod_casual
                    try:
                        personal_gap = (
                                ((total_manpower_req - total_manpower_present) / total_manpower_req) * 100).__format__(
                            ".3")
                    except Exception as e:
                        st.write(e)
                        personal_gap = 0
                    # ANNOTATING ALL THE VALUES
                    if personal_gap != 0:
                        annotated_text("Total Manpower Present : ", (f"{total_manpower_present}", "", "green"))
                        annotated_text("Total Staff Present : ",
                                       (f"{total_manpower_present - total_casual}", "", 'green'))
                        annotated_text("Total Casual Present : ", (f'{total_casual}', "", "blue"))
                        annotated_text("Personal Gap : ", (f'{personal_gap}%', "", "red"))

                        # LOGING ALL DATA INTO THE DATA BASE
                        cur.execute(
                            f'INSERT INTO PERSONAL VALUES ("{datetime.now()}","{date}",{total_manpower_req}, {total_manpower_absent},{total_casual})')
                        conn.commit()
                        st.success("Data Saved")

        if selected == 'UPDATE':
            # st.write("Updating Personal")
            date = st.date_input("Select date to update the status")

            if date is not None:
                st.write(f"The Selected date is {date}")
                df = pd.read_sql_query(f'Select * from PERSONAL where date = "{date}"', conn)
                edited_df = st.data_editor(df, width=1600)
                # print(edited_df)
                update = st.button("Data Update")
                if update:
                    try:
                        for _, row in edited_df.iterrows():
                            cur.execute(
                                f'UPDATE PERSONAL SET Manpower_Req = "{row["Manpower_Req"]}",Manpower_Absent = "{row["Manpower_Absent"]}",Casual_Present= "{row["Casual_Present"]}"  WHERE TIME_STAMP = "{row["Time_Stamp"]}" ')
                            conn.commit()
                        st.success("Data Updated")
                    except Exception as e:
                        st.warning(e)
                time_stamp = st.text_input("Enter The Time Stamp To Delete")
                button = st.button("Delete Entry")
                if button:
                    cur.execute(f"DELETE FROM Personal WHERE Time_Stamp = '{time_stamp}'")
                    conn.commit()
                    st.success("Success ")
                    st.rerun()

    # ***************** Delivery ****************************
    if selected == 'Delivery':
        # INITIALIZING THE DATABASE CONNECTION
        conn = sqlite3.connect('database/delivery.db')
        cur = conn.cursor()
        # PROVIDING OPTIONS
        option = ["", "UPDATE", 'LOG']
        selected = st.selectbox("Select Action To Perform", options=option, index=0)
        # ACTIONS ACCORDING TO OPTIONS
        if selected == 'LOG':
            with st.form("Delivery"):
                date = st.date_input("Date")
                col1, col2 = st.columns((2, 2), gap="small")
                with col1:
                    target = st.number_input("Target", step=1, min_value=0)
                with col2:
                    actual = st.number_input("Actual", step=1, min_value=0)
                issue = st.text_input("Issues")

                submit = st.form_submit_button("Save")

                if submit:
                    cur.execute(
                        f"""INSERT INTO DELIVERY VALUES ("{datetime.now()}","{date}", {target}, {actual},"{issue}")""")
                    conn.commit()
                    annotated_text("Delta is : ",
                                   (f'{(((target - actual) / target) * 100).__format__(".3")}%', "", "blue"))
                    st.success("Data Saved")

        if selected == "UPDATE":
            date = st.date_input("Select date to update the status")

            if date is not None:
                st.write(f"The Selected date is {date}")
                df = pd.read_sql_query(f'Select * from DELIVERY where date = "{date}"', conn)
                edited_df = st.data_editor(df, width=1600)
                # print(edited_df)
                update = st.button("Data Update")
                if update:
                    try:
                        for _, row in edited_df.iterrows():
                            cur.execute(
                                f'UPDATE DELIVERY SET ACTUAL = "{row["ACTUAL"]}",TARGET = "{row["TARGET"]}",ISSUES= "{row["ISSUES"]}"  WHERE TIME_STAMP = "{row["Time_Stamp"]}" ')
                            conn.commit()
                        st.success("Data Updated")
                    except Exception as e:
                        st.warning(e)
                time_stamp = st.text_input("Enter The Time Stamp To Delete")
                button = st.button("Delete Entry")
                if button:
                    cur.execute(f"DELETE FROM Delivery WHERE Time_Stamp = '{time_stamp}'")
                    conn.commit()
                    st.success("Success ")
                    st.rerun()

    # ********************** Unsafe Practice Tracking **********************#
    if selected == 'Unsafe Practices Tracking':
        conn = sqlite3.connect('database/safety.db')
        cur = conn.cursor()
        # PROVIDING OPTIONS
        option = ["", 'UPDATE', 'LOG']
        selected = st.selectbox("Select Action to Perform", options=option, index=0)

        # ACTIONS ACCORDING TO THE SELECTED OPTION
        if selected == 'LOG':
            no_event = st.number_input("Enter number of events to log", step=1)
            if no_event > 0:
                with st.form("safety"):
                    date = st.date_input("Date")
                    col1, col2, col3 = st.columns((1, 1, 1))
                    for i in range(0, no_event):
                        with col1:
                            st.text_input("Observation", key=f"event{i}")
                        with col2:
                            st.text_input("Location", key=f"location{i}")
                        with col3:
                            st.selectbox("Current Status", options=['Open', 'Closed'], key=f"status{i}")
                    submit = st.form_submit_button("Save")
                    if submit:
                        for i in range(0, no_event):
                            cur.execute(
                                f"""INSERT INTO 'UNSAFE PRACTICES TRACKING' VALUES ("{datetime.now()}","{date}","{st.session_state[f'event{i}']},",
                                "{st.session_state[f'location{i}']}","{st.session_state[f'status{i}']}")""")
                            conn.commit()
                        st.success("Datas Saved")
        if selected == 'UPDATE':
            date = st.date_input("Select date to update the status")
            if date is not None:
                st.write(f"The Selected date is {date}")
                df = pd.read_sql_query(f"""Select * from 'UNSAFE PRACTICES TRACKING' where date = "{date}" """, conn)
                edited_df = st.data_editor(df, width=1600)
                # print(edited_df)
                update = st.button("Data Update")
                if update:
                    try:
                        for _, row in edited_df.iterrows():
                            cur.execute(
                                f'UPDATE SAFETY SET STATUS = "{row["STATUS"]}",EVENT = "{row["EVENT"]}",LOCATION = "{row["LOCATION"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                            conn.commit()
                        st.success("Data Updated")
                    except Exception as e:
                        st.write(e)
                time_stamp = st.text_input("Enter The Time Stamp To Delete")
                button = st.button("Delete Entry")
                if button:
                    cur.execute(f"DELETE FROM Safety WHERE Time_Stamp = '{time_stamp}'")
                    conn.commit()
                    st.success("Success ")
                    st.rerun()

    # ******************* Unsafe Incidences ***************** #
    if selected == 'Unsafe Incidences':
        conn = sqlite3.connect('database/safety.db')
        cur = conn.cursor()
        # PROVIDING OPTIONS
        option = ["", 'UPDATE', 'LOG']
        selected = st.selectbox("Select Action to Perform", options=option, index=0)

        # ACTIONS ACCORDING TO THE SELECTED OPTION
        if selected == 'LOG':
            no_event = st.number_input("Enter number of events to logS", step=1)
            if no_event > 0:
                with st.form("safety"):
                    date = st.date_input("Date")
                    col1, col2, col3, col4, col5, col6, col7 = st.columns((1,1,1,1,1,1,1))
                    for i in range(0, no_event):
                        with col1:
                            st.selectbox("Category", options=['Recordable Loss Time Injury MTD', 'Recordable Accident MTD', 'First Aid MTD', 'Near MIS MTD', 'Fire MTD'], key=f"category{i}")
                        with col2:
                            st.text_input("Observations", key=f"event{i}")
                        with col3:
                            st.text_input("Location", key=f"location{i}")
                        with col4:
                            st.text_input("Action", key=f"action{i}")
                        with col5:
                            st.selectbox("Medical", options=['yes', 'no'], key=f"medical{i}")
                        with col6:
                            st.selectbox("Status", options=['Open', 'Closed'], key=f"status{i}")
                        with col7:
                            st.time_input("Time", key=f"time{i}")
                    submit = st.form_submit_button("Save")

                    if submit:
                        for i in range(0, no_event):
                            cur.execute(
                                f"""INSERT INTO "UNSAFE INCIDENCES" VALUES ("{datetime.now()}","{date}","{st.session_state[f'category{i}']}","{st.session_state[f'event{i}']}","{st.session_state[f'location{i}']}","{st.session_state[f"medical{i}"]}","{st.session_state[f"action{i}"]}","{st.session_state[f'status{i}']}","{st.session_state[f'time{i}']}")""")
                            conn.commit()
                        st.success("Data Saved")
        if selected == 'UPDATE':
            date = st.date_input("Select date to update the status")
            if date is not None:
                st.write(f"The Selected date is {date}")
                df = pd.read_sql_query(f'Select * from "UNSAFE INCIDENCES" where date = "{date}"', conn)
                edited_df = st.data_editor(df, width=1600)
                # print(edited_df)
                update = st.button("Data Update")
                if update:
                    try:
                        for _, row in edited_df.iterrows():
                            cur.execute(
                                f'UPDATE "UNSAFE INCIDENCES" SET CATEGORY = "{row["CATEGORY"]}",TIME = "{row["TIME"]}",MEDICAL = "{row["MEDICAL"]}",ACTION = "{row["ACTION"]}",STATUS = "{row["STATUS"]}",EVENT = "{row["EVENT"]}",LOCATION = "{row["LOCATION"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                            conn.commit()
                        st.success("Data Updated")
                    except Exception as e:
                        st.write(e)
                time_stamp = st.text_input("Enter The Time Stamp To Delete")
                button = st.button("Delete Entry")
                if button:
                    cur.execute(f"DELETE FROM 'UNSAFE INCIDENCES' WHERE Time_Stamp = '{time_stamp}'")
                    conn.commit()
                    st.success("Success ")
                    st.rerun()

    # ******************* Quality *********************** #
    if selected == 'Quality':
        # st.write("Quality is selected")
        conn = sqlite3.connect('database/quality.db')
        cur = conn.cursor()
        # PROVIDING OPTIONS
        option = ["", 'UPDATE', 'LOG']
        selected = st.selectbox("Select Action to Perform", options=option, index=0)

        # ACTIONS ACCORDING TO THE SELECTED OPTION
        if selected == 'LOG':
            with st.form("Quality"):
                date = st.date_input("Date")
                col1, col2 = st.columns((2, 2))
                with col1:
                    part_name = st.text_input("Enter Part Name or Code")
                with col2:
                    total_production = st.number_input("Enter Total Production Quantity", min_value=0, step=1)
                    total_NG = st.number_input("Enter No. Of NG Parts", min_value=0, step=1)
                issue = st.text_input("Issues")
                submit = st.form_submit_button("Save")

                if submit:
                    query = f'INSERT INTO QUALITY VALUES ("{datetime.now()}","{date}","{part_name}",{total_production},{total_NG},"{issue}")'
                    cur.execute(query)
                    conn.commit()
                    st.success("Data Saved")

        if selected == 'UPDATE':
            date = st.date_input("Select date to update the status")

            if date is not None:
                st.write(f"The Selected date is {date}")
                df = pd.read_sql_query(f'Select * from QUALITY where date = "{date}"', conn)
                edited_df = st.data_editor(df, width=1600)
                # print(edited_df)
                update = st.button("Data Update")
                if update:
                    try:
                        for _, row in edited_df.iterrows():
                            cur.execute(
                                f'UPDATE QUALITY SET PART_NAME = "{row["PART_NAME"]}",TOTAL_PRODUCTION = "{row["TOTAL_PRODUCTION"]}",TOTAL_NG = "{row["TOTAL_NG"]}", ISSUE = "{row["ISSUE"]}" WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                            conn.commit()
                        st.success("Data Updated")
                    except Exception as e:
                        st.write(e)
                time_stamp = st.text_input("Enter The Time Stamp To Delete")
                button = st.button("Delete Entry")
                if button:
                    cur.execute(f"DELETE FROM Personal WHERE Time_Stamp = '{time_stamp}'")
                    conn.commit()
                    st.success("Success ")
                    st.rerun()

    if selected == '':
        annotated_text(("Welcome to Database Manager , You can Update the database here !!!", "", "green"))
