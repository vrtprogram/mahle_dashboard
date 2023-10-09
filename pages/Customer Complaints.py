from methods.main import layout, customer_complaint, complaint_trend

layout("Customer Complaints")

def main():
    customer_complaint()
    complaint_trend()
    
if __name__ == "__main__":
    main()