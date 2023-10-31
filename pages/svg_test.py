import streamlit as st
from xml.etree import ElementTree as ET
from methods.main import fetch_data
import base64
import datetime
import pandas as pd
import numpy as np

# Parse the existing SVG file
tree = ET.parse('resources\C.svg')
root = tree.getroot()

on_date = st.date_input(":green[Select Date:]")
current_date = datetime.date.today()
# days_in_current_month = calendar.monthrange(current_year, current_month)[1]   #for check total days in current month
total_days = (current_date.day)
# st.write(total_days)

row_data = fetch_data("PRODUCTIVITY AND OEE")
first_day_of_month = current_date.replace(day=1)
days_to_add = 0
for i in range(1, total_days):
    if i < 10:
        target_element = root.find(f".//*[@id='untitled-u-day{i}']")
    else:
        target_element = root.find(f".//*[@id='untitled-u-day{i}_']")
    # st.write(days_to_add)
    new_date = first_day_of_month + datetime.timedelta(days=days_to_add)
    days_to_add += 1
    df = row_data[row_data["DATE"] == f"{new_date}"]
    filter_data = df[df["CATEGORY"] == "HUMAN PRODUCTIVITY"]
    oe_target = filter_data["TARGET"]
    oe_actual = filter_data["ACTUAL"]
    comparison = np.where(oe_target > oe_actual, 'red', 'green')

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
    if new_date.weekday() == 6: target_element.set('fill', "blue")
    else:
        for result in comparison:
            # st.write(result)
            color = result
            target_element.set('fill', color)
        tree.write('output.svg')

# Display the modified SVG using Streamlit
with open('output.svg', 'r') as f:
    svg = f.read()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s" style="height:15rem;"/>' % b64
    st.write(f"""<div>{html}</div>""", unsafe_allow_html=True)




# st.markdown(f"""
#     <style>
#         /* Define your custom CSS styles here */
#         .svg-container {{
#             max-width: 100%; /* Ensure the container is responsive */
#             overflow: hidden; /* Hide the overflowing content */
#         }}
#     </style>
#     <center><div> 
#         <svg class="svg-container" height="150" width="450">
#             <text x="20" y="130" font-size="10rem" font-weight="bold" font-family="Arial" fill={color}>S</text>
#             <text x="220" y="30" font-size="0.65rem" font-weight="bold" fill="black">LEGEND:</text>
#             <text x="220" y="50" font-size="0.65rem" font-weight="bold" fill="red">RECORDABLE LOST TIME ENJURY</text>
#             <text x="220" y="70" font-size="0.65rem" font-weight="bold" fill="darkred">RECORDABLE ACCIDENT</text>
#             <text x="220" y="90" font-size="0.65rem" font-weight="bold" fill="orange">FIRST AID</text>
#             <text x="220" y="110" font-size="0.65rem" font-weight="bold" fill="yellow">NEAR MISS</text>
#             <text x="220" y="130" font-size="0.65rem" font-weight="bold" fill="blue">FIRE</text>
#             <text x="220" y="150" font-size="0.65rem" font-weight="bold" fill="green">NO INCIDENT</text>
#         </svg>
#     </div></center>
#     """, unsafe_allow_html=True)
# letter_color = 'green'

# st.markdown(f"""
            #     <style>
            #         .container {{
            #             width: 200px;
            #             height: 16.3rem;
            #             position: relative;
            #         }}
            #         .block {{
            #             background-color: blue;
            #             width:1.2rem;
            #         }}
            #         .block1{{ position: relative; left: 15rem; background-color: {letter_color};}}
            #         .block2{{ position: relative; left: 13.75rem; bottom: 1.6rem;}}
            #         .block3{{ position: relative; left: 12.5rem; bottom: 3.2rem;}}
            #         .block4{{ position: relative; left: 11.27rem; bottom: 4.8rem;}}
            #         .block5{{ position: relative; left: 10.1rem; bottom: 6.4rem;}}
            #         .block6{{ position: relative; left: 8.895rem; bottom: 8rem;}}
            #         .block7{{ position: relative; left: 7.7rem; bottom: 9.6rem;}}
            #         .block8{{ position: relative; left: 7.7rem; bottom: 9.6rem;}}
            #         .block9{{ position: relative; left: 7.7rem; bottom: 9.6rem;}}
            #         .block10{{ position: relative; left: 7.7rem; bottom: 9.6rem;}}
            #         .block11{{ position: relative; left: 7.7rem; bottom: 9.6rem;}}
            #         .block12{{ position: relative; left: 7.7rem; bottom: 9.6rem}}
            #         .block13{{ position: relative; left: 8.9rem; bottom: 11.18rem;}}
            #         .block14{{ position: relative; left: 10.1rem; bottom: 12.8rem;}}
            #         .block15{{ position: relative; left: 11.3rem; bottom: 14.4rem;}}
            #         .block16{{ position: relative; left: 12.5rem; bottom: 15.98rem;}}
            #         .block17{{ position: relative; left: 13.65rem; bottom: 17.58rem;}}
            #         .block18{{ position: relative; left: 14.85rem; bottom: 19.18rem;}}
            #         .block19{{ position: relative; left: 14.85rem; bottom: 19.2rem;}}
            #         .block20{{ position: relative; left: 14.85rem; bottom: 19.2rem;}}
            #         .block21{{ position: relative; left: 14.85rem; bottom: 19.2rem;}}
            #         .block22{{ position: relative; left: 14.85rem; bottom: 19.2rem;}}
            #         .block23{{ position: relative; left: 14.85rem; bottom: 19.2rem;}}
            #         .block24{{ position: relative; left: 13.65rem; bottom: 20.8rem;}}
            #         .block25{{ position: relative; left: 12.42rem; bottom: 22.4rem;}}
            #         .block26{{ position: relative; left: 11.25rem; bottom: 24rem;}}
            #         .block27{{ position: relative; left: 10.02rem; bottom: 25.6rem;}}
            #         .block28{{ position: relative; left: 8.85rem; bottom: 27.2rem;}}
            #         .block29{{ position: relative; left: 7.64rem; bottom: 28.8rem;}}
            #         .block30{{ position: relative; left: 7.6rem; bottom: 32rem;}}
            #     </style>
            #     <div class="container">
            #         <div class="block block1" id="block1">1</div>
            #         <div class="block block2">2</div>
            #         <div class="block block3">3</div>
            #         <div class="block block4">4</div>
            #         <div class="block block5">5</div>
            #         <div class="block block6">6</div>
            #         <div class="block block7">7</div>
            #         <div class="block block8">8</div>
            #         <div class="block block9">9</div>
            #         <div class="block block10">10</div>
            #         <div class="block block11">11</div>
            #         <div class="block block12">12</div>
            #         <div class="block block13">13</div>
            #         <div class="block block14">14</div>
            #         <div class="block block15">15</div>
            #         <div class="block block16">16</div>
            #         <div class="block block17">17</div>
            #         <div class="block block18">18</div>
            #         <div class="block block19">19</div>
            #         <div class="block block20">20</div>
            #         <div class="block block21">21</div>
            #         <div class="block block22">22</div>
            #         <div class="block block23">23</div>
            #         <div class="block block24">24</div>
            #         <div class="block block25">25</div>
            #         <div class="block block26">26</div>
            #         <div class="block block27">27</div>
            #         <div class="block block28">28</div>
            #         <div class="block block29">29</div>
            #         <div class="block block30">30</div>
            #     </div>
            # """,unsafe_allow_html=True)