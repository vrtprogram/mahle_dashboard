from methods.main import layout, fetch_data
import streamlit as st

layout("Problem Solving Competency")

def main():
    psc_data = fetch_data("PROBLEM SOLVING COMPETENCY")
    st.markdown(f"""
        <style>
            .category{{border:1px solid black; width:12%; padding-top:1rem; float:left; height: 3rem; text-align:center; font-weight:bold;}}
            .content{{border:1px solid black; width:12%; padding-top:1rem; float:left; height: 3rem; text-align:center;}}
            .main_category{{border:1px solid black; width:28%; padding-top:1rem; float:left; height: 3rem; text-align:center; font-weight:bold;}}
        </style>
        <div>
            <div class="main_category">Days in Week</div>
            <div class="category">day 1</div>
            <div class="category">day 2</div>
            <div class="category">day 3</div>
            <div class="category">day 4</div>
            <div class="category">day 5</div>
            <div class="category">day 6</div>
        </div>
        <div>
            <div class="main_category">Problem Raised (A)</div>
            <div class="content">day 1</div>
            <div class="content">day 2</div>
            <div class="content">day 3</div>
            <div class="content">day 4</div>
            <div class="content">day 5</div>
            <div class="content">day 6</div>
        </div>
        <div>
            <div class="main_category">Problem Solved (B)</div>
            <div class="content">day 1</div>
            <div class="content">day 2</div>
            <div class="content">day 3</div>
            <div class="content">day 4</div>
            <div class="content">day 5</div>
            <div class="content">day 6</div>
        </div>
        <div>
            <div class="main_category">Problem WIP</div>
            <div class="content">day 1</div>
            <div class="content">day 2</div>
            <div class="content">day 3</div>
            <div class="content">day 4</div>
            <div class="content">day 5</div>
            <div class="content">day 6</div>
        </div>
        <div>
            <div class="main_category">PSP Competency</div>
            <div class="content">day 1</div>
            <div class="content">day 2</div>
            <div class="content">day 3</div>
            <div class="content">day 4</div>
            <div class="content">day 5</div>
            <div class="content">day 6</div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
