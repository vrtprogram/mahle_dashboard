"""
This is the property of VR Technologies please take permission before redistribution.
Author@ Swapnil Diwakar
EmailId@ Diwakarswapnil@gmail.com
Date@ 13/07/23

"""

from methods.main import layout, unsafe_incident_tracking

# import json
# from streamlit_lottie import st_lottie


# -------------------------------------------------
# print(df.columns)
# -------------------- Setting Up Page layout --------------------------#
layout("Unsafe Incidences Tracking")

def main():
    unsafe_incident_tracking()
    pass

if __name__ == "__main__":
    main()
