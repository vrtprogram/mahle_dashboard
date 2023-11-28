import streamlit as st
from methods.main import layout, fetch_data, data_filter_between,fetch_month_data
from datetime import date
from datetime import datetime as dt
from datetime import datetime, timedelta
import sqlite3
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
from xml.etree import ElementTree as ET
import base64
from streamlit.components.v1 import html
import time

layout("this page only for testing")


def main():

    with sqlite3.connect("database/main_database.db") as conn:
        # query = f"SELECT * FROM \"{table_name}\";"
        # dataframe = pd.read_sql_query(query, conn)
        cur = conn.cursor()
        cur.execute(f"DELETE FROM 'PLANT PPM & SUPPLIER PPM' WHERE DATE <= 2023-11-24 00:00:00")
        # dataframe['DATE'] = pd.to_datetime(dataframe['DATE'])
        # current_year = pd.Timestamp('now').to_period('Y')
        # # current_month = pd.Timestamp('now').to_period('M')
        # dataframe = dataframe[((dataframe['DATE'].dt.to_period('Y')) == current_year)]
        # dataframe['DATE'] = dataframe['DATE'].dt.strftime('%Y-%m-%d')

    # st.subheader("Get Specipic Data!")
    # my_data = 0
    # c1,c2,c3 = st.columns((1,1,1))
    # with c1:
    #     starting_date = st.date_input("Select Start Date")
    # with c2:
    #     end_date = st.date_input("Select End Date")
    # with c3:
    #     category = st.selectbox("Category", options=[' ','INCIDENCES DETAILS', 'UNSAFE PRACTICES TRACKING', 'PRODUCTIVITY AND OEE', 'MACHINE BREAKDOWN TIME', 'OTIF_CC PDI'])
    # if category == ' ':
    #     pass
    # else:
    #     my_data = data_filter_between(category, starting_date, end_date)
    # if not my_data.empty:
    #     st.table(my_data)
    # else:
    #     pass

    # df = fetch_data("UNSAFE PRACTICES TRACKING")
    # df['DATE'] = pd.to_datetime(df['DATE'])
    # current_month = pd.Timestamp('now').to_period('M')
    # month_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    # target_data = fetch_data("SET DAILY TARGET")
    # target_data = target_data[target_data["CATEGORY"] == 'Incident Practices']  #filter data acording category
    # monthly_target = target_data[((target_data["DATE"].dt.to_period("M")) == current_month)]
    # st.subheader("FTP Trend")
    today_date = datetime.now()
    # current_week_number = today_date.strftime('%U') #check current week number
    # cl1,cl2,cl3 = st.columns((1,1,1))
    # with cl1:   # ****** Daily_Data ****** #
    #     desired_data = month_data[month_data['DATE'].dt.strftime('%U') == current_week_number]
    #     daily_data_count = desired_data.groupby(desired_data['DATE'].dt.to_period('D')).size().reset_index(name='data')
    #     desired_data['Day'] = desired_data['DATE'].dt.strftime('%a')  # Day format in weekdays
    #     unique_desired_data = desired_data.drop_duplicates(subset='Day', keep='first')
    #     desired_trgt = monthly_target[monthly_target['DATE'].dt.strftime('%U') == current_week_number]
    #     desired_trgt['DATE'] = desired_trgt['DATE'].dt.strftime("%Y-%m-%d")
    #     daily_data_count['DATE'] = daily_data_count['DATE'].dt.strftime("%Y-%m-%d") # Convert 'DATE' to a string in both DataFrames for merging
    #     merged_data = pd.merge(daily_data_count, desired_trgt, on='DATE')  # Merge on the 'DATE' column
    #     merged_data['color'] = np.where(merged_data['data'] >= merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
    #     fig = go.Figure()
    #     # Add a trace for each target value
    #     for day, actual_value, my_color in zip(unique_desired_data['Day'], merged_data['data'], merged_data['color']):
    #         fig.add_trace(go.Scatter(x=[day, day], y=[0, actual_value], mode='lines', name='count', line=dict(color=my_color, width=30), showlegend=False))
    #     # Plotting the line chart using Plotly Express
    #     fig.add_trace(go.Scatter(x=unique_desired_data['Day'], y=merged_data['VALUE'], line=dict(color='black', width=1), mode='lines+markers', name='Target'))
    #     # Update layout
    #     fig.update_layout(title='Daily Trend', xaxis_title='Day', yaxis_title='Actual')
    #     st.plotly_chart(fig, use_container_width=True)
    # with cl2:   # ****** Weekly_Data ****** #
    #     weekly_data = month_data.groupby(month_data['DATE'].dt.to_period('W')).size()
    #     weekly_trgt = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum()
    #     weekly_data = pd.DataFrame({'my_data': weekly_data})
    #     merged_data = pd.merge(weekly_data, weekly_trgt, on='DATE')   #Merge actual and target data in single table
    #     merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
    #     weekly_data.index = weekly_data.index.astype(str)
    #     weekly_data['WEEKLY_NUMBER'] = range(1, len(weekly_data) +1)
    #     fig = go.Figure(data=[
    #         go.Bar(
    #             x=list(weekly_data['WEEKLY_NUMBER']),  # Convert range to list
    #             y=merged_data['my_data'],
    #             marker_color=[color for color in merged_data['color']],
    #         ),
    #     ])
    #     fig.update_layout(
    #         xaxis_title='Week',
    #         yaxis_title='Total Actual',
    #         title="Weekly Trend",
    #     )
    #     st.plotly_chart(fig, use_container_width=True)
    # with cl3:   # ****** Monthly_Data ****** #
    #     monthly_data = df.groupby(df['DATE'].dt.to_period('M')).size()
    #     monthly_target = target_data.groupby(target_data['DATE'].dt.to_period('M'))['VALUE'].sum()
    #     monthly_data = pd.DataFrame({'my_data': monthly_data})
    #     merged_data = pd.merge(monthly_data, monthly_target, on='DATE')   #Merge actual and target data in single table
    #     merged_data['color'] = np.where(merged_data['my_data'] > merged_data['VALUE'], "#fa2323", "#5fe650")   #Compare data and add color in table acordingly
    #     monthly_data.index = monthly_data.index.strftime('%b')
    #     fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=merged_data['my_data'], marker_color=[color for color in merged_data['color']],)])
    #     # Customize the chart layout
    #     fig.update_layout(
    #         xaxis_title='Month',
    #         yaxis_title='Total Actual',
    #         title="Monthly Trend",
    #     )
    #     st.plotly_chart(fig, use_container_width=True)
    #     pass

    completion_date = today_date - timedelta(days=today_date.timetuple().tm_yday)
    st.write(completion_date)

    # Initialize messages list in session_state
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []
    # # Function to add a message to the chat history
    # def add_message(sender, message, timestamp):
    #     st.session_state.messages.append({"sender": sender, "message": message, "timestamp": timestamp})
    # # Function to display the chat history
    # def display_chat_history():
    #     for msg in st.session_state.messages:
    #         st.write(f"{msg['timestamp']} - {msg['sender']}: {msg['message']}")
    # st.title("Simple Chat App")
    # message_input = st.chat_input("Your Message:", key="message_input")
    # if message_input:
    #     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     add_message("You", message_input, current_time)
    # # Display chat history
    # st.header("Chat History")
    # display_chat_history()


    # my_html = """
    # <script>
    #     function startTimer(duration, display) {
    #         var timer = duration, minutes, seconds;
    #         setInterval(function () {
    #             minutes = parseInt(timer / 60, 10)
    #             seconds = parseInt(timer % 60, 10);
    #             minutes = minutes < 10 ? "0" + minutes : minutes;
    #             seconds = seconds < 10 ? "0" + seconds : seconds;
    #             display.textContent = minutes + ":" + seconds;
    #             if (--timer < 0) {
    #                 timer = duration;
    #             }
    #         }, 1000);
    #     }
    #     window.onload = function () {
    #         var fiveMinutes = 60 * 5,
    #             display = document.querySelector('#time');
    #         startTimer(fiveMinutes, display);
    #     };
    # </script>
    # <body>
    #     <div>Registration closes in <span id="time">05:00</span> minutes!</div>
    # </body>
    # """
    # html(my_html)
    # if st.button("Is blocked?"):
    #     st.write("No, you can still interact")
    #     st.balloons()


    # df = fetch_data("PERSONAL GAP")
    # df['DATE'] = pd.to_datetime(df['DATE'])
    # current_month = pd.Timestamp('now').to_period('M')
    # df = df.iloc[-1]
    # a = 3
    # st.write(a+df['ACTUAL MANPOWER'])
    # pg_data = df[((df['DATE'].dt.to_period('M')) == current_month)]
    # pg_target = fetch_data("SET DAILY TARGET")
    # pg_target = pg_target[pg_target["CATEGORY"] == 'Personal Gap']
    # monthly_target = pg_target[((pg_target["DATE"].dt.to_period("M")) == current_month)]
    # today_date = datetime.now()
    # current_week_number = today_date.strftime('%U')
    # cl1,cl2,cl3 = st.columns((1,1,1))
    # with cl1:   # ****** Daily_Data ****** #
    #     st.markdown("")
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:0.7rem 0rem;'>Daily Trend</center>""",unsafe_allow_html=True)
    #     desired_data = pg_data[pg_data['DATE'].dt.strftime('%U') == current_week_number]
    #     daily_data = desired_data.groupby(desired_data['DATE'].dt.to_period('D'))['PERSONAL GAP'].sum()
    #     daily_data.index = daily_data.index.strftime('%b %d')
    #     daily_color = []
    #     for i in daily_data.index:
    #         # Format the date in the same way as the monthly_target data for comparison
    #         formatted_date = datetime.strptime(i, '%b %d').strftime('%b %d')
    #         # Find the corresponding row in monthly_target with the same formatted date
    #         matching_target = monthly_target[monthly_target['DATE'].dt.strftime('%b %d') == formatted_date]
            
    #         if not matching_target.empty:
    #             target_value = matching_target["VALUE"].values[0]
    #             # print(daily_data[i], target_value)
    #             if daily_data[i] > target_value:
    #                 daily_color.append("#fa2323")  # Complaints exceed target
    #             else:
    #                 daily_color.append("#5fe650")  # Complaints meet or are below target
    #         else:
    #             daily_color.append("#5fe650")
                
    #     fig = go.Figure(data=[go.Bar(x=daily_data.index, y=daily_data, marker_color=daily_color)])
    #     # Customize the chart layout
    #     fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Days', yaxis_title='Personal Gap')
    #     # Display the chart in Streamlit
    #     st.plotly_chart(fig)

    # with cl2:   # ****** Weekly_Data ****** #
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Weekly Trend</center>""",unsafe_allow_html=True)
    #     weekly_data = pg_data.groupby(pg_data['DATE'].dt.to_period('W'))[['ACTUAL MANPOWER', 'PLANNED MANPOWER']].sum()
    #     weekly_data['NEW_PG'] = round(((weekly_data['PLANNED MANPOWER'] - weekly_data['ACTUAL MANPOWER'])/weekly_data['PLANNED MANPOWER'])*100, 2)
    #     # st.write(weekly_data['NEW_PG'])
    #     weekly_target = monthly_target.groupby(monthly_target['DATE'].dt.to_period('W'))['VALUE'].sum()
    #     weekly_data.index = range(1, len(weekly_data) + 1)
    #     weekly_color = []
    #     for i in weekly_data.index:
    #         target_value = weekly_target.get(i, 0)
    #         data_value = weekly_data.loc[i, 'NEW_PG']
    #         if data_value > target_value:
    #             weekly_color.append("#fa2323")  # Data exceed target
    #         else:
    #             weekly_color.append("#5fe650")  # Data meet or are below target
    #     fig = go.Figure(data=[go.Bar(x=weekly_data.index, y=weekly_data['NEW_PG'], marker_color=weekly_color)])
    #     # Customize the chart layout
    #     fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Weeks', yaxis_title='Personal Gap')
    #     # Display the chart in Streamlit
    #     st.plotly_chart(fig)

    # with cl3:   # ****** Monthly_Data ****** #
    #     st.markdown("""<center style='font-weight:bold; font-size:1.3rem; text-decoration: underline; padding:1.2rem 0rem;'>Monthly Trend</center>""",unsafe_allow_html=True)
    #     monthly_data = df.groupby(df['DATE'].dt.to_period('M'))[['ACTUAL MANPOWER', 'PLANNED MANPOWER']].sum()
    #     monthly_target = pg_target.groupby(pg_target['DATE'].dt.to_period('M'))['VALUE'].sum()
    #     monthly_data['NEW_PG'] = round(((monthly_data['PLANNED MANPOWER'] - monthly_data['ACTUAL MANPOWER'])/monthly_data['PLANNED MANPOWER'])*100, 2)
    #     monthly_data.index = monthly_data.index.strftime('%b')
    #     monthly_color = []
    #     for i in monthly_data.index:
    #         target_value = monthly_target.get(i, 0)
    #         data_value = monthly_data.loc[i, 'NEW_PG']
    #         if data_value > target_value:
    #             monthly_color.append("#fa2323")  # Data exceed target
    #         else:
    #             monthly_color.append("#5fe650")  # Data meet or are below target
    #     fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=monthly_data['NEW_PG'], marker_color=monthly_color)])
    #     # Customize the chart layout
    #     fig.update_layout(height=387, width=430, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor='white', paper_bgcolor='lightgray', xaxis=dict(tickfont=dict(color='black')), yaxis=dict(tickfont=dict(color='black')), xaxis_title='Months', yaxis_title='Personal Gap')
    #     # Display the chart in Streamlit
    #     st.plotly_chart(fig)


    

    data = {
        "DATE": pd.date_range(start="2023-11-01", periods=56, freq="D"),
        "TARGET": [80, 80, 80, 80, 80, 80, 80] * 8,
        "ACTUAL": [78, 82, 76, 85, 79, 81, 77] * 8,
    }

    # Convert data to DataFrame
    hp_data = pd.DataFrame(data)

    # Define a function to create a bar chart
    def create_bar_chart(data, title):
        # Calculate the color based on the comparison between ACTUAL and TARGET
        data['COLOR'] = np.where(data['ACTUAL'] >= data['TARGET'], 'green', 'red')
        
        # Create a bar chart using Plotly Graph Objects with explicitly defined colors
        colors = {'green': '#008000', 'red': '#FF0000'}

        fig = go.Figure(data=[
            go.Bar(
                x=data['DATE'],
                y=data['ACTUAL'],
                marker_color=[colors[color] for color in data['COLOR']],
            ),
        ])

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Actual',
            title=title,
        )

        st.plotly_chart(fig)

    # st.subheader("Weekly Trend - Plant PPM")
    weekly_data = hp_data.resample('W-MON', on='DATE').agg({'DATE': 'first', 'TARGET': 'mean', 'ACTUAL': 'mean'}).reset_index(drop=True)
    weekly_data = weekly_data.dropna()  # Remove rows with NaN values
    create_bar_chart(weekly_data, "Weekly Trend - Plant PPM")

    st.subheader("Monthly Trend - Plant PPM")
    monthly_data = hp_data.resample('M', on='DATE').agg({'DATE': 'first', 'TARGET': 'mean', 'ACTUAL': 'mean'}).reset_index(drop=True)
    monthly_data = monthly_data.dropna()  # Remove rows with NaN values
    create_bar_chart(monthly_data, "Monthly Trend - Plant PPM")



    with sqlite3.connect("database/main_database.db") as con:
        query = f"SELECT * from 'OTIF_CC PDI'"
        df = pd.read_sql_query(query, con)
        oe = df[(df["CATEGORY"] == "OE") & (df["ACTUAL"] < df["TARGET"])]
        # st.write(oe)
        if not oe.empty:
            # Get the most recent event date
            last_event_date = oe["DATE"].max()
            # Calculate the number of days since the last event
            last_event_date = datetime.strptime(last_event_date, "%Y-%m-%d")
            today = datetime.today()
            days_since_last_event = (today - last_event_date).days
            st.write(f"Days since the last 'Recordable Loss Time Injury' event: {days_since_last_event}")
        else:
            st.write("No 'Recordable Loss Time Injury' events found in the database.")
    

    # tree = ET.parse("C:/Users/admin/Downloads/S.svg")
    # root = tree.getroot()
    # on_date = st.date_input(":green[Select Date:]")
    # current_date = datetime.date.today()
    # days_in_current_month = calendar.monthrange(current_year, current_month)[1]   #for check total days in current month
    # total_days = (current_date.day)
    # st.write(total_days)

    # row_data = fetch_data("PRODUCTIVITY AND OEE")
    # first_day_of_month = current_date.replace(day=1)
    # days_to_add = 0
    # for i in range(1, 32):
    #     if i < 10:
    #         target_element = root.find(f".//*[@id='untitled-u-day{i}']")
    #     else:
    #         target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
        # st.write(days_to_add)
        # new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
        # days_to_add += 1
        # df = row_data[row_data["DATE"] == f"{new_date}"]
        # filter_data = df[df["CATEGORY"] == "HUMAN PRODUCTIVITY"]
        # oe_target = filter_data["TARGET"]
        # oe_actual = filter_data["ACTUAL"]
        # comparison = np.where(oe_target > oe_actual, 'red', 'green')

        # for result in comparison:
        #     st.write(result)

        # if new_date.weekday() == 6: color = "blue"
        # else:
        #     if oe_target > oe_actual: color = 'red'
        #     elif oe_actual >= oe_target: color = 'green'
        # if target_element is not None:
        #     target_element.set('fill', 'gray')
        # else:
        #     print(f"Element not found for i={i}")
        # if new_date.weekday() == 6: target_element.set('fill', "blue")
        # else:
        #     for result in comparison:
                # st.write(result)
                # color = result
    #     target_element.set('fill', 'gray')
    #     tree.write('output.svg')

    # # Display the modified SVG using Streamlit
    # with open('output.svg', 'r') as f:
    #     svg = f.read()
    #     b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    #     html = r'<img src="data:image/svg+xml;base64,%s" style="height:15rem;"/>' % b64
    #     st.write(f"""<div>{html}</div>""", unsafe_allow_html=True)


    # on_date = st.date_input("select date")
    # ppm_graph = fetch_data("PLANT PPM & SUPPLIER PPM")
    # today_data = ppm_graph[ppm_graph["DATE"] == f"{on_date}"]
    # for index, row in ppm_graph.iterrows():
    #     if row["CATEGORY"] == "PLANT PPM":
    #         plant_target = row["TARGET"]
    #         plant_actual = row["ACTUAL"]
    # color = 'red' if plant_target > plant_actual else 'green'
    # today_data['DATE'] = pd.to_datetime(today_data['DATE'])
    # # Format the 'DATE' column to display only the date portion
    # today_data['DATE'] = today_data['DATE'].dt.strftime('%b %d')
    # fig = px.bar(today_data, x='DATE', y=['ACTUAL', 'TARGET'])
    # fig.update_layout(title='Plant Target vs. Plant Actual', xaxis_title='DATE', yaxis_title='VALUE')
    # st.plotly_chart(fig)
    # st.bar_chart(ppm_graph, x='DATE', y=['ACTUAL', 'TARGET'], color=['#a6f59a', '#f7a392'])
    
    # year = datetime.now().year
    # strt_date = f"{year}-01-01"
    # end_date = f"{year}-12-31"
    # row_data = data_filter_between("INCIDENCES DETAILS", strt_date, end_date)
    # st.table(row_data)
        
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

    # # Sample list of suggestions
    # suggestions = ["apple", "banana", "cherry", "grape", "kiwi", "orange", "pear", "pineapple", "strawberry"]
    # # Get user input
    # user_input = st.text_input("Enter a fruit:", "")
    # # Filter suggestions based on the user's input
    # filtered_suggestions = [suggestion for suggestion in suggestions if user_input.lower() in suggestion.lower()]
    # # Display the filtered suggestions
    # st.write("Suggestions:", filtered_suggestions)

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
