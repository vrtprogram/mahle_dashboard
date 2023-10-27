from methods.main import layout, current_date, fetch_data
import streamlit as st

layout("Visits or Audits")

def main():
    current_date()
    visit_data = fetch_data("VISITS")
    visit_data.get_specific_data("DATE", "2023-10-15")
    # visit_data = visit_data.get_data()
    # st.table(visit_data[["DATE", "Purpose of Visit", "Visited by Customer or Auditor", "Remarks or Responsibility"]])
    pass

if __name__ == "__main__":
    main()