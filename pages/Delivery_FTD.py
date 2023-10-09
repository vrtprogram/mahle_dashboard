from methods.main import layout, OTIF_sale, current_updates, critcal_customer_pdi

layout("Delivery FTD")

def main():
    current_updates()
    OTIF_sale()
    critcal_customer_pdi()

if __name__ == "__main__":
    main()