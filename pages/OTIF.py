import streamlit as st
from methods.main import layout, otif

layout("On Time In Full (OTIF)")

def main():
    otif()

    h2_col1, h2_col2 = st.columns((1,1.5))
    with h2_col1:
        st.subheader(":blue[OTIF Trend]",divider="rainbow")
        st.markdown("weekly and early Graph")
    with h2_col2:
        pass

if __name__ == "__main__":
    main()