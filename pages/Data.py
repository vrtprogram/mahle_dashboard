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

    options = ['', 'Safety', 'Quality', 'Delivery', 'Cost', 'Personal', ]

    selected = st.selectbox('Menu', options=options)
    # -------Data Entry Pages --------------------------------#

    # **************** Personal **************************#
    if selected == 'Personal':
        with sqlite3.connect('database/personal.db') as conn:
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

    # ***************** Delivery ****************************#
    if selected == 'Delivery':
        c_opt = ['', 'OTIF & Critical Customer PDI', 'Sale Plan vs Actual']
        slct = st.selectbox('Delivery', options=c_opt)
        if slct == 'OTIF & Critical Customer PDI':
            # INITIALIZING THE DATABASE CONNECTION
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                # PROVIDING OPTIONS
                option = ["", "UPDATE", 'LOG']
                selected = st.selectbox("Delivery", options=option, index=0)
                # ACTIONS ACCORDING TO OPTIONS
                if selected == 'LOG':
                    no_event = st.number_input("Enter number of events to log", step=1)
                    if no_event > 0:
                        with st.form("Delivery"):
                            date = st.date_input("Date")
                            col1, col2, col3 = st.columns((1,1,1), gap="small")
                            for i in range(0, no_event):
                                with col1:
                                    st.selectbox("Category", options=['OE', 'AfterMarket', 'OE_Spare', 'Export', 'MSIL', 'Honda', 'GM', 'HD', 'RNAIPL', 'Ford'], key=f"category{i}")
                                with col2:
                                    target = st.number_input("Target", step=1, min_value=0, key=f"target{i}")
                                with col3:
                                    actual = st.number_input("Actual", step=1, min_value=0, key=f"actual{i}")
                                # with col4:
                                #     issue = st.text_input("Issues", key=f"issue{i}")
                            submit = st.form_submit_button("Save")

                            if submit:
                                for i in range(0, no_event):
                                    cur.execute(
                                        f"""INSERT INTO 'OTIF_CC PDI' VALUES ("{datetime.now()}","{date}","{st.session_state[f"category{i}"]}","{st.session_state[f'target{i}']}","{st.session_state[f'actual{i}']}")""")
                                    conn.commit()
                                annotated_text("Delta is : ",
                                            (f'{(((target - actual) / target) * 100).__format__(".3")}%', "", "blue"))
                                st.success("Data Saved")
                if selected == "UPDATE":
                    date = st.date_input("Select date to update the status")
                    if date is not None: 
                        st.write(f"The Selected date is {date}")
                        df = pd.read_sql_query(f'Select * from "OTIF_CC PDI" where date = "{date}"', conn)
                        edited_df = st.data_editor(df, width=1600)
                        # print(edited_df)
                        update = st.button("Data Update")
                        if update:
                            try:
                                for _, row in edited_df.iterrows():
                                    cur.execute(
                                        f'UPDATE "OTIF_CC PDI" SET CATEGORY = "{row["CATEGORY"]}", ACTUAL = "{row["ACTUAL"]}",TARGET = "{row["TARGET"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                    conn.commit()
                                st.success("Data Updated")
                            except Exception as e:
                                st.warning(e)
                        time_stamp = st.text_input("Enter The Time Stamp To Delete")
                        button = st.button("Delete Entry")
                        if button:
                            cur.execute(f"DELETE FROM 'OTIF_CC PDI' WHERE Time_Stamp = '{time_stamp}'")
                            conn.commit()
                            st.success("Success ")
                            st.rerun()

        if slct == 'Sale Plan vs Actual':
            # INITIALIZING THE DATABASE CONNECTION
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                opt = ["", "DATA", "ISSUE"]
                slct = st.selectbox("Sale Plan vs Actual", options=opt, index=0)
                if slct == "DATA":
                    option = ["", "UPDATE", "LOG"]
                    selected = st.selectbox('DATA', options=option, index=0)
                    # ACTIONS ACCORDING TO OPTIONS
                    if selected == "LOG":
                        no_event = st.number_input("Enter number of events to log", step=1)
                        if no_event > 0:
                            with st.form("Delivery"):
                                date = st.date_input("Date")
                                col1, col2, col3 = st.columns((1,1,1), gap="small")
                                for i in range(0, no_event):
                                    with col1:
                                        budgeted_sale = st.number_input("Budgeted Sale", step=1, min_value=0, key=f"budgeted_sale{i}")
                                    with col2:
                                        order_book = st.number_input("Order Book", step=1, min_value=0, key=f"order_book{i}")
                                    with col3:
                                        actual_sale = st.number_input("Actual Sale", step=1, min_value=0, key=f"actual_sale{i}")
                                submit = st.form_submit_button("Save")

                                if submit:
                                    for i in range(0, no_event):
                                        cur.execute(
                                            f"""INSERT INTO 'SALE PLAN VS ACTUAL' (TIME_STAMP, DATE, 'BUDGETED SALE', 'ORDER BOOK', 'ACTUAL SALE') VALUES ("{datetime.now()}","{date}","{st.session_state[f"budgeted_sale{i}"]}","{st.session_state[f"order_book{i}"]}","{st.session_state[f"actual_sale{i}"]}")""")
                                        conn.commit()
                                    st.success("Data Saved")
                    if selected == "UPDATE":
                        date = st.date_input("Select date to update the status")
                        if date is not None: 
                            st.write(f"The Selected date is {date}")
                            df = pd.read_sql_query(f'Select * from "SALE PLAN VS ACTUAL" where date = "{date}"', conn)
                            edited_df = st.data_editor(df, width=1600)
                            # print(edited_df)
                            update = st.button("Data Update")
                            if update:
                                try:
                                    for _, row in edited_df.iterrows():
                                        cur.execute(
                                            f'UPDATE "SALE PLAN VS ACTUAL" SET "BUDGETED SALE" = "{row["BUDGETED SALE"]}","ORDER BOOK" = "{row["ORDER BOOK"]}","ACTUAL SALE" = "{row["ACTUAL SALE"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                        conn.commit()
                                    st.success("Data Updated")
                                except Exception as e:
                                    st.warning(e)
                            time_stamp = st.text_input("Enter The Time Stamp To Delete")
                            button = st.button("Delete Entry")
                            if button:
                                cur.execute(f"DELETE FROM 'SALE PLAN VS ACTUAL' WHERE Time_Stamp = '{time_stamp}'")
                                conn.commit()
                                st.success("Success ")
                                st.rerun()
                
                if slct == "ISSUE":
                    option = ["", "UPDATE", "LOG"]
                    selected = st.selectbox('ISSUE', options=option, index=0)
                    # ACTIONS ACCORDING TO OPTIONS
                    if selected == "LOG":
                        no_event = st.number_input("Enter number of events to log", step=1)
                        if no_event > 0:
                            with st.form("Delivery"):
                                date = st.date_input("Date")
                                col1, col2, col3, col4= st.columns((1,1,1,1), gap="small")
                                for i in range(0, no_event):
                                    with col1:
                                        st.text_input("Part", key=f"part{i}")
                                    with col2:
                                        st.text_input("Issue", key=f"issue{i}")
                                    with col3:
                                        st.text_input("Action", key=f"action{i}")
                                    with col4:
                                        st.date_input("Target_date", key=f"t_date{i}")
                                        pass
                                submit = st.form_submit_button("Save")

                                if submit:
                                    for i in range(0, no_event):
                                        cur.execute(
                                            f"""INSERT INTO 'DELIVERY ISSUES' VALUES ("{datetime.now()}","{date}","{st.session_state[f'part{i}']}","{st.session_state[f'issue{i}']}","{st.session_state[f'action{i}']}","{st.session_state[f't_date{i}']}")""")
                                        conn.commit()
                                    st.success("Data Saved")
                    if selected == "UPDATE":
                        date = st.date_input("Select date to update the status")
                        if date is not None: 
                            st.write(f"The Selected date is {date}")
                            df = pd.read_sql_query(f'Select * from "DELIVERY ISSUES" where date = "{date}"', conn)
                            edited_df = st.data_editor(df, width=1600)
                            # print(edited_df)
                            update = st.button("Data Update")
                            if update:
                                try:
                                    for _, row in edited_df.iterrows():
                                        cur.execute( 
                                            f'UPDATE "DELIVERY ISSUES" SET "PART NO" = "{row["PART NO"]}","ISSUE RAISED" = "{row["ISSUE RAISED"]}","ACTION" = "{row["ACTION"]}","TARGET DATE" = "{row["TARGET DATE"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                        conn.commit()
                                    st.success("Data Updated")
                                except Exception as e:
                                    st.warning(e)
                            time_stamp = st.text_input("Enter The Time Stamp To Delete")
                            button = st.button("Delete Entry")
                            if button:
                                cur.execute(f"DELETE FROM 'DELIVERY ISSUES' WHERE Time_Stamp = '{time_stamp}'")
                                conn.commit()
                                st.success("Success ")
                                st.rerun()
            pass

    # ********************** Safety **********************#
    if selected == 'Safety':
        c_opt = ['', 'Unsafe Incidences', 'Unsafe Practices Tracking']
        slct = st.selectbox('Safety', options=c_opt)

        if slct == 'Unsafe Practices Tracking':
            with sqlite3.connect('database/safety.db') as conn:
                cur = conn.cursor()
                # PROVIDING OPTIONS
                option = ["", 'UPDATE', 'LOG']
                selected = st.selectbox("Unsafe Practices Tracking", options=option, index=0)
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

        if slct == 'Unsafe Incidences':
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                # PROVIDING OPTIONS
                option = ["", 'UPDATE', 'LOG']
                selected = st.selectbox("Unsafe Incidences", options=option, index=0)

                # ACTIONS ACCORDING TO THE SELECTED OPTION
                if selected == 'LOG':
                    no_event = st.number_input("Enter number of events to logS", step=1)
                    if no_event > 0:
                        with st.form("safety"):
                            date = st.date_input("Date")
                            col1, col2, col3, col4, col5, col6, col7 = st.columns((1,1,1,1,1,1,1))
                            for i in range(0, no_event):
                                with col1:
                                    st.selectbox("Category", options=['Recordable Loss Time Injury', 'Recordable Accident', 'First Aid', 'Near MIS', 'Fire'], key=f"category{i}")
                                with col2:
                                    st.text_input("Observations", key=f"event{i}")
                                with col3:
                                    st.text_input("Value_stream", key=f"value_stream{i}")
                                with col4:
                                    st.text_input("Action", key=f"action{i}")
                                with col5:
                                    st.selectbox("Medical", options=['yes', 'no'], key=f"medical{i}")
                                with col6:
                                    st.selectbox("Status", options=['Open', 'Closed', 'Inprocess'], key=f"status{i}")
                                with col7:
                                    st.time_input("Time", key=f"time{i}")
                            submit = st.form_submit_button("Save")

                            if submit:
                                for i in range(0, no_event):
                                    cur.execute(
                                        f"""INSERT INTO "INCIDENCES DETAILS" VALUES ("{datetime.now()}","{date}","{st.session_state[f'time{i}']}","{st.session_state[f'category{i}']}","{st.session_state[f'event{i}']}","{st.session_state[f'value_stream{i}']}","{st.session_state[f"medical{i}"]}","{st.session_state[f"action{i}"]}","{st.session_state[f'status{i}']}")""")
                                    conn.commit()
                                st.success("Data Saved")
                if selected == 'UPDATE':
                    date = st.date_input("Select date to update the status")
                    if date is not None:
                        st.write(f"The Selected date is {date}")
                        df = pd.read_sql_query(f'Select * from "INCIDENCES DETAILS" where date = "{date}"', conn)
                        edited_df = st.data_editor(df, width=1600)
                        # print(edited_df)
                        update = st.button("Data Update")
                        if update:
                            try:
                                for _, row in edited_df.iterrows():
                                    cur.execute(
                                        f'UPDATE "INCIDENCES DETAILS" SET TIME = "{row["TIME"]}",CATEGORY = "{row["CATEGORY"]}",MEDICAL = "{row["MEDICAL"]}",ACTION = "{row["ACTION"]}",STATUS = "{row["STATUS"]}",EVENT = "{row["EVENT"]}","VALUE STREAM" = "{row["VALUE STREAM"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                    conn.commit()
                                st.success("Data Updated")
                            except Exception as e:
                                st.write(e)
                        time_stamp = st.text_input("Enter The Time Stamp To Delete")
                        button = st.button("Delete Entry")
                        if button:
                            cur.execute(f"DELETE FROM 'INCIDENCES DETAILS' WHERE Time_Stamp = '{time_stamp}'")
                            conn.commit()
                            st.success("Success ")
                            st.rerun()

    # ******************* Quality *********************** #
    if selected == 'Quality':
        c_opt = ['', 'Customer Complaints', 'Plant & Supplier PPM', 'FTP & Reported Rejection']
        slct = st.selectbox('Quality', options=c_opt)
        if slct == 'Customer Complaints':
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                option = ["", "UPDATE", 'LOG']
                selected = st.selectbox("Customer Complaints", options=option, index=0)
                # ACTIONS ACCORDING TO OPTIONS
                if selected == 'LOG':
                        no_event = st.number_input("Enter number of events to log", step=1)
                        if no_event > 0:
                            with st.form("Quality"):
                                date = st.date_input("Date")
                                col1, col2, col3, col4= st.columns((1, 1, 1, 1))
                                for i in range(0, no_event):
                                    with col1:
                                        st.text_input("Complaint", key=f"complaint{i}")
                                    with col2:
                                        st.date_input("Close_date", key=f"close_date{i}")
                                    with col3:
                                        st.text_input("Responsibility", key=f"responsibility{i}")
                                    with col4:
                                        st.selectbox("Current Status", options=['Open', 'Closed', 'Inprocess'], key=f"status{i}")
                                submit = st.form_submit_button("Save")
                                if submit:
                                    for i in range(0, no_event):
                                        cur.execute(
                                            f"""INSERT INTO 'CUSTOMER COMPLAINTS' VALUES ("{datetime.now()}","{date}","{st.session_state[f'complaint{i}']}",
                                            "{date}","{st.session_state[f'close_date{i}']}","{st.session_state[f'status{i}']}","{st.session_state[f'responsibility{i}']}")""")
                                        conn.commit()
                                    st.success("Datas Saved")
                if selected == 'UPDATE':
                    date = st.date_input("Select date to update the status")
                    if date is not None:
                        st.write(f"The Selected date is {date}")
                        df = pd.read_sql_query(f"""Select * from 'CUSTOMER COMPLAINTS' where date = "{date}" """, conn)
                        edited_df = st.data_editor(df, width=1600)
                        # print(edited_df)
                        update = st.button("Data Update")
                        if update:
                            try:
                                for _, row in edited_df.iterrows():
                                    cur.execute(
                                        f'UPDATE "CUSTOMER COMPLAINTS" SET STATUS = "{row["STATUS"]}",COMPLAINT = "{row["COMPLAINT"]}","RAISE DATE" = "{row["RAISE DATE"]}","RESPONSIBILITY" = "{row["RESPONSIBILITY"]}","TARGET DATE" = "{row["TARGET DATE"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                    conn.commit()
                                st.success("Data Updated")
                            except Exception as e:
                                st.write(e)
                        time_stamp = st.text_input("Enter The Time Stamp To Delete")
                        button = st.button("Delete Entry")
                        if button:
                            cur.execute(f"DELETE FROM 'CUSTOMER COMPLAINTS' WHERE Time_Stamp = '{time_stamp}'")
                            conn.commit()
                            st.success("Success ")
                            st.rerun()

        if slct == 'Plant & Supplier PPM':
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                opt = ["", "PLANT_SUPPLIER_PPM DATA", 'PPM_ISSUE']
                slct = st.selectbox("Plant & Supplier PPM", options=opt, index=0)
                if slct == "PLANT_SUPPLIER_PPM DATA":
                    option = ["", "UPDATE", 'LOG']
                    selected = st.selectbox("PLANT_SUPPLIER_PPM DATA", options=option, index=0)
                    # ACTIONS ACCORDING TO OPTIONS
                    if selected == 'LOG':
                            no_event = st.number_input("Enter number of events to log", step=1)
                            if no_event > 0:
                                with st.form("Quality"):
                                    date = st.date_input("Date")
                                    col1, col2, col3, col4= st.columns((1, 1, 1, 1))
                                    for i in range(0, no_event):
                                        with col1:
                                            st.selectbox("Category", options=['PLANT PPM', 'SUPPLIER PPM'], key=f"category{i}")
                                        with col2:
                                            st.number_input("Target", key=f"target{i}")
                                        with col3:
                                            st.number_input("Quantity", key=f"quantity{i}")
                                        with col4:
                                            st.number_input("Rejection", key=f"rejection{i}")
                                    submit = st.form_submit_button("Save")
                                    if submit:
                                        for i in range(0, no_event):
                                            cur.execute( 
                                                f"""INSERT INTO 'PLANT PPM & SUPPLIER PPM' VALUES ("{datetime.now()}","{date}","{st.session_state[f'category{i}']}",
                                                "{st.session_state[f'target{i}']}","{st.session_state[f'quantity{i}']}","{st.session_state[f'rejection{i}']}")""")
                                            conn.commit()
                                        st.success("Datas Saved")
                    if selected == 'UPDATE':
                        date = st.date_input("Select date to update the status")
                        if date is not None:
                            st.write(f"The Selected date is {date}")
                            df = pd.read_sql_query(f"""Select * from 'PLANT PPM & SUPPLIER PPM' where date = "{date}" """, conn)
                            edited_df = st.data_editor(df, width=1600)
                            # print(edited_df)
                            update = st.button("Data Update")
                            if update:
                                try:
                                    for _, row in edited_df.iterrows():
                                        cur.execute(
                                            f'UPDATE "PLANT PPM & SUPPLIER PPM" SET CATEGORY = "{row["CATEGORY"]}",TARGET = "{row["TARGET"]}","QUANTITY" = "{row["QUANTITY"]}","REJECTION" = "{row["REJECTION"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                        conn.commit()
                                    st.success("Data Updated")
                                except Exception as e:
                                    st.write(e)
                            time_stamp = st.text_input("Enter The Time Stamp To Delete")
                            button = st.button("Delete Entry")
                            if button:
                                cur.execute(f"DELETE FROM 'PLANT PPM & SUPPLIER PPM' WHERE Time_Stamp = '{time_stamp}'")
                                conn.commit()
                                st.success("Success ")
                                st.rerun()

                if slct == "PPM_ISSUE":
                    option = ["", "UPDATE", 'LOG']
                    selected = st.selectbox("PPM PROBLEMS", options=option, index=0)
                    # ACTIONS ACCORDING TO OPTIONS
                    if selected == 'LOG':
                            no_event = st.number_input("Enter number of events to log", step=1)
                            if no_event > 0:
                                with st.form("Quality"):
                                    date = st.date_input("Date")
                                    col1, col2, col3, col4= st.columns((1, 1, 1, 1))
                                    for i in range(0, no_event):
                                        with col1:
                                            st.selectbox("Category", options=['PLANT PPM', 'SUPPLIER PPM'], key=f"category{i}")
                                        with col2:
                                            st.text_input("Problem", key=f"problem{i}")
                                        with col3:
                                            st.text_input("Part_Line", key=f"part_line{i}")
                                        with col4:
                                            st.number_input("Rej_qty", key=f"rej_qty{i}")
                                    submit = st.form_submit_button("Save")
                                    if submit:
                                        for i in range(0, no_event):
                                            cur.execute( 
                                                f"""INSERT INTO 'PPM PROBLEMS' VALUES ("{datetime.now()}","{date}","{st.session_state[f'category{i}']}",
                                                "{st.session_state[f'problem{i}']}","{st.session_state[f'part_line{i}']}","{st.session_state[f'rej_qty{i}']}")""")
                                            conn.commit()
                                        st.success("Datas Saved")
                    if selected == 'UPDATE':
                        date = st.date_input("Select date to update the status")
                        if date is not None:
                            st.write(f"The Selected date is {date}")
                            df = pd.read_sql_query(f"""Select * from 'PPM PROBLEMS' where date = "{date}" """, conn)
                            edited_df = st.data_editor(df, width=1600)
                            # print(edited_df)
                            update = st.button("Data Update")
                            if update:
                                try:
                                    for _, row in edited_df.iterrows():
                                        cur.execute(
                                            f'UPDATE "PPM PROBLEMS" SET CATEGORY = "{row["CATEGORY"]}",PROBLEM = "{row["PROBLEM"]}","PART_LINE" = "{row["PART_LINE"]}","REJ_QTY" = "{row["REJ_QTY"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                        conn.commit()
                                    st.success("Data Updated")
                                except Exception as e:
                                    st.write(e)
                            time_stamp = st.text_input("Enter The Time Stamp To Delete")
                            button = st.button("Delete Entry")
                            if button:
                                cur.execute(f"DELETE FROM 'PPM PROBLEMS' WHERE Time_Stamp = '{time_stamp}'")
                                conn.commit()
                                st.success("Success ")
                                st.rerun()

        if slct == 'FTP & Reported Rejection':
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                opt = ["", "FTP_REJECTION_DATA", 'ISSUE']
                slct = st.selectbox("FTP & Reported Rejection", options=opt, index=0)
                if slct == "FTP_REJECTION_DATA":
                    option = ["", "UPDATE", 'LOG']
                    selected = st.selectbox("FTP_REJECTION_DATA", options=option, index=0)
                    # ACTIONS ACCORDING TO OPTIONS
                    if selected == 'LOG':
                            no_event = st.number_input("Enter number of events to log", step=1)
                            if no_event > 0:
                                with st.form("Quality"):
                                    date = st.date_input("Date")
                                    col1, col2, col3= st.columns((1, 1, 1))
                                    for i in range(0, no_event):
                                        with col1:
                                            st.selectbox("Category", options=['First Time Pass (%)', 'Reported Rejection (%)', 'Reported Rejection (INR)'], key=f"category{i}")
                                        with col2:
                                            st.number_input("Target", key=f"target{i}")
                                        with col3:
                                            st.number_input("Actual", key=f"actual{i}")
                                    submit = st.form_submit_button("Save")
                                    if submit:
                                        for i in range(0, no_event):
                                            cur.execute(
                                                f"""INSERT INTO 'FTP AND REPORTED REJECTION' VALUES ("{datetime.now()}","{date}","{st.session_state[f'category{i}']}",
                                                "{st.session_state[f'target{i}']}","{st.session_state[f'actual{i}']}")""")
                                            conn.commit()
                                        st.success("Datas Saved")
                    if selected == 'UPDATE':
                        date = st.date_input("Select date to update the status")
                        if date is not None:
                            st.write(f"The Selected date is {date}")
                            df = pd.read_sql_query(f"""Select * from 'FTP AND REPORTED REJECTION' where date = "{date}" """, conn)
                            edited_df = st.data_editor(df, width=1600)
                            # print(edited_df)
                            update = st.button("Data Update")
                            if update:
                                try:
                                    for _, row in edited_df.iterrows():
                                        cur.execute(
                                            f'UPDATE "FTP AND REPORTED REJECTION" SET CATEGORY = "{row["CATEGORY"]}",TARGET = "{row["TARGET"]}","ACTUAL" = "{row["ACTUAL"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                        conn.commit()
                                    st.success("Data Updated")
                                except Exception as e:
                                    st.write(e)
                            time_stamp = st.text_input("Enter The Time Stamp To Delete")
                            button = st.button("Delete Entry")
                            if button:
                                cur.execute(f"DELETE FROM 'FTP AND REPORTED REJECTION' WHERE Time_Stamp = '{time_stamp}'")
                                conn.commit()
                                st.success("Success ")
                                st.rerun()
                if slct == 'ISSUE':
                    option = ["", "UPDATE", 'LOG']
                    selected = st.selectbox("FTP_REJECTION_DATA", options=option, index=0)
                    if selected == 'LOG':
                        no_event = st.number_input("Enter number of events to log", step=1)
                        if no_event > 0:
                            with st.form("Quality"):
                                date = st.date_input("Date")
                                col1, col2, col3, col4= st.columns((1, 1, 1, 1))
                                for i in range(0, no_event):
                                    with col1:
                                        st.text_input("Part_no", key=f"part_no{i}")
                                    with col2:
                                        st.text_input("Issue", key=f"issue{i}")
                                    with col3:
                                        st.text_input("Corrective_Action", key=f"corrective_action{i}")
                                    with col4:
                                        st.date_input("Target_date", key=f"target_date{i}")
                                submit = st.form_submit_button("Save")
                                if submit:
                                    for i in range(0, no_event):
                                        cur.execute(
                                            f"""INSERT INTO 'FTP REJECTION ISSUE' VALUES ("{datetime.now()}","{date}","{st.session_state[f'part_no{i}']}","{st.session_state[f'issue{i}']}","{st.session_state[f'corrective_action{i}']}","{st.session_state[f'target_date{i}']}")""")
                                        conn.commit()
                                    st.success("Datas Saved")
                    if selected == 'UPDATE':
                            date = st.date_input("Select date to update the status")
                            if date is not None:
                                st.write(f"The Selected date is {date}")
                                df = pd.read_sql_query(f"""Select * from 'FTP REJECTION ISSUE' where date = "{date}" """, conn)
                                edited_df = st.data_editor(df, width=1600)
                                # print(edited_df)
                                update = st.button("Data Update")
                                if update:
                                    try:
                                        for _, row in edited_df.iterrows():
                                            cur.execute(
                                                f'UPDATE "FTP REJECTION ISSUE" SET PART NO" = "{row["PART NO"]}",ISSUE = "{row["ISSUE"]}","CORRECTIVE ACTION" = "{row["CORRECTIVE ACTION"]}","TARGET DATE" = "{row["TARGET DATE"]}"  WHERE TIME_STAMP = "{row["TIME_STAMP"]}" ')
                                            conn.commit()
                                        st.success("Data Updated")
                                    except Exception as e:
                                        st.write(e)
                                time_stamp = st.text_input("Enter The Time Stamp To Delete")
                                button = st.button("Delete Entry")
                                if button:
                                    cur.execute(f"DELETE FROM 'FTP REJECTION ISSUE' WHERE Time_Stamp = '{time_stamp}'")
                                    conn.commit()
                                    st.success("Success ")
                                    st.rerun()

    # ******************* Cost *********************** #
    if selected == 'Cost':
        c_opt = ['', 'Productivity and OEE', 'RAW Metarial PDI', 'Machine Breakdown Time']
        slct = st.selectbox('Cost', options=c_opt)
        if slct == 'Productivity and OEE':
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                opt = ["", "Productivity and OEE DATA", 'OEE_ISSUE']
                slct = st.selectbox("Productivity and OEE", options=opt, index=0)
                if slct == "Productivity and OEE DATA":
                    option = ["", "UPDATE", 'LOG']
                    selected = st.selectbox("Productivity and OEE DATA", options=option, index=0)
                    # ACTIONS ACCORDING TO OPTIONS
                    if selected == 'LOG':
                        no_event = st.number_input("Enter number of events to log", step=1)
                        if no_event > 0:
                            with st.form("cost"):
                                date = st.date_input("Date")
                                col1, col2, col3 = st.columns((1, 1, 1))
                                for i in range(0, no_event):
                                    with col1:
                                        st.selectbox("Category", options=['','HUMAN PRODUCTIVITY', 'PLANT AGGREGATE OEE'], key=f"category{i}")
                                    with col2:
                                        st.number_input("Target", key=f"target{i}")
                                    with col3:
                                        st.number_input("Actual", key=f"actual{i}")
                                submit = st.form_submit_button("Save")
                                if submit:
                                    for i in range(0, no_event):
                                        cur.execute(
                                            f"""INSERT INTO 'PRODUCTIVITY AND OEE' VALUES ("{datetime.now()}","{date}","{st.session_state[f'category{i}']}","{st.session_state[f'target{i}']}","{st.session_state[f'actual{i}']}")"""
                                        )
                                    st.success("Data Saved")
                    if selected == 'UPDATE':
                        date = st.date_input("Select date to update data")
                        if date is not None:
                            df = pd.read_sql_query(f"""Select * from 'PRODUCTIVITY AND OEE' where date = "{date}" """,conn)
                            edited_df = st.data_editor(df, width=1600)
                            update = st.button("Data Update")
                            if update:
                                try:
                                    for _, row in edited_df.iterrows():
                                        cur.execute(
                                            f'UPDATE COST SET CATEGORY = "{row["CATEGORY"]}", TARGET = "{row["TARGET"]}", ACTUAL = "{row["ACTUAL"]}" WHERE TIME_STAMP = "{row["TIME_STAMP"]}" '
                                        )
                                        conn.commit()
                                    st.success("Data Updated")
                                except Exception as e:
                                    st.write(e)
                            time_stamp = st.text_input("Enter the time stamp to delete")
                            button = st.button("Delete Entery")
                            if button:
                                cur.execute(f"DELETE FROM 'PRODUCTIVITY AND OEE' WHERE Time_Stamp = '{time_stamp}' ")
                                conn.commit()
                                st.success("Success")
                                st.rerun()
                        st.write("update")
                if slct == "OEE_ISSUE":
                    option = ["", "UPDATE", 'LOG']
                    selected = st.selectbox("OEE_ISSUE", options=option, index=0)
                    # ACTIONS ACCORDING TO OPTIONS
                    if selected == 'LOG':
                        no_event = st.number_input("Enter number of events to log", step=1)
                        if no_event > 0:
                            with st.form("cost"):
                                date = st.date_input("Date")
                                col1, col2, col3, col4, col5, col6 = st.columns((1, 1, 1, 1, 1, 1))
                                for i in range(0, no_event):
                                    with col1:
                                        st.selectbox("Category", options=['','HUMAN PRODUCTIVITY', 'PLANT AGGREGATE OEE'], key=f"category{i}")
                                    with col2:
                                        st.text_input("Issue", key=f"issue{i}")
                                    with col3:
                                        st.text_input("Responsibility", key=f"responsibility{i}")
                                    with col4:
                                        st.date_input("Target_date", key=f"target_date{i}")
                                    with col5:
                                        st.text_input("Action", key=f"action{i}")
                                    with col6:
                                        st.selectbox("Status", options=['','Open', 'Closed', 'Inprocess'], key=f"status{i}")
                                submit = st.form_submit_button("Save")
                                if submit:
                                    for i in range(0, no_event):
                                        cur.execute(
                                            f"""INSERT INTO 'COST ISSUE' VALUES ("{datetime.now()}","{date}","{st.session_state[f'category{i}']}","{st.session_state[f'issue{i}']}","{date}","{st.session_state[f'target_date{i}']}","{st.session_state[f'responsibility{i}']}","{st.session_state[f'action{i}']}","{st.session_state[f'status{i}']}")"""
                                        )
                                    st.success("Data Saved")
                    if selected == 'UPDATE':
                        date = st.date_input("Select date to update data")
                        if date is not None:
                            df = pd.read_sql_query(f"""Select * from 'COST ISSUE' where date = "{date}" """,conn)
                            edited_df = st.data_editor(df, width=1600)
                            update = st.button("Data Update")
                            if update:
                                try:
                                    for _, row in edited_df.iterrows():
                                        cur.execute(
                                            f'UPDATE "COST ISSUE" SET CATEGORY = "{row["CATEGORY"]}","RAISE DATE" = "{row["RAISE DATE"]}","TARGET DATE" = "{row["TARGET DATE"]}","RESPONSIBILITY" = "{row["RESPONSIBILITY"]}","ACTION" = "{row["ACTION"]}","STATUS" = "{row["STATUS"]}" WHERE TIME_STAMP = "{row["TIME_STAMP"]}" '
                                        )
                                        conn.commit()
                                    st.success("Data Updated")
                                except Exception as e:
                                    st.write(e)
                            time_stamp = st.text_input("Enter the time stamp to delete")
                            button = st.button("Delete Entery")
                            if button:
                                cur.execute(f"DELETE FROM 'COST ISSUE' WHERE Time_Stamp = '{time_stamp}' ")
                                conn.commit()
                                st.success("Success")
                                st.rerun()
                        st.write("update")
                    
        if slct == 'RAW Metarial PDI':
            with sqlite3.connect('database/cost.db') as conn:
                cur = conn.cursor()
                option = ["", "UPDATE", 'LOG']
                selected = st.selectbox("RAW Metarial PDI", options=option, index=0)
                # ACTIONS ACCORDING TO OPTIONS
                if selected == 'LOG':
                    no_event = st.number_input("Enter number of events to log", step=1)
                    if no_event > 0:
                        with st.form("cost"):
                            date = st.date_input("Date")
                            col1, col2, col3, col4, col5, col6 = st.columns((1, 1, 1, 1, 1, 1))
                            for i in range(0, no_event):
                                with col1:
                                    st.selectbox("Category", options=['','A', 'B', 'C'], key=f"category{i}")
                                with col2:
                                    st.text_input("Part No", key=f"part_no{i}")
                                with col3:
                                    st.number_input("Value MINR", key=f"value_minr{i}")
                                with col4:
                                    st.number_input("Actual Value MINR", key=f"actual_value_minr{i}")
                                with col5:
                                    st.text_input("PDI", key=f"pdi{i}")
                                with col6:
                                    st.multiselect("Select Issues", options=['issue1','issue2','issue3','issue4'], key=f"issue{i}")
                            submit = st.form_submit_button("Save")
                            if submit:
                                for i in range(0, no_event):
                                    cur.execute(
                                        f"""INSERT INTO 'RAW MATERIAL PDI' VALUES ("{datetime.now()}","{date}","{st.session_state[f'category{i}']}","{st.session_state[f'part_no{i}']}","{st.session_state[f'value_minr{i}']}","{st.session_state[f'actual_value_minr{i}']}","{st.session_state[f'pdi{i}']}","{st.session_state[f'issue{i}']}")"""
                                    )
                                st.success("Data Saved")
                if selected == 'UPDATE':
                    date = st.date_input("Select date to update data")
                    if date is not None:
                        df = pd.read_sql_query(f"""Select * from 'RAW MATERIAL PDI' where date = "{date}" """,conn)
                        edited_df = st.data_editor(df, width=1600)
                        update = st.button("Data Update")
                        if update:
                            try:
                                for _, row in edited_df.iterrows():
                                    cur.execute(
                                        f'UPDATE COST SET CATEGORY = "{row["CATEGORY"]}", PART NO = "{row["PART NO"]}", VALUE_MINR = "{row["VALUE_MINR"]}", ACTUAL VALUE_MINR = "{row["ACTUAL VALUE_MINR"]}", PDI = "{row["PDI"]}", ISSUES = "{row["ISSUES"]}" WHERE TIME_STAMP = "{row["TIME_STAMP"]}" '
                                    )
                                    conn.commit()
                                st.success("Data Updated")
                            except Exception as e:
                                st.write(e)
                        time_stamp = st.text_input("Enter the time stamp to delete")
                        button = st.button("Delete Entery")
                        if button:
                            cur.execute(f"DELETE FROM 'RAW MATERIAL PDI' WHERE Time_Stamp = '{time_stamp}' ")
                            conn.commit()
                            st.success("Success")
                            st.rerun()
                    st.write("update")
                    
        if slct == 'Machine Breakdown Time':
            with sqlite3.connect('database/main_database.db') as conn:
                cur = conn.cursor()
                option = ["", "UPDATE", 'LOG']
                selected = st.selectbox("Machine Breakdown Time", options=option, index=0)
                # ACTIONS ACCORDING TO OPTIONS
                if selected == 'LOG':
                    no_event = st.number_input("Enter number of events to log", step=1)
                    if no_event > 0:
                        with st.form("cost"):
                            date = st.date_input("Date")
                            col1, col2, col3, col4, col5, col6, col7 = st.columns((1, 1, 1, 1, 1, 1, 1))
                            for i in range(0, no_event):
                                with col1:
                                    st.text_input("Line", key=f"line{i}")
                                with col2:
                                    st.text_input("Machine", key=f"machine{i}")
                                with col3:
                                    st.time_input("B/D Time", key=f"b/d_time{i}")
                                with col4:
                                    st.multiselect("Select Issues", options=['issue1','issue2','issue3','issue4'], key=f"issue{i}")
                                with col5:
                                    st.text_input("Action", key=f"action{i}")
                                with col6:
                                    st.selectbox("Status", options=['','Open', 'Closed', 'Inprocess'], key=f"status{i}")
                                with col7:
                                    st.text_input("Delivery Failure", key=f"delivery_failure{i}")

                            submit = st.form_submit_button("Save")
                            if submit:
                                for i in range(0, no_event):
                                    cur.execute(
                                        f"""INSERT INTO 'MACHINE BREAKDOWN TIME' VALUES ("{datetime.now()}","{date}","{st.session_state[f'line{i}']}","{st.session_state[f'machine{i}']}","{st.session_state[f'b/d_time{i}']}","{st.session_state[f'issue{i}']}","{st.session_state[f'action{i}']}","{st.session_state[f'status{i}']}","{st.session_state[f'delivery_failure{i}']}")"""
                                    )
                                st.success("Data Saved")
                if selected == 'UPDATE':
                    date = st.date_input("Select date to update data")
                    if date is not None:
                        df = pd.read_sql_query(f"""Select * from 'MACHINE BREAKDOWN TIME' where date = "{date}" """,conn)
                        edited_df = st.data_editor(df, width=1600)
                        update = st.button("Data Update")
                        if update:
                            try:
                                for _, row in edited_df.iterrows():
                                    cur.execute(
                                        f'UPDATE "MACHINE BREAKDOWN TIME" SET LINE = "{row["LINE"]}", MACHINE = "{row["MACHINE"]}", B/D TIME = "{row["B/D TIME"]}", ISSUE = "{row["ISSUE"]}", ACTION = "{row["ACTION"]}", STATUS = "{row["STATUS"]}", DELIVERY FAILURE = "{row["DELIVERY FAILURE"]}" WHERE TIME_STAMP = "{row["TIME_STAMP"]}" '
                                    )
                                    conn.commit()
                                st.success("Data Updated")
                            except Exception as e:
                                st.write(e)
                        time_stamp = st.text_input("Enter the time stamp to delete")
                        button = st.button("Delete Entery")
                        if button:
                            cur.execute(f"DELETE FROM 'MACHINE BREAKDOWN TIME' WHERE Time_Stamp = '{time_stamp}' ")
                            conn.commit()
                            st.success("Success")
                            st.rerun()
                    st.write("update")

    if selected == '':
        annotated_text(("Welcome to Database Manager , You can Update the database here !!!", "", "green"))

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')