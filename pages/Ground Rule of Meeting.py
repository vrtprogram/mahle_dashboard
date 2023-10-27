import streamlit as st
from methods.main import layout, current_date

layout("Ground Rule of Meeting")

def main():
    current_date()
    st.markdown("""
                <div>
                    <ul>
                        <li><h5>Start or end meeting on time.</h5></li>
                        <li><h5>Stay on task no side conversation.</h5></li>
                        <li><h5>Listen to others and don't interrupt.</h5></li>
                        <li><h5>Remain focused and don't attend calls./h5></li>
                        <li><h5>Make decision based on clear information</h5></li>
                        <li><h5>Bring closure to decision</h5></li>
                        <li><h5>Identify actions that results from decisions.</h5></li>
                        <li><h5>Accept the fact that there will be difference in opinion.</h5></li>
                        <li><h5>Show mutual respect.</h5></li>
                        <li><h5>Honor brainstorming without being attached to viewpoint.</h5></li>
                        <li><h5>Keep notes of the meeting as an individual.</h5></li>
                        <li><h5>Attack the problems not the person - “no blame game”.</h5></li>
                        <li><h5>Speak your mind without fear or reprisal.</h5></li>
                    </ul>
                </div>
    """, unsafe_allow_html=True)
    
    pass

if __name__ == "__main__":
    main()