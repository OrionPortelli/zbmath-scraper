from scraper import Scraper
import api_client as api
import py_client as py
from json_builder import JsonBuilder

def exec():
    """Basic command line interface for users to user the scraper (filters required)"""
    print("|--------------------------------|")
    print("|PYTHON DATA COLLECTION INTERFACE|")
    print("|--------------------------------|")
    print("\t1. Collect ID's")
    print("\t2. Scrape Records")
    print("\t3. Collect ID's then scrape the records")
    choice = int(input("Enter option: "))

    match choice:
        # Collect ID's
        case 1:
            print("\nCOLLECTING ID'S")
            outpath=input("ID Output Filepath: ")
            set=input("Set: ")
            start=input("Start: ")
            end=input("End: ")
            py.getIdentifiers(outpath=outpath, set=set, start=start, end=end)
        # Scrape Records
        case 2:
            print("\nSCRAPING RECORDS")
            inpath=input("ID Input Filepath: ")
            outpath=input("Record Output Filepath: ")
            py.scrapeRecords(inpath=inpath, outpath=outpath)
            print("ID's collected")
        # Both
        case 3:
            print("\nCOLLECTING ID'S")
            inpath=input("ID Output Filepath: ")
            set=input("Set: ")
            start=input("Start: ")
            end=input("End: ")
            py.getIdentifiers(outpath=inpath, set=set, start=start, end=end)

            print("\nSCRAPING RECORDS")
            outpath=input("Record Output Filepath: ")
            py.scrapeRecords(inpath=inpath, outpath=outpath)
        case _:
            print("Invalid choice, exiting")

if __name__ == "__main__":
    exec()
