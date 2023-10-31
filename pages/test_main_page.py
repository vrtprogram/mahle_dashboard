import streamlit as st
import base64
import os
from streamlit_extras.switch_page_button import switch_page
from methods.main import layout, fetch_data
from xml.etree import ElementTree as ET


st.cache_data()

layout("Shopfloor Management")
st.markdown(
    "<br>", unsafe_allow_html=True
)

def main():
    col1, col2, col3 = st.columns((5, 0.5, 2))
    colors = ['black', 'red', 'green', 'orange', 'magenta', 'darkblue']
    # column for images
    with col1:
        col_img_A, col_img_B, col_img_C = st.columns((1, 0.1, 1))
        with col_img_A:
            color = colors[1]
            # color = "red"
            st.markdown("""<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Safety</div></center>""", unsafe_allow_html=True)
            st.markdown(f"""
                <style>
                    /* Define your custom CSS styles here */
                    .svg-container {{
                        max-width: 100%; /* Ensure the container is responsive */
                        overflow: hidden; /* Hide the overflowing content */
                    }}
                </style>
                <center><div> 
                    <svg class="svg-container" height="150" width="450">
                        <text x="20" y="130" font-size="10rem" font-weight="bold" font-family="Arial" fill={color}>S</text>
                        <text x="220" y="30" font-size="0.65rem" font-weight="bold" fill="black">LEGEND:</text>
                        <text x="220" y="50" font-size="0.65rem" font-weight="bold" fill="red">RECORDABLE LOST TIME ENJURY</text>
                        <text x="220" y="70" font-size="0.65rem" font-weight="bold" fill="darkred">RECORDABLE ACCIDENT</text>
                        <text x="220" y="90" font-size="0.65rem" font-weight="bold" fill="orange">FIRST AID</text>
                        <text x="220" y="110" font-size="0.65rem" font-weight="bold" fill="yellow">NEAR MISS</text>
                        <text x="220" y="130" font-size="0.65rem" font-weight="bold" fill="blue">FIRE</text>
                        <text x="220" y="150" font-size="0.65rem" font-weight="bold" fill="green">NO INCIDENT</text>
                    </svg>
                </div></center>
                """, unsafe_allow_html=True)
            letter_color = 'green'
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

            st.markdown(
                """<center style = "height:2rem;">
                <br>
                <p style = "font-size:13px;">_____ days without any recordable lost time injury.</p>
                </center>
                """, unsafe_allow_html=True
            )
            st.markdown("""
                    <style>
                    .horizental1 {
                        border-bottom: 5px dashed grey;
                        position: relative;
                        top: 0rem;
                        margin: 1rem 0rem;
                    }
                  </style>
                    <div class="horizental1">
                    </div>
                """, unsafe_allow_html=True)
            color = "blue"
            st.markdown("""<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Delivery</div></center>""", unsafe_allow_html=True)
            st.markdown(f"""
                <center><div>
                    <svg class="svg-container" height="150" width="450">
                        <text x="20" y="130" font-size="10rem" font-weight="bold" font-family="Arial" fill={color}>D</text>
                        <text x="250" y="30" font-size="0.65rem" font-weight="bold" fill="black">LEGEND:</text>
                        <text x="250" y="50" font-size="0.65rem" font-weight="bold" fill="green">TARGET ACHIEVED</text>
                        <text x="250" y="70" font-size="0.65rem" font-weight="bold" fill="red">TARGET MISSED</text>
                        <text x="250" y="90" font-size="0.65rem" font-weight="bold" fill="blue">PLANT OFF</text>
                    </svg>
                </center></div>
                """, unsafe_allow_html=True)
            st.markdown(
                """<center style = "height:2rem;">
                <br>                
                <p style = "font-size:13px;">______ days since OE delivery failure. </p>
                </center>
                """, unsafe_allow_html=True
            )
            with col_img_B:
                st.markdown("""
                    <style>
                    .vertical2 {
                      border-left: 5px dashed grey;
                      height: 31rem;
                      position:absolute;
                      left: 50%;
                    }
                  </style>
                    <div class="vertical2">
                    </div>
                """, unsafe_allow_html=True)

            with col_img_C:
                color = "orange"
                st.markdown("""<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Quality</div></center>""", unsafe_allow_html=True)
                st.markdown(f"""
                    <center><div>
                        <svg class="svg-container" height="150" width="450">
                            <text x="10" y="130" font-size="10rem" font-weight="bold" font-family="Arial" fill={color}>Q</text>
                            <text x="250" y="30" font-size="0.65rem" font-weight="bold" fill="black">LEGEND:</text>
                            <text x="250" y="50" font-size="0.65rem" font-weight="bold" fill="green">TARGET ACHIEVED</text>
                            <text x="250" y="70" font-size="0.65rem" font-weight="bold" fill="red">TARGET MISSED</text>
                            <text x="250" y="90" font-size="0.65rem" font-weight="bold" fill="blue">PLANT OFF</text>
                        </svg>
                    </center></div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                       <center style = "height:2rem;"> <br> <p style = "font-size:13px;">______ days since customer complaint.</p> </center>
                   """, unsafe_allow_html=True)
                st.markdown("""
                    <style>
                    .horizental1 {
                        border-bottom: 5px dashed grey;
                        position: relative;
                        top: 0rem;
                        margin: 1rem 0rem;
                    }
                  </style>
                    <div class="horizental1">
                    </div>
                """, unsafe_allow_html=True)
                color = "green"
                st.markdown("""<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Cost</div></center>""", unsafe_allow_html=True)
                st.markdown(f"""
                    <center><div>
                        <svg class="svg-container" height="150" width="450">
                            <text x="20" y="130" font-size="10rem" font-weight="bold" font-family="Arial" fill={color}>C</text>
                            <text x="250" y="30" font-size="0.65rem" font-weight="bold" fill="black">LEGEND:</text>
                            <text x="250" y="50" font-size="0.65rem" font-weight="bold" fill="green">TARGET ACHIEVED</text>
                            <text x="250" y="70" font-size="0.65rem" font-weight="bold" fill="red">TARGET MISSED</text>
                            <text x="250" y="90" font-size="0.65rem" font-weight="bold" fill="blue">PLANT OFF</text>
                        </svg>
                    </center></div>
                    """, unsafe_allow_html=True)
                st.markdown("""
                    <center style = "height:2rem;">
                    <br>
               <p style = "font-size:13px;">______ days since productivity target missed. </p>
                </center>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
             <style>
        .vertical1 {
          border-left: 5px dashed grey;
          height: 30rem;
          position:absolute;
          left: 50%;
        }
      </style>
        <div class="vertical1">
        </div>
        
        """, unsafe_allow_html=True)
    # For menu
    with col3:
        st.markdown("""<style>
                        .st-emotion-cache-115gedg:nth-child(1){ bottom:1rem; }
                        .st-emotion-cache-115gedg:nth-child(2){ bottom:4rem; }
                        .st-emotion-cache-1r6slb0:nth-child(1){ bottom:2.5rem; }
                        .st-emotion-cache-ocqkz7{ height:3rem }
                    </style>""", unsafe_allow_html=True)
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/info.png", width=50)
        with col_selector:
            generalInfo = st.selectbox("General Information", ["General Information", "Ground rule of meeting"],index=None, placeholder="General Information", label_visibility="hidden")
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/safety.png", width=50)
        with col_selector:
            safetySelection = st.selectbox("Safety", ["Safety FTD","Unsafe Incidents Tracking", "Unsafe Practice Tracking"], key="safety", index=None, placeholder="Safety", label_visibility="hidden")
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/quality.png", width=50)
        with col_selector:
            qualitySelection = st.selectbox("Quality", ["Quality FTD", "Customer Complaints", "Plant PPM & Supplier PPM", "FTP and Reported Rejection"],
                                            key="quality", index=None, placeholder="Quality", label_visibility="hidden")
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/delivery.png", width=50)
        with col_selector:
            deliverySelection = st.selectbox("Delivery", ["Delivery FTD", "OTIF", "Sale Plan vs Actual", "Critical Customer PDI", ], key='personal', index=None, placeholder="Delivery", label_visibility="hidden")

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/cost.png", width=50)
        with col_selector:
            costSelection = st.selectbox("Cost", ["Cost FTD", "Productivty and OEE", "RAW Material PDI", "Machine Breakdown Time"], key='delivery', index=None, placeholder="Cost", label_visibility="hidden")

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/problem_solving.png", width=50)
        with col_selector:
            # st.markdown("<br>", unsafe_allow_html=True)
            problem = st.selectbox("Problem Solving", ["Problem Solving"], index=None, placeholder="Problem Solving", label_visibility="hidden")

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/personal.png", width=50)
        with col_selector:
            personalSelection = st.selectbox("Personal", ["Daily", "Monthly", "Annually"], key='cost', index=None, placeholder="Personal", label_visibility="hidden")

    match safetySelection:
        case "":
            pass
        case "Safety FTD":
            switch_page("Safety FTD")
        case "Unsafe Incidents Tracking":
            switch_page("Unsafe_Incidents_Tracking")
        case "Unsafe Practice Tracking":
            switch_page("Unsafe Practice Tracking")

    match deliverySelection:
        case "Delivery FTD":
            switch_page("Delivery FTD")
        case "OTIF":
            switch_page("OTIF")
        case "Sale Plan vs Actual":
            switch_page("Sale_Plan_vs_Actual")
        case "Critical Customer PDI":
            switch_page("Critical_customer_PDI")

    match costSelection:
        case "Cost FTD":
            switch_page("Cost_FTD")
        case "Productivty and OEE":
            switch_page("Productivity_and_OEE")
        case "RAW Material PDI":
            switch_page("Raw_Metarial_PDI")
        case "Machine Breakdown Time":
            switch_page("Machine_breakdown_Time")

    match personalSelection:
        case "":
            pass
        case "Daily":
            switch_page("Personal FTD")
        case "Monthly":
            switch_page("Unsafe Practice Tracking")
        case "Annually":
            switch_page("Unsafe Practice Tracking")
    
    match qualitySelection:
        case "Quality FTD":
            switch_page("Quality FTD")
        case "Customer Complaints":
            switch_page("Customer_Complaints")
        case "Plant PPM & Supplier PPM":
            switch_page("Plant_&_Supplier_PPM")
        case "FTP and Reported Rejection":
            switch_page("FTP_and_Reported_Rejection")

    match generalInfo:
        case "General Information":
            switch_page("General-Info")
        case "Ground rule of meeting":
            switch_page("Ground_Rule_of_Meeting")

    match problem:
        case "":
            pass
        case "Problem Solving":
            switch_page("problemSolving")


main()
