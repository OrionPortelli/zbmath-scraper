from scraper import Scraper
import requests
import api_client

# Test file for functions for now

def scraper_test(link):
    s = Scraper(link)

    print("Software:", s.getSoftware())
    print("MSC:", s.getMSC())
    print("Date:", s.getDate())
    print("Language:", s.getLanguage())
    print("DE Number:", s.getDENumber())

if __name__ == "__main__":
    api_client 
    