from scraper import Scraper
from lxml import etree
import requests

RECORD_ROOT = "https://zbmath.org/?q=an:"
API_ROOT = "https://oai.zbmath.org/v1/?verb="
TAG_PREFIX = "{http://www.openarchives.org/OAI/2.0/}"

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
    # Add the last item on the last page
    s = sets[-1]
    classes[s[0].text] = s[1].text[4:]

    return classes

def getIDCount(set=None, start=None, end=None):
    """Returns the integer number of records that satisfy the given filters
    
    Args:
        set: String MSC set code to filter ID's by
        start: String start date of filtering range (format 1970-01-01T00:00:00Z)
        end: String end date of filtering range (format 1970-01-01T00:00:00Z)

    Raises:
        ValueError: Bad arguments (invalid filters).
    """
    # Build zbMATH API request url
    req_url = (
        f"{API_ROOT}ListIdentifiers&metadataPrefix=oai_dc"
        + (f"&set={set}" if set else "")
        + (f"&from={start}" if start else "")
        + (f"&until={end}" if end else "")
    )

    # Request & parse XML 
    xml = requests.get(req_url).content
    root = etree.fromstring(xml)[2]

    return count(root)

def count(xml_root):
    """Returns the integer number of results from a zbMATH request (helper function)

    Args:
        xml_root: lxml etree containing the relevant portion of the request (3rd element)

    Raises: 
        ValueError: Bad arguments (invalid filters).
    """
    # Check for errors
    if xml_root.tag == f"{TAG_PREFIX}error":
        if xml_root.text == "noRecordsMatch":
            return 0
        raise ValueError("Bad argument (invalid filters).")

    # If multiple pages present, get count directly
    if xml_root[-1].tag == f"{TAG_PREFIX}resumptionToken":
        return int(xml_root[-1].get('completeListSize'))

    return len(xml_root)
