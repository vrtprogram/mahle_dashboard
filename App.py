import streamlit as st
import pandas as pd
from plotly import express as px
from streamlit_extras.switch_page_button import switch_page
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

# ---- SETTING BASIC PAGE PARAMETERS AND TOP LOGOS ---- #
st.set_page_config(layout="wide", page_title="Welcome", initial_sidebar_state="collapsed")
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

colimg1, colimg2, colimg3 = st.columns((1.75, 1, 9), gap="small")
with colimg1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.image("resources/logo.png")
with colimg3:
    st.write("")
    st.write("")
    st.markdown("""<u><div style="font-size:450%;color:white"> VR Technologies</h1></u>""", unsafe_allow_html=True)

options = [
    "Main Page",
    "Safety",
    "Delivery",
    "Personal"
]
#choice = option_menu(None, options=options, #orientation="horizontal")

# if choice == 'Main Page':
#     switch_page('app')
# else:
#     switch_page(choice)


# --------------------------------------------------------------#

def main():
    colA_1, colB_1 = st.columns((5, 5), gap="small")
    with colA_1:
        st.image("resources/safety-s.gif", caption=None, width=None)
        col1, col2, col3 = st.columns((6, 5, 5), gap="small")
        if col2.button("Safety", key="Safety"):
            switch_page("Safety")
    with colB_1:
        st.image("resources/Quality-Q.gif", caption=None, width=None)
        col4, col5, col6 = st.columns((6, 5, 5), gap="small")
        if col5.button("Quality", key="Quality"):
            switch_page("Delivery")

    colA_2, colB_2 = st.columns((5, 5), gap="small")
    with colA_2:
        st.image("resources/Delivery-D.gif", caption=None, width=None)
        col6, col7, col8 = st.columns((6, 5, 5), gap="small")
        if col7.button("Delivery", key="Delivery"):
            switch_page("Delivery")
    with colB_2:
        st.image("resources/p.gif", caption=None, width=None)
        col9, col10, col11 = st.columns((6, 5, 5), gap="small")
        if col10.button("Personal", key="Personal"):
            switch_page("Personal")

    st.write('<h1>"<u>Best SPM Manufacture In India</u>"<h1> ', unsafe_allow_html=True)
    components.iframe(
        'https://docs.google.com/presentation/d/e/2PACX-1vT5Ni04N7k13yn0nnFzGP8lTxXuXVTDKkUc6V6ukdCaWs3g3hKahZZYvEOUqK5zQcb66asOg-r12am7/embed?start=true&loop=true&delayms=10000',
        height=470)


if __name__ == "__main__":
    main()
