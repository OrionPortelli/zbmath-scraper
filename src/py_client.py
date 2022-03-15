import api_client as api
from json_builder import JsonBuilder
from scraper import Scraper
from lxml import etree
import requests
import json

import time

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

    Raises:
        ValueError: Bad arguments (invalid filters).
    """
    print("Collecting ID's:")
    t = time.perf_counter()
    
    # Build zbMATH API request base url
    req_url = (
        f"{api.API_ROOT}ListIdentifiers&metadataPrefix=oai_dc"
        + (f"&set={set}" if set else "")
        + (f"&from={start}" if start else "")
        + (f"&until={end}" if end else "")
    )
   
    with JsonBuilder(outpath) as out:
        # Request XML of first page
        xml = requests.get(req_url).content
        root = etree.fromstring(xml)[2]
        
        # Setup & populate JSON file with metadata
        count = api.count(root)
        out.format_ids(set, start, end, count)

        # Get first page ID's & write to file
        ids = []
        token = root[-1].text if root[-1].tag == f"{api.TAG_PREFIX}resumptionToken" else None
        for i in range(len(root) - 1):
            ids.append(int(root[i][0].text[ID_PREFIX:]))
        out.add_ID_page(ids)

        # Collect ID's from subsequent pages
        while token:
            ids = []
            xml = requests.get(req_url + f"&resumptionToken={token}").content
            root = etree.fromstring(xml)[2]

            token = root[-1].text if root[-1].tag == f"{api.TAG_PREFIX}resumptionToken" else None
            for i in range(len(root) - 1):
                ids.append(root[i][0].text[ID_PREFIX:])
            out.add_ID_page(ids)

        # Append final ID & close
        out.add_ID(root[-1][0].text[ID_PREFIX:])
        out.close()
    
    print(f"\tCollected {count} ID's in {time.perf_counter() - t:.2f}s")

def scrapeRecords(inpath, outpath="data/records.json"):
    """
    Scrapes key information from all records in the input file and writes it to
    a json file.

    Args:
        inpath: String input filepath of JSON file with record ID's
        outpath: String output filepath
    """
    print("Scraping records:")
    t = time.perf_counter()

    with open(inpath) as j:
        ids = json.load(j)
    
    with JsonBuilder(outpath) as out:
        # Setup output file
        out.format_records(ids['set'], ids['start'], ids['end'], ids['count'])
        
        # Scrape & write all records
        i = 0
        for id in ids['identifiers'][:-1]:
            # Debug print every thousand ID's
            i += 1
            if i % 500 == 0:
                print(f"Scraped: {i}/{ids['count']}")

            # Scrape record
            record = api.getRecord(id)
            record[id] = id # Set ID manually as failsafe
            out.add_record(json.dumps(record))
            out.add_comma()
        record = api.getRecord(ids['identifiers'][-1])
        out.add_record(json.dumps(record))

    print(f"\tScraped {ids['count']} records in {time.perf_counter() - t:.2f}s")
