from methods.main import layout, current_date, visits
import streamlit as st

layout("Visits or Audits")

def main():
    # current_date()
    visits()

if __name__ == "__main__":
    main()