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

def msc_compact():
    PAGES = 7 # 64 MSC codes and 10 per request (page)

    classes = {}
    for i in range(PAGES):
        if i == 0:
            xml = requests.get("https://oai.zbmath.org/v1/?verb=ListSets").content
        else:
            xml = requests.get(f"https://oai.zbmath.org/v1/?verb=ListSets&resumptionToken={token}").content
        root = etree.fromstring(xml)
        sets = root[2]

        for j in range(len(sets)-1):
            s = sets[j]
            classes[s[0].text] = s[1].text[6:]

        token = sets[-1].text 
        print(f"Page {i+1} complete")
    # Add the last item on the last page
    s = sets[-1]
    classes[s[0].text] = s[1].text

if __name__ == "__main__":
    print(msc_compact())
    