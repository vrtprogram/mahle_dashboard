import streamlit as st

st.set_page_config(layout="wide", page_title="Safety FTD", initial_sidebar_state="collapsed")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 20px;
                    padding-bottom: 0rem;
                    padding-left: 10px;
                    padding-right: 10px;
                }
        </style>
        """, unsafe_allow_html=True)


def main():
    st.markdown(
        """
        <center>
         <div style="background-color: blue; font-family:fantasy">
            <i><u>
                <h1>
                    Safety Incidents Tracking
                </h1>
            </u></i>
        </div>
        </center>
        """,
        unsafe_allow_html=True
    )


main()
