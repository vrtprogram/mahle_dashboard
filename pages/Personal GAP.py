import streamlit as st
from methods.main import layout
from datetime import date

layout("Personal GAP")

def main():
    my_date = date(year=2023, month=10, day=10)
    formatted_time = my_date.ctime()
    print(formatted_time)
    st.write(formatted_time)
    pass

if __name__ == "__main__":
    main()