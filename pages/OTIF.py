import streamlit as st
from methods.main import layout, otif

layout("On Time In Full (OTIF)")

def main():
    otif()

if __name__ == "__main__":
    main()