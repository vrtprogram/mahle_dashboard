import streamlit as st
import base64
import os
from streamlit_extras.switch_page_button import switch_page


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


# Setting up page Config.
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

st.markdown(
    """
    <center>
     <div style="background-color: blue; font-family:fantasy">
        <i>
            <h1>
                Shopfloor Management
            </h1>
        </i>
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
        gif_html = get_img_with_href("resources/safety-s.gif", "/SafetyDaily")
        st.markdown(gif_html, unsafe_allow_html=True)
        st.markdown(
            """<center>
            <h4 style = "font-family: Cambria"> Safety </h4>
            </center>
            """, unsafe_allow_html=True
        )
        st.markdown("---")
        gif_html = get_img_with_href("resources/Delivery-D.gif", "/DeliveryDaily")
        st.markdown(gif_html, unsafe_allow_html=True)
        st.markdown(
            """<center>
            <h4 style = "font-family: Cambria"> Delivery </h4>
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
            gif_html = get_img_with_href("resources/p.gif", "/PersonalDaily")
            st.markdown(gif_html, unsafe_allow_html=True)
            st.markdown("""
            <center>
            <h4 style = "font-family: Cambria"> Personal </h4>
            </center>
            """, unsafe_allow_html=True)
            st.markdown("---")
            gif_html = get_img_with_href("resources/Quality-Q.gif", "/QualityDaily")
            st.markdown(gif_html, unsafe_allow_html=True)
            st.markdown("""
                <center>
            <h4 style = "font-family: Cambria"> Quality </h4>
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
        # st.markdown("<br>", unsafe_allow_html=True)
        st.image("resources/info.png", width=50)
    with col_selector:
        st.link_button("General Information", "/GeneralInfo")
    col_icon, col_selector = st.columns((1, 2))
    with col_icon:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("resources/safety.png", width=50)
    with col_selector:
        safetySelection = st.selectbox("Safety", ["", "Daily", "Monthly", "Annually"], key="safety")
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
        st.image("resources/problem_solving.png", width=50)
    with col_selector:
        st.markdown("<br>", unsafe_allow_html=True)
        st.link_button("Problem Solving", "/ProblemSolving")

    col_icon, col_selector = st.columns((1, 2))
    with col_icon:
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("resources/cost.png", width=50)
    with col_selector:
        costSelection = st.selectbox("Cost", ["", "Daily", "Monthly", "Annually"], key='cost')

match safetySelection:
    case "":
        pass
    case "Daily":
        switch_page("SafetyDaily")
    case "Monthly":
        switch_page("Safety")
    case "Annually":
        switch_page("Safety")

match costSelection:
    case "":
        pass
    case "Daily":
        switch_page("SafetyDaily")
    case "Monthly":
        switch_page("Safety")
    case "Annually":
        switch_page("Safety")

match deliverySelection:
    case "":
        pass
    case "Daily":
        switch_page("SafetyDaily")
    case "Monthly":
        switch_page("Safety")
    case "Annually":
        switch_page("Safety")

match personalSelection:
    case "":
        pass
    case "Daily":
        switch_page("SafetyDaily")
    case "Monthly":
        switch_page("Safety")
    case "Annually":
        switch_page("Safety")
match qualitySelection:
    case "":
        pass
    case "Daily":
        switch_page("SafetyDaily")
    case "Monthly":
        switch_page("Safety")
    case "Annually":
        switch_page("Safety")
