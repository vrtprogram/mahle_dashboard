import streamlit as st
from methods.main import layout, current_date, ftp_rejection

layout("FTP & Reported Rejection")

def main():
    current_date()
    # st.write("""<div style='text-align:center;font-size:1.5rem;font-weight:bold;padding-top:1.5rem;'><u>FTP And Reported Rejection</u></div>""",unsafe_allow_html=True)
    ftp_rejection()
    
    
if __name__ == "__main__":
    main()