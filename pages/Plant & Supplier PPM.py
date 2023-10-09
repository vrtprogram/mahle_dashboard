import streamlit as st
from methods.main import layout, plant_supplier_ppm

layout("Plant & Supplier PPM")

def main():
    plant_supplier_ppm()

    h2_col1, h2_col2 = st.columns((1,1.5))
    with h2_col1:
        st.subheader(":blue[PPM Trend]",divider="rainbow")
        st.markdown("weekly and early Graph")
    with h2_col2:
        pass

if __name__ == "__main__":
    main()