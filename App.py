import streamlit as st
import base64
import os


# FUNCTION TO GET IMAGE WITH HREF
@st.cache_data()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache_data()
def get_img_with_href(local_img_path, target_url):
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


def safety_page_switcher():
    select = st.session_state["safety"]

    if select:
        print("Selected", select)


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
        </style>
        """, unsafe_allow_html=True)

st.markdown(
    """
    <center>
     <div style="background-color: blue;">
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
        gif_html = get_img_with_href("resources/safety-s.gif", "/Safety")
        st.markdown(gif_html, unsafe_allow_html=True)
        st.markdown(
            """<center>
            <h4 style = "font-family: Cambria"> Safety </h4>
            </center>
            """, unsafe_allow_html=True
        )
        st.markdown("---")
        gif_html = get_img_with_href("resources/Delivery-D.gif", "/Delivery")
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
                  border-left: 5px dashed white;
                  height: 40rem;
                  position:center;
                  left: 50%;
                }
              </style>
                <div class="vertical2">
                </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("""
         <style>
    .vertical1 {
      border-left: 5px dashed white;
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
    st.selectbox("Safety", ["Daily", "Monthly", "Annually"], on_change=safety_page_switcher, key="safety")
