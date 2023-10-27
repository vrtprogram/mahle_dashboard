import streamlit as st
from methods.main import layout, current_date

layout("General Information")

def main():
    current_date()
    col1, col2 = st.columns((1,1))
    with col1:
        st.markdown(
        """
        # Morning meeting Agenda

        - Discuss the data in SQDC format one by one.

        - Identify KPI's where target is not achieved and review the action plan.

        - Discuss the issues reported by the plant team.

        - Discuss the Problem solving cards and provide action plan with target closure date.

        - Carry out “Go & See” activity with your team for major problems. 

        - Make “Go & See” a habit. If any major issue exist then discuss on 5S, safety, or check closure of any earlier problem.

        - Meeting to be carried out in the designated Plant SFM area.
        """
        )
        pass
    with col2:
        st.markdown("""
            # Steps for Go & See

            - Identify on the basis of prioritization matrix.

            - Go to the concentrated line or place.

            - Discuss raised problem with concerned operator

            - Observe the problem with CFT.

            - Come out from the line/place and discuss with the CFT & concerned operator.

            - Try to get direct cause by why-why analysis.

            - Mention responsible person and target date for the closure of problem card.

            - Handover one card (yellow) to responsible person.

            - If direct cause is not identified, call concerned department responsible in problem solving meeting.

            - Discuss the problem (root cause analysis) and action points in problem solving. 

            - Appreciate the team for their contribution and efforts.
        """)
        pass
    
if __name__ == "__main__":
    main()