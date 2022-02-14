from scraper import Scraper
import requests
from lxml import etree

RECORD_ROOT = "https://zbmath.org/?q=an:"
API_ROOT = "https://oai.zbmath.org/v1/?verb="

def getRecord(id):
    """Retrieves the main fields from a given zbMATH record
    
    Args:
        id: The DE number of the record in question
    
    Returns: JSON serializable dictionary representation of the records key fields
    """
    s = Scraper(f'{RECORD_ROOT}{id}')
    return s.getInfoJSON()

def getClasses():
    """Retrives all available 2 digit MSC codes on zbMATH"""
    print("Collecting MSC codes")
    PAGES = 7 # 64 MSC codes and 10 per request (page)
    classes = {}
    for i in range(PAGES):
        if i == 0:
            xml = requests.get(f"{API_ROOT}ListSets").content
        else:
            xml = requests.get(f"{API_ROOT}ListSets&resumptionToken={token}").content
        root = etree.fromstring(xml)
        sets = root[2]

        for j in range(len(sets)-1):
            s = sets[j]
            classes[s[0].text] = s[1].text[6:]

        token = sets[-1].text 
        print(f"\tPage {i+1} complete")
    # Add the last item on the last page
    s = sets[-1]
    classes[s[0].text] = s[1].text[4:]

    return classes

def getIDCount(msc=None, start=None, end=None):
    """Retrieves the integer number of records that satisfy the given filters"""
    # Build zbMATH API request url
    req_url = (
        f"{API_ROOT}ListIdentifiers&metadataPrefix=oai_dc"
        + (f"&set={msc}" if msc else "")
        + (f"&from={start}" if start else "")
        + (f"&until={end}" if end else "")
    )

    # Request & parse XML 
    xml = requests.get(req_url).content
    root = etree.fromstring(xml)
    count = root[2][-1].get('completeListSize')

    return count
