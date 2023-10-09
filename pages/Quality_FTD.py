from methods.main import layout, customer_complaint_psp, ftp_rejection, current_updates

layout("Quality FTD")

def main():

    current_updates()

    customer_complaint_psp()

    ftp_rejection()

if __name__ == "__main__":
    main()