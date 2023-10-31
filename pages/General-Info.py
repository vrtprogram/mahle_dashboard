import streamlit as st
from methods.main import layout, current_date

layout("General Information")

def main():
    # current_date()
    col1, col2, col3 = st.columns((1,0.2,1))
    with col1:
        st.markdown("""
        <h3 style='font-weight:bold; font-size:2rem;'>Morning meeting Agenda<h/3>
        """,unsafe_allow_html=True)
        st.markdown("""
                <div style='padding:0.5rem;'>
                    <ol>
                        <li>Discuss the data in SQDC format one by one.</li>
                        <li>Identify KPI's where target is not achieved and review the action plan.</li>
                        <li>Discuss the issues reported by the plant team.</li>
                        <li>Discuss the Problem solving cards and provide action plan with target closure date.</li>
                        <li>Carry out “Go & See” activity with your team for major problems. </li>
                        <li>Make “Go & See” a habit. If any major issue exist then discuss on 5S, safety, or check closure of any earlier problem.</li>
                        <li>Meeting to be carried out in the designated Plant SFM area.</li>
                    </ol>
                </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <style>
                .vertical2 {
                    border-left: 5px dashed grey;
                    height: 30rem;
                    position:absolute;
                    left: 50%;
                }
            </style>
            <div class="vertical2">
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <h3 style='font-weight:bold; font-size:2rem;'>Steps for Go & See<h/3>
        """,unsafe_allow_html=True)
        st.markdown("""
                <div>
                    <ol>
                        <li>Identify on the basis of prioritization matrix.</li>
                        <li>Go to the concentrated line or place.</li>
                        <li>Discuss raised problem with concerned operator</li>
                        <li>Observe the problem with CFT.</li>
                        <li>Come out from the line/place and discuss with the CFT & concerned operator.</li>
                        <li>Try to get direct cause by why-why analysis.</li>
                        <li>Mention responsible person and target date for the closure of problem card.</li>
                        <li>Handover one card (yellow) to responsible person.</li>
                        <li>If direct cause is not identified, call concerned department responsible in problem solving meeting.</li>
                        <li>Discuss the problem (root cause analysis) and action points in problem solving. </li>
                        <li>Appreciate the team for their contribution and efforts.</li>
                    </ol>
                </div>
        """, unsafe_allow_html=True)
        pass
    
if __name__ == "__main__":
    main()