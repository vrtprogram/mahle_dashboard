import streamlit as st
from methods.main import layout, current_date

layout("General Information")

def main():
    st.markdown("""
        <h3 style='font-weight:bold; font-size:2rem;'>Ground Rule of Meeting<h/3>
    """,unsafe_allow_html=True)
    st.markdown("""
                <div style='padding:1rem;'>
                    <ol>
                        <li>Start or end meeting on time.</li>
                        <li>Stay on task no side conversation.</li>
                        <li>Listen to others and don't interrupt.</li>
                        <li>Remain focused and don't attend calls.</li>
                        <li>Make decision based on clear information</li>
                        <li>Bring closure to decision</li>
                        <li>Identify actions that results from decisions.</li>
                        <li>Accept the fact that there will be difference in opinion.</li>
                        <li>Show mutual respect.</li>
                        <li>Honor brainstorming without being attached to viewpoint.</li>
                        <li>Keep notes of the meeting as an individual.</li>
                        <li>Attack the problems not the person - “no blame game”.</li>
                        <li>Speak your mind without fear or reprisal.</li>
                    </ol>
                </div>
    """, unsafe_allow_html=True)
    
    pass

if __name__ == "__main__":
    main()