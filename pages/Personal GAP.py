import streamlit as st
from methods.main import layout, personal_gap
from datetime import date

layout("Personal GAP")

def main():
    personal_gap()
    pass

if __name__ == "__main__":
    main()