from scraper import Scraper
import requests
from lxml import etree

# Test file for functions for now

def scraper_test(link):
    s = Scraper(link)

    print("Software:", s.getSoftware())
    print("MSC:", s.getMSC())
    print("Date:", s.getDate())
    print("Language:", s.getLanguage())
    print("DE Number:", s.getDENumber())

def no_software_test(link):
    s = Scraper(link)
    print(s.getInfoJSON())

if __name__ == "__main__":
    no_software_test("https://zbmath.org/?q=an%3A7465767")
    