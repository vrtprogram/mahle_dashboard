import streamlit as st
from methods.main import layout
from datetime import date

layout("Personal GAP")

def main():
    col1, col2 = st.columns((1,1))
    with col1:
        st.markdown(
                """
                <style>
                .custom {
                    margin: 0.7rem;
                    padding-top: 1rem;
                    border: 1px solid black;
                    height: 8rem;
                    font-size:1.15rem;
                    border-radius: 0.7rem;
                    font-weight: bold;
                    box-shadow: 5px 5px 10px;
                    text-align: center;
                }
                .custom h4{ font-weight:bold; }
                @media (min-width: 1920px) and (max-width: 2860px){
                    .custom { font-size:1.35rem; height:10rem; }
                    .custom h4{ font-size:1.3rem; font-weight:bold; padding-top:1rem}
                }
                </style>
                """,
                unsafe_allow_html=True
            )   #custom css for columns
        cr11,cr12=st.columns((1,1))
        with cr11:
            st.markdown(f"""<div class="custom">Planned Manpower Required
                        <h4>{"655"}</h4></div>""",unsafe_allow_html=True)
            st.markdown(f"""<div class="custom">Actual Manpower Available
                        <h4>{"45"}</h4></div>""",unsafe_allow_html=True)
        with cr12:
            st.markdown(f"""<div class="custom">Personal Gap (PG)
                        <h4>{"54"}</h4></div>""",unsafe_allow_html=True)
            st.markdown(f"""<div class="custom">Planned & Unplanned Absenteelsm
                        <h4>{"58"}</h4></div>""",unsafe_allow_html=True)
        pass
    with col2:
        pr_1 = ""
        pr_2 = ""
        pr_3 = ""
        st.markdown(f"""<style>
                    .head{{height:25rem; width:100%; border:1px solid black;}} .head h4{{padding-top:1rem}} .head hr{{margin:0.3em;}} .head p{{padding-top:1rem; overflow-wrap:break-word;}}
                    </style><div class="head"><center><h4>Top 3 Problems</h4><hr><p>{pr_1}</p><p>{pr_2}</p><p>{pr_3}</p></center></div>""",unsafe_allow_html=True)

if __name__ == "__main__":
    main()