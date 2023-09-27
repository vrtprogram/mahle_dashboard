import streamlit as st
import base64
import os
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", page_title="Welcome", initial_sidebar_state='collapsed')
st.markdown("""
            <style>
                   .block-container {
                        padding-top: 20px;
                        padding-bottom: 1px;
                        padding-left: 10px;
                        padding-right: 10px;
                    }
                    .element-container{
                        padding:None;
                    }

            </style>
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                .stDeployButton{visibility:hidden;}
            </style>
            """, unsafe_allow_html=True)


st.cache_data()
def main():
    # Setting up page Config.
    def get_base64_of_bin_file(bin_file) -> base64:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()

    def get_img_with_href(local_img_path, target_url) -> str:
        img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
        bin_str = get_base64_of_bin_file(local_img_path)
        html_code = f'''
        <center>
            <a href="{target_url}">
                <img src="data:image/{img_format};base64,{bin_str}" class='custom_image'  height=250px, width=270px />
            </a>
        </center>
            '''
        return html_code



    st.markdown(
        """
        <center>
         <div>
            <i><u>
                <h1 style="font-size:60px;">
                    Shopfloor Management
                </h1>
            </u></i>
        </div>
        </center>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        "<br>", unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns((5, 0.5, 2))

    # column for images
    with col1:
        col_img_A, col_img_B, col_img_C = st.columns((1, 0.2, 1))
        with col_img_A:
            gif_html = get_img_with_href("resources/safety-s.gif", "/SafetyFTD")
            st.markdown(gif_html, unsafe_allow_html=True)
            st.markdown(
                """<center>
                <br>
                <p style = "font-size:12px">_____ days without any recordable lost time injury.</p>
                </center>
                """, unsafe_allow_html=True
            )
            st.markdown("---")
            gif_html = get_img_with_href("resources/Delivery-D.gif", "/DeliveryFTD")
            st.markdown(gif_html, unsafe_allow_html=True)
            st.markdown(
                """<center>
                <br>                
                <p style = "font-size:12px">______ days since OE delivery failure. </p>
                </center>
                """, unsafe_allow_html=True
            )
            with col_img_B:
                st.markdown("""
                    <style>
                    .vertical2 {
                      border-left: 5px solid grey;
                      height: 40rem;
                      position:absolute;
                      left: 50%;
                    }
                  </style>
                    <div class="vertical2">
                    </div>
                """, unsafe_allow_html=True)

            with col_img_C:
                gif_html = get_img_with_href("resources/Quality-Q.gif", "/QualityFTD")
                st.markdown(gif_html, unsafe_allow_html=True)
                st.markdown("""
                       <center>
                       <br>
                          <p style = "font-size:12px">______ days since customer complaint. </p>
                           </center>
                   """, unsafe_allow_html=True)
                st.markdown("---")
                gif_html = get_img_with_href("resources/C.gif", "/CostFTD")
                st.markdown(gif_html, unsafe_allow_html=True)
                st.markdown("""
                    <center>
                    <br>
               <p style = "font-size:12px">______ days since productivity target missed. </p>
                </center>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
             <style>
        .vertical1 {
          border-left: 5px dashed grey;
          height: 40rem;
          position:absolute;
          left: 50%;
        }
      </style>
        <div class="vertical1">
        </div>
        
        """, unsafe_allow_html=True)
    # For menu
    with col3:
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/info.png", width=50)
        with col_selector:
            generalInfo = st.selectbox("General Information", ["", "General Information"])
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/safety.png", width=50)
        with col_selector:
            safetySelection = st.selectbox("Safety", ["", "Safety FTD", "Unsafe Practice Tracking"], key="safety")
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/quality.png", width=50)
        with col_selector:
            qualitySelection = st.selectbox("Quality", ["", "Daily", "Monthly", "Annually", "Customer Complaints"],
                                            key="quality")
        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/personal.png", width=50)
        with col_selector:
            personalSelection = st.selectbox("Personal", ["", "Daily", "Monthly", "Annually", ], key='personal')

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/delivery.png", width=50)
        with col_selector:
            deliverySelection = st.selectbox("Delivery", ["", "Daily", "Monthly", "Annually"], key='delivery')

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/problem_solving.png", width=50)
        with col_selector:
            st.markdown("<br>", unsafe_allow_html=True)
            problem = st.selectbox("Problem Solving", ["", "Problem Solving"])

        col_icon, col_selector = st.columns((1, 2))
        with col_icon:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image("resources/cost.png", width=50)
        with col_selector:
            costSelection = st.selectbox("Cost", ["", "Daily", "Monthly", "Annually"], key='cost')

    match safetySelection:
        case "":
            pass
        case "Safety FTD":
            switch_page("Safety FTD")
        case "Unsafe Practice Tracking":
            switch_page("Unsafe Practice Tracking")
        case "Annually":
            switch_page("Unsafe Practice Tracking")

    match costSelection:
        case "":
            pass
        case "Daily":
            switch_page("Cost FTD")
        case "Monthly":
            switch_page("Unsafe Practice Tracking")
        case "Annually":
            switch_page("Unsafe Practice Tracking")

    match deliverySelection:
        case "":
            pass
        case "Daily":
            switch_page("Delivery FTD")
        case "Monthly":
            switch_page("Unsafe Practice Tracking")
        case "Annually":
            switch_page("Unsafe Practice Tracking")

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
        case "":
            pass
        case "Daily":
            switch_page("Quality FTD")
        case "Monthly":
            switch_page("Unsafe Practice Tracking")
        case "Annually":
            switch_page("Unsafe Practice Tracking")

    match generalInfo:
        case "":
            pass
        case "General Information":
            switch_page("General-Info")

    match problem:
        case "":
            pass
        case "Problem Solving":
            switch_page("problemSolving")


main()
