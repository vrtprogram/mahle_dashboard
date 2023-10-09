from methods.main import layout, productivity_oee, raw_metarial, current_updates

layout("Cost FTD")

def main():
    current_updates()
    
    productivity_oee()

    raw_metarial()

if __name__ == "__main__":
    main()