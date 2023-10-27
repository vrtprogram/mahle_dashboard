import streamlit as st
from methods.main import layout, plant_supplier_ppm

layout("Plant & Supplier PPM")

def main():
    plant_supplier_ppm()

if __name__ == "__main__":
    main()