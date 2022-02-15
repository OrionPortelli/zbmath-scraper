import api_client as apy
from json_builder import JsonBuilder
from lxml import etree
import requests

TAG_PREFIX = "{http://www.openarchives.org/OAI/2.0/}" # zbMATH API tag prefix
ID_PREFIX = len("oai:zbmath.org:") # Num characters before an identifier

def getIdentifiers(outpath="data/ids.json", set=None, start=None, end=None):
    """
    Writes all DE numbers for zbMATH records with the given filters to the
    specified file.

    Args:
        outpath: String output filepath
        set: String MSC set code to filter ID's by
        start: String start date of filtering range (format 1970-01-01T00:00:00Z)
        end: String end date of filtering range (format 1970-01-01T00:00:00Z)
    """
    # Build zbMATH API request base url
    req_url = (
        f"{apy.API_ROOT}ListIdentifiers&metadataPrefix=oai_dc"
        + (f"&set={set}" if set else "")
        + (f"&from={start}" if start else "")
        + (f"&until={end}" if end else "")
    )
   
    with JsonBuilder as out:
        # Request XML of first page
        xml = requests.get(req_url).content
        root = etree.fromstring(xml)[2]

        # Get first page ID's
        ids = []
        token = root[-1].text if root[-1].tag == f"{TAG_PREFIX}resumptionToken" else None
        for i in range(len(root) - 1):
            ids.append(int(root[i][0].text[ID_PREFIX:]))

        # Collect ID's from subsequent pages
        degub = 1
        while token:
            print("page =", degub)
            xml = requests.get(req_url + f"&resumptionToken={token}").content
            root = etree.fromstring(xml)[2]
            for i in range(len(root) - 1):
                ids.append(int(root[i][0].text[ID_PREFIX:]))
            token = root[-1].text if root[-1].tag == f"{TAG_PREFIX}resumptionToken" else None
            degub += 1
        print("escaped loop")

        # Append final ID
        ids.append(int(root[-1][0].text[ID_PREFIX:]))

        res = {'start' : start, 'end' : end, 'ids' : ids}
        return res
