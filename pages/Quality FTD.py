import streamlit as st
from datetime import datetime

st.set_page_config(layout="wide", page_title="Safety FTD", initial_sidebar_state="collapsed")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 1.5rem;
                    padding-right: 1.5rem;
                }
        </style>
        """, unsafe_allow_html=True)
hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    st.markdown(
        """
        <center>
         <div style="margin-bottom:1rem; font-family:fantasy">
            <i><u>
                <h1>
                    Quality FTD 
                </h1>
            </u></i>
        </div>
        </center>
        """,
        unsafe_allow_html=True
    )
    st.markdown("___")

    d_col1, d_col2=st.columns((1,0.3))
    with d_col1:
        pass
    with d_col2:
        on_date = st.date_input(":green[Select Date:]")
        on_time = datetime.now().time().strftime("%H:%M")
        # st.write(on_date)
    col1,col2=st.columns((1,1.8))
    with col1:
        # date=datetime.now().date().strftime("%d-%m-%Y")
        st.subheader(f":blue[Status as on: {on_date}]",divider="rainbow")
    with col2:
        st.subheader(":blue[Costomer Complaints]",divider="rainbow")
        st.markdown("""
            <style>
                    .float-container {  padding: 5px;   }
                    .float-cn {width: 22%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-cd {width: 35%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-dr {width: 15%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-dc {width: 15%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .float-st {width: 13%; font-size:0.8rem; color:red; float: left; font-weight:bold; height:10rem; text-align:center; padding: 10px; border: 1px solid black;
                    }
                    .par {padding-top:1rem; font-size:0.7rem; color:black; }
                    hr{ margin:0em; }
                    
            </style>
            <div class="float-container">
                <div class="float-cn">Complaints<hr><p class="par">comp_no</p></div>
                <div class="float-cd">Complaint details<hr><p class="par">comp_det</p></div>
                <div class="float-dr">Raised<hr><p class="par">comp_rais</p></div>
                <div class="float-dc">Close<hr><p class="par">comp_cls</p></div>
                <div class="float-st">Status<hr><p class="par">comp_sts</p></div>
            </div>
        """.replace("comp_no",(str("test_no")))
        .replace("comp_det",(str("test_complaint")))
        .replace("comp_rais",(str("test_ris")))
        .replace("comp_cls",(str("test_cls")))
        .replace("comp_sts",(str("CLOSE"))),unsafe_allow_html=True)

        st.subheader(":blue[Plant PPM & Supplier PPM]",divider="rainbow")
        cl1,cl2=st.columns((1,1.5))
        with cl1:
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:1rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center;'>Plant PPM
                        <div style='content: "";display: table;clear: both;'>
                            <div style='float: left;width: 50%;padding: 1rem 2rem;'>Actual
                                <h6 style='color:white;'>$1</h6>
                            </div>
                            <div style='float: left;width: 50%;padding: 1rem 1.5rem;'>Actual
                                <h6 style='color:white;'>$2</h6>
                            </div>
                        </div>
                        </div>""".replace("$1",str("32")).replace("$2",str("13")),unsafe_allow_html=True)
            st.markdown(f"""<div style='background-color:tomato;margin:1rem;padding-top:1.3rem;border:1px solid black;height:8rem;border-radius:0.7rem;font-weight:bold;box-shadow:5px 5px 10px;text-align:center'>Supplier PPM
                        <div style='content: center;display: table;clear: both;'>
                            <div style='float: left;test-align:center;width: 50%;padding:1rem 2rem;'>Actual
                                <h6 style='color:white;'>$1</h6>
                            </div>
                            <div style='float: right;test-align:center;width: 50%;padding:1rem 1.5rem;'>Actual
                                <h6 style='color:white;'>$2</h6>
                            </div>
                        </div>
                        </div>""".replace("$1",str("42")).replace("$2",str("52")),unsafe_allow_html=True)
        with cl2:
            st.write("""
                <style>
                     .float-container { padding: 5px;   }
                     .float-prb { width: 50%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                    .float-prt { width: 25%; font-size:0.8rem; float: left; font-weight:bold; height:3.5rem; text-align:center; padding: 5px; border: 1px solid black;
                    }
                </style>
                <div style='padding-top:0.8rem;'>
                     <div class="float-container">
                        <div class="float-prb" style='color:red;height:2rem;'>Problems</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Part/Line</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Rej Qty</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">ppm_prb1</div>
                        <div class="float-prt">ppm_prt1</div>
                        <div class="float-prt">ppm_qty1</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">ppm_prb1</div>
                        <div class="float-prt">ppm_prt1</div>
                        <div class="float-prt">ppm_qty1</div>
                    </div>
                </div>
                <div style='padding-top:0.8rem;'>
                     <div class="float-container">
                        <div class="float-prb" style='color:red;height:2rem;'>Problems</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Part/Line</div>
                        <div class="float-prt" style='color:red;height:2rem;'>Rej Qty</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">spm_prb1</div>
                        <div class="float-prt">spm_prt1</div>
                        <div class="float-prt">spm_qty1</div>
                    </div>
                    <div class="float-container">
                        <div class="float-prb">spm_prb1</div>
                        <div class="float-prt">spm_prt1</div>
                        <div class="float-prt">spm_qty1</div>
                    </div>
                </div>
            """.replace("ppm_prb1",str("nppb1"))
            .replace("ppm_prt1",str("nppt1"))
            .replace("ppm_qty1",str("nppq1"))
            .replace("ppm_prb2",str("nppb2"))
            .replace("ppm_prt2",str("nppt2"))
            .replace("ppm_qty2",str("nppq2"))
            .replace("spm_prb1",str("sppb1"))
            .replace("spm_prt1",str("sppt1"))
            .replace("spm_qty1",str("sppq1"))
            .replace("spm_prb2",str("sppb2"))
            .replace("spm_prt2",str("sppt2"))
            .replace("spm_qty2",str("sppq2")),unsafe_allow_html=True)
        
    # st.markdown("___")
    st.write("""<div style='text-align:center;font-size:1.5rem;font-weight:bold;padding-top:1.5rem;'><u>FTP And Reported Rejection</u></div>""",unsafe_allow_html=True)
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

if __name__ == "__main__":
    main()