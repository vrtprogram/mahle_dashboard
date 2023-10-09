from methods.main import layout, incident_tracking, incident_detail, current_updates

layout("Safety FTD")

def main():
    current_updates()
    incident_tracking()
    incident_detail()
    pass

    # *** Get Data between two dates*** 
    # from_date = st.date_input("From:")
    # to_date = st.date_input("To:")
    # days = from_date - to_date
    # query = "SELECT SUM(Value) AS Total FROM UNSAFE_PRACTICE_TRACKING WHERE Date BETWEEN ? AND ?"
    # cursor.execute(query, (from_date, to_date))
    # Value_SD = cursor.fetchone()[0]
    # if st.button("Show"):
    #     st.write(f"Total value for {days} days: {Value_SD}")

if __name__ == "__main__":
    main()


# def main():
#     app = SafetyApp()
#     app.render_safety_dashboard()
#     app.render_incident_tracking()

# if __name__ == "__main__":
#     main()