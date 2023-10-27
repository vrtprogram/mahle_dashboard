import streamlit as st
from methods.main import layout, fetch_data, bar_graph
from datetime import date
from datetime import datetime as dt
from datetime import datetime
import sqlite3
import plotly.graph_objects as go
import pandas as pd

layout("this page only for testing")

def main():

    # bar_graph("SALE PLAN VS ACTUAL")

    #sum data for month
    df = fetch_data("OTIF_CC PDI")
    df['DATE'] = pd.to_datetime(df['DATE']) # Convert the "DATE" column to datetime
    current_month = datetime.now().month    # Get the current month
    filtered_df = df[df['DATE'].dt.month == current_month]  # Filter the DataFrame for the current month
    total_value = filtered_df['ACTUAL'].sum()    # Sum all the values in the "Value" column
    st.write(f"total value is = {total_value}")

    # options=["No data", "comment"]
    # slct = st.selectbox("opt", options)
    # if slct == "comment":
    #     st.text_input("Issue", placeholder="write here")

    # target_values = [80, 83]
    # actual_values = [90, 92]
    # # Calculate daily percentages
    # daily_percentages = [(actual / target) * 100 for actual, target in zip(actual_values, target_values)]
    # # Sum of daily percentages
    # total_percentage = sum(daily_percentages)
    # # Calculate the average percentage
    # average_percentage = total_percentage / len(target_values)
    # print(f"Total Percentage: {total_percentage:.2f}%")
    # print(f"Average Percentage: {average_percentage:.2f}%")
    
    # ********** Letter colors **********
    # on_date = st.date_input(":green[Select Date:]")
    # if on_date.weekday() == 6: day = "Sunday"
    # else: day = "it's not sunday"
    # st.write(day)
    # st.color_picker("color")
    
    # complaint_data = fetch_data("CUSTOMER COMPLAINTS")
    # df = complaint_data.get_data()
    # df = df[df["DATE"] == "2023-10-18"]
    # def my_color(status):
    #     if status == 'Open':
    #         color = 'background-color: #FB2D30'
    #     elif status == 'Inprocess':
    #         color = 'background-color: #F3ED21'
    #     elif status == 'Closed':
    #         color = 'background-color: #78E866'
    #     # color = 'green' if target > actual else 'red'
    #     return f'{color}'
    # styled_df = df.style.applymap(my_color, subset=['STATUS'])
    # st.write(styled_df)

    # st.latex(r'''
    # a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    # \sum_{k=0}^{n-1} ar^k =
    # a \left(\frac{1-r^{n}}{1-r}\right)
    # ''')

    st.write("this is data")
    col1,col2,col3 = st.columns((1,1,3))
    with col1:
        x = st.button("Open status")
    with col2:
        y = st.button("Close status")
    with col3:
        z = st.button("clr screen")
    if x:
        st.write("this is open")
        # specific_data("INCIDENCES DETAILS", "STATUS", "Open")
        pass
    elif y:
        st.write("this is close")
        # specific_data("INCIDENCES DETAILS", "STATUS", "Closed")
        pass
    elif z:
        x = False
        y = False
    
    # ********** Get all tables from a database ************#
    with sqlite3.connect("database/safety.db") as conn:
        # Get a list of all table names in the database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        table_names = [table[0] for table in table_names]
        # Create a dictionary to store DataFrames for each table
        dataframes = {}
        # Fetch data from each table and store it in a DataFrame
        st.write(table_names)
        for table_name in table_names:
            query = f"SELECT * FROM \"{table_name}\";"
            dataframes[table_name] = pd.read_sql_query(query, conn)
            # st.write(table_name)
        # Close the database connection
    # x = [{1:"fffed", 2:"dshhsds"},{1:"fffed", 2:"dsds"}]
    # st.write(dataframes)
    # for table_name, df in dataframes.items():
    #     st.write(f"Data from table: {table_name}")
    #     st.dataframe(df)  # Use st.dataframe to display the DataFrame
    # st.table(dataframes["UNSAFE INCIDENCES"])
    trgt_table = "INCIDENCES DETAILS"
    spec_data = "Closed"
    if trgt_table in dataframes:
        st.write("table is available")
        df = dataframes[trgt_table]
        filter_data = df[df["STATUS"] == spec_data]
        st.dataframe(filter_data)

    # **********************
    # *** Get Data between two dates*** #
    # from_date = st.date_input("From:")
    # to_date = st.date_input("To:")
    # days = from_date - to_date
    # query = "SELECT SUM(Value) AS Total FROM UNSAFE_PRACTICE_TRACKING WHERE Date BETWEEN ? AND ?"
    # cursor.execute(query, (from_date, to_date))
    # Value_SD = cursor.fetchone()[0]
    # if st.button("Show"):
    #     st.write(f"Total value for {days} days: {Value_SD}")

    # **********************
    my_array = [12, 45, 6, 89, 34, 72, 98, 54, 182]
    max_value = max(my_array)
    print("Maximum value in the array:", max_value)

    # ***********************************
    # HTML template with JavaScript for dynamic color change
    value = 100
    value1 = 12
    colors = ['black', 'red', 'green', 'orange', 'magenta', 'darkblue']
    if value == 100:
        color = colors[2]
    elif value1 == 12:
        color = colors[1]
    st.markdown(f"""
    <svg height="250" width="250">
        <text id="colorChange" x="50" y="200" font-size="17rem" fill={color}>S</text>
    </svg>
    """, unsafe_allow_html=True)

    # ***************************
    option = st.selectbox(
    "",
    ("Email", "Home phone", "Mobile phone"),
    index=None,
    placeholder="Select contact method...",
    )
    st.write('You selected:', option)

    # *****************************
    with sqlite3.connect("database/safety.db") as conn:
        # Get a list of all table names in the database
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        table_names = [table[0] for table in table_names]
        # Create a dictionary to store DataFrames for each table
        dataframes = {}
        # Fetch data from each table and store it in a DataFrame
        for table_name in table_names:
            query = f"SELECT * FROM \"{table_name}\";"
            dataframes[table_name] = pd.read_sql_query(query, conn)
        pass
    
    # data_df = dataframes["UNSAFE PRACTICES TRACKING"]
    data_df = fetch_data("CUSTOMER COMPLAINTS")
    on_day = datetime.now().day
    data_df["DATE"] = pd.to_datetime(data_df["DATE"])
    data_df = data_df[data_df["DATE"].dt.day == on_day]
    data_df = data_df[["COMPLAINT", "RAISE DATE", "RESPONSIBILITY", "TARGET DATE", "STATUS"]]
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
    # styled_df = data_df.style.set_table_styles(styles)
    # st.data_editor(data_df, hide_index=True, )
    # st.table(styled_df)
    
    # **********************************
    if "mytsks" not in st.session_state:
        st.session_state.mytsks = []
    if "tskclk" not in st.session_state:
        st.session_state.tskclk = []
    if "chkarr" not in st.session_state:
        st.session_state.chkarr = []
    if "rerun" not in st.session_state:
        st.session_state.rerun = False
    def cmpltTask(task):
        idx = st.session_state.mytsks.index(task)
        st.session_state.chkarr[idx] = not st.session_state.chkarr[idx]
        st.session_state.rerun = True
    def listTasks():
        st.session_state.tskclk = []
        for i, task in enumerate(st.session_state.mytsks):
            st.session_state.tskclk.append(st.checkbox(task, value = st.session_state.chkarr[i], key = f'l{i}' + f'{dt.now():%d%m%Y%H%M%S%f}', on_change = cmpltTask, args=(task,), help ='Check to mark as completed'))
    if st.session_state.rerun == True:
        st.session_state.rerun = False
        st.experimental_rerun()
    else:
        tsk = st.text_input('Enter your tasks', value="", placeholder = 'Enter a task')
        if st.button('Add Task'):
            if tsk != "":
                st.session_state.mytsks.append(tsk)
                st.session_state.chkarr.append(False)
    listTasks()

    # *******************************
    x = st.multiselect("Select items", options=['test1', 'test2', 'test3', 'test4'])
    x = str(x)
    print(x)
    print(type(x))
    my_date = date(year=2023, month=10, day=10)
    formatted_time = my_date.ctime()
    print(formatted_time)
    st.write(formatted_time)
    
if __name__ == "__main__":
    main()