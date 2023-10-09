import streamlit as st
from methods.main import layout

layout("FTP & Reported Rejection")

def main():
    h1_col1, h1_col2 = st.columns((1.1,1))
    with h1_col1:
        st.subheader(":blue[FTP And Reported Rejection]",divider="rainbow")
    with h1_col2:
        pass 
    # st.write("""<div style='text-align:center;font-size:1.5rem;font-weight:bold;padding-top:1.5rem;'><u>FTP And Reported Rejection</u></div>""",unsafe_allow_html=True)
    st.write("""
                <style>
                     .float-container { padding: 5px;   }
                     .float-prb { width: 55%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                    .float-prt { width: 20%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                    .float-pn {width: 20%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .float-ir {width: 40%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .float-ca {width: 20%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .float-td {width: 15%;font-size:0.8rem; color:red;float: left;font-weight:bold;height:10rem;text-align:center;padding: 10px;border: 1px solid black;
                    }
                    .par {padding-top:1rem; font-size:0.7rem; color:black; }
                    hr{ margin:0em; }
                </style>
                <div>
                     <div class="float-container">
                        <div class="float-prb" style='color:red;height:2rem;'>Particular</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Target</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Actual</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">Firtst Time Pass % (FTP)</div>
                        <div class="float-prt">tftp</div>
                        <div class="float-prt">aftp</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">Reported Rejection (Percntage)</div>
                        <div class="float-prt">trp</div>
                        <div class="float-prt">arp</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">Reported Rejection (INR)</div>
                        <div class="float-prt">tri</div>
                        <div class="float-prt">tri</div>
                    </div>
                </div>
                <div class="float-container">
                    <div class="float-pn">Part number<hr><p class="par">prn</p></div>
                    <div class="float-ir">Issue Reported<hr><p class="par">irp</p></div>
                    <div class="float-ca">Corrective Action<hr><p class="par">cra</p></div>
                    <div class="float-td">Targate Date<hr><p class="par">tda</p></div>
                </div>
            """.replace("tftp",(str("Tar_FTP")))
            .replace("aftp",(str("Act_FTP")))
            .replace("trp",(str("Tar_TRP")))
            .replace("trp",(str("Act_TRP")))
            .replace("tri",(str("Tar_TRI")))
            .replace("tri",(str("Act_TRI")))
            .replace("prn",(str("Part_No")))
            .replace("irp",(str("Issue_Repo")))
            .replace("cra",(str("Crt_Act")))
            .replace("tda",(str("Trg_Date"))),unsafe_allow_html=True)
    
    h2_col1, h2_col2 = st.columns((1.1,1))
    with h2_col1:
        st.subheader(":blue[FTP and Reported Rejection Trend]",divider="rainbow")
        st.markdown("weekly and early Graph")
    with h2_col2:
        pass
    
if __name__ == "__main__":
    main()