import streamlit as st
import base64
import os
from streamlit_extras.switch_page_button import switch_page
from methods.main import layout, S_letter, Q_letter, D_letter, C_letter


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
            st.markdown(
                """<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Safety</div></center>""", unsafe_allow_html=True)
            S_letter()  # Dynamic svg letter
            st.markdown("""
                    <style>
                    .horizental1 {
                        border-bottom: 3px dashed grey;
                        position: relative;
                        top: 0rem;
                        margin: 1rem 0rem;
                    }
                  </style>
                    <div class="horizental1">
                    </div>
                """, unsafe_allow_html=True)
            color = "blue"
            st.markdown(
                """<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Delivery</div></center>""", unsafe_allow_html=True)
            D_letter()  # Dynamic svg letter
            with col_img_B:
                st.markdown("""
                    <style>
                    .vertical2 {
                      border-left: 3px dashed grey;
                      height: 37rem;
                      position:absolute;
                      left: 50%;
                    }
                  </style>
                    <div class="vertical2">
                    </div>
                """, unsafe_allow_html=True)
            with col_img_C:
                color = "orange"
                st.markdown(
                    """<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Quality</div></center>""", unsafe_allow_html=True)
                Q_letter()  # Dynamic svg letter
                st.markdown("""
                    <style>
                    .horizental1 {
                        border-bottom: 3px dashed grey;
                        position: relative;
                        top: 0rem;
                        margin: 1rem 0rem;
                    }
                  </style>
                    <div class="horizental1">
                    </div>
                """, unsafe_allow_html=True)
                color = "green"
                st.markdown(
                    """<center><div style='background-color:lightgray; width:95%; font-weight:bold;'>Cost</div></center>""", unsafe_allow_html=True)
                C_letter()  # Dynamic svg letter
    with col2:
        st.markdown("""
             <style>
        .vertical1 {
          border-left: 3px dashed grey;
          height: 35rem;
          position:absolute;
          left: 50%;
        }
      </style>
        <div class="vertical1">
        </div>
        """, unsafe_allow_html=True)
    # For menu
    with col3:
        st.markdown("""<center><div style='background-color:lightgray; position:relative; bottom:1rem; border-radius:5px; width:100%; font-weight:bold;'>KPI Information</div></center>""", unsafe_allow_html=True)
        st.markdown("""<style>
                        .st-emotion-cache-115gedg:nth-child(1){ bottom:1rem; }
                        .st-emotion-cache-115gedg:nth-child(2){ bottom:2rem; }
                        .st-emotion-cache-1r6slb0:nth-child(1){ bottom:0.5rem; }
                        .st-emotion-cache-ocqkz7{ height:3rem }
                    </style>""", unsafe_allow_html=True)
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/info.png", width=50)
        with col_selector:
            generalInfo = st.selectbox("General Information", [
                                       "General Information", "Ground rule of meeting"], index=None, placeholder="General Information", label_visibility="hidden")
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/safety.png", width=50)
        with col_selector:
            safetySelection = st.selectbox("Safety", ["Safety FTD", "Unsafe Incidents Tracking", "Unsafe Practice Tracking"],
                                           key="safety", index=None, placeholder="Safety", label_visibility="hidden")
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
            deliverySelection = st.selectbox("Delivery", ["Delivery FTD", "OTIF", "Sale Plan vs Actual", "Critical Customer PDI", ],
                                             key='personal', index=None, placeholder="Delivery", label_visibility="hidden")

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/cost.png", width=50)
        with col_selector:
            costSelection = st.selectbox("Cost", ["Cost FTD", "Productivty and OEE",
                                         "Machine Breakdown Time"], key='delivery', index=None, placeholder="Cost", label_visibility="hidden")

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/problem_solving.png", width=50)
        with col_selector:
            # st.markdown("<br>", unsafe_allow_html=True)
            problem = st.selectbox("Problem Solving", [
                                   "Problem Solving"], index=None, placeholder="Problem Solving", label_visibility="hidden")

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            # st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/personal.png", width=50)
        with col_selector:
            personalSelection = st.selectbox("Personal", [
                                             "Personal Gap", "Visits/Audits", "Attendance Sheet"], key='cost', index=None, placeholder="Personal", label_visibility="hidden")

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            if st.button("Data"):
                switch_page("Data")
        with col_selector:
            pass

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
        case "Personal Gap":
            switch_page("Personal_GAP")
        case "Visits/Audits":
            switch_page("Visits")
        case "Attendance Sheet":
            switch_page("Attendance")

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
            switch_page("Problem_Solving_Competency")


main()
