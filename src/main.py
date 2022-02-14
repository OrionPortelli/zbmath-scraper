from scraper import Scraper
import requests
import api_client as apy

# Test file for functions for now
TEST_RECORDS = [5797851, 7367256]

def scraper_test(link):
    s = Scraper(link)

    print("Software:", s.getSoftware())
    print("MSC:", s.getMSC())
    print("Date:", s.getDate())
    print("Language:", s.getLanguage())
    print("DE Number:", s.getDENumber())

if __name__ == "__main__":
    #print(apy.getClasses())
    print("RECORD:", apy.getRecord(TEST_RECORDS[1]))
    print("COUNT:", apy.getIDCount(msc="05", start="2020-01", end="2020-02"))
