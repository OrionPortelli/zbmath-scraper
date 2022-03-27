from src.api import api_client
from src.api.json_builder import JsonBuilder

from lxml import etree
import requests
import json
import time

# Constants
TAG_PREFIX = "{http://www.openarchives.org/OAI/2.0/}" # zbMATH API tag prefix
OAI_DC_TAG = "{http://purl.org/dc/elements/1.1/}" # zbMATH API OAI_DC tag prefix
ID_PREFIX = len("oai:zbmath.org:") # Num characters before an identifier
GET_RECORD_PREFIX = f"{api_client.API_ROOT}GetRecord&identifier=oai:zbmath.org:"

def getIdentifiers(outpath="data/ids.json", set=None, start=None, end=None, verbose=True):
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

    Returns:
        The number of ID's collected
    """
    # Lambda function to disable printing when verbosity is False
    vprint = print if verbose else lambda *a, **k: None
    vprint("Collecting ID's:")
    t = time.perf_counter()
    
    # Build zbMATH API request base url
    req_url = (
        f"{api_client.API_ROOT}ListIdentifiers&metadataPrefix=oai_dc"
        + (f"&set={set}" if set else "")
        + (f"&from={start}" if start else "")
        + (f"&until={end}" if end else "")
    )
   
    with JsonBuilder(outpath) as out:
        # Request XML of first page
        xml = requests.get(req_url).content
        root = etree.fromstring(xml)[2]
        
        # Setup & populate JSON file with metadata
        count = api_client.count(root)
        out.format_ids(set, start, end, count)

        # Get first page ID's & write to file
        ids = []
        token = root[-1].text if root[-1].tag == f"{api_client.TAG_PREFIX}resumptionToken" else None
        for i in range(len(root) - 1):
            ids.append(int(root[i][0].text[ID_PREFIX:]))
        out.add_ID_page(ids)

        # Collect ID's from subsequent pages
        while token:
            ids = []
            xml = requests.get(req_url + f"&resumptionToken={token}").content
            root = etree.fromstring(xml)[2]

            token = root[-1].text if root[-1].tag == f"{api_client.TAG_PREFIX}resumptionToken" else None
            for i in range(len(root) - 1):
                ids.append(root[i][0].text[ID_PREFIX:])
            out.add_ID_page(ids)

        # Append final ID & close
        out.add_ID(root[-1][0].text[ID_PREFIX:])
        out.close()
    vprint(f"\tCollected {count} ID's in {time.perf_counter() - t:.2f}s")
    return count

def scrapeRecords(inpath, outpath="data/records.json", limit=1990, verbose=True):
    """
    Scrapes key information from all records in the input file and writes it to
    a json file.

    Args:
        inpath: String input filepath of JSON file with record ID's
        outpath: String output filepath
        limit: Integer limit on the number of records scraped (for rate limit avoidance)

    Returns:
        True if all records were scraped, False if the limit was reached.
    """
    # Lambda function to disable printing when verbosity is False
    vprint = print if verbose else lambda *a, **k: None
    vprint("Scraping records:")
    t = time.perf_counter()
    limitReached = False # True if limit reached before scraping all records

    with open(inpath) as j:
        ids = json.load(j)
    
    with JsonBuilder(outpath) as out:
        # Setup output file
        out.format_records(ids['set'], ids['start'], ids['end'], ids['count'])

        # Scrape first & write w/o preceding comma:
        record = api_client.getRecord(ids['identifiers'][0])
        out.add_record(json.dumps(record))
        
        # Scrape & write remaining records
        i = 0
        for id in ids['identifiers'][1:]:
            # Debug print every 250 ID's
            i += 1
            if verbose and i % 250 == 0:
                print(f"Scraped: {i}/{ids['count']}")
            if limit and i >= limit:
                limitReached = True
                break

            # Scrape record
            record = api_client.getRecord(id)
            record['id'] = id # Set ID manually as failsafe
            out.add_comma()
            out.add_record(json.dumps(record))
    vprint(f"\tScraped {i} records in {time.perf_counter() - t:.2f}s")
    return not limitReached

def continueScrape(idpath, recordpath, limit=1990, verbose=True):
    """
    Given a complete list of ID's and an incomplete list of records,
    continues scraping missing records.

    Args:
        idpath: String filepath for the complete list of record ID's
        recordpath: String filepath for the incomplete list of records (output written here)
        limit: Integer limit on the number of records scraped (for rate limit avoidance)
        verbose: Boolean determining whether to print debug statements

    Returns:
        True if all records were scraped, False if the limit was reached.
    """
    # Lambda function to disable printing when verbosity is False
    vprint = print if verbose else lambda *a, **k: None
    vprint("Continuing scraping records:")
    t = time.perf_counter()
    limitReached = False # True if limit reached before scraping all records
    
    # Load ID's & existing records
    with open(idpath) as j:
        ids = set(json.load(j)['identifiers'])
    with open(recordpath) as j:
        records = json.load(j)

    # Use set of scraped ID's to find the remaining ones
    scraped_ids = {r['id'] for r in records['records']}
    remaining = ids - scraped_ids

    
    with JsonBuilder(recordpath) as out:
        # Setup output file
        out.format_continue(json.dumps(records))

        # Scrape & write remaining records
        i = 0
        for id in remaining:
            # Debug print every 250 ID's
            i += 1
            if verbose and i % 250 == 0:
                print(f"Scraped: {i}/{len(remaining)}")
            if limit and i >= limit:
                limitReached = True
                break

            # Scrape record
            record = api_client.getRecord(id)
            record['id'] = id # Set ID manually as failsafe
            out.add_comma()
            out.add_record(json.dumps(record))
    vprint(f"\tScraped {i} records in {time.perf_counter() - t:.2f}s")
    return limitReached

def fullCollect(idpath, recordpath, set=None, start=None, end=None):
    """
    The complete record scraping pipeline. Collects ID's, then scrapes records.
    Additionally, uses advanced techniques to avoid the request limit and allow
    scraping of the full collection of records.

    Args:
        idpath: String filepath for the complete list of record ID's
        recordpath: String filepath for the incomplete list of records (output written here)
        limit: Integer limit on the number of records scraped (for rate limit avoidance)
    """
    API_LINK = "https://oai.zbmath.org/"

    # Collect ID's
    count = getIdentifiers(outpath=idpath, set=set, start=start, end=end)

    # Scrape first batch of records
    print('Scraping records')
    t = time.perf_counter()
    complete = scrapeRecords(inpath=idpath, outpath=recordpath, verbose=False)
    
    # Repeat the rate limit skip until all records scraped
    i = 1
    while not complete:
        print(f'Scraped {1990 * i}/{count}')
        # Trigger 600/min request limit on API (overrides 2000/day limit)
        requests.get(API_LINK)

        # Wait out limit
        time.sleep(180)
        requests.get(API_LINK) # Fail that resets cooldown
        requests.get(API_LINK).text[0:10] # Check it worked
        complete = continueScrape(idpath=idpath, recordpath=recordpath, verbose=False)
        i += 1
    
    print(f"Scraped {count}/{count} records in {time.perf_counter() - t:.2f}s")

def cleanDataset(inpath, outpath):
    """
    Cleans the date and language fields of a set of records using the zbMATH API.

    Args:
        inpath: String filepath for the complete list of dirty input records
        outpath: String filepath for the output list of cleaned records
    """
    print("Cleaning record dates & languages:")
    t = time.perf_counter()

    # Load scraped records
    with open(inpath) as j:
        records = json.load(j)

    with JsonBuilder(outpath) as out:
        # Setup output file
        out.format_records(records['set'], records['start'], records['end'], records['count'])

        # Write first record without preceeding comma
        r = cleanRecord(records['records'][0])
        out.add_record(json.dumps(r))

        # Iterate over records to retrieve fields
        i = 0
        for r in records['records'][1:]:
            i += 1
            if i % 500 == 0:
                print(f"Cleaned {i}/{records['count']}")
            
            # Create request URL using prefix template
            r = cleanRecord(r)
            out.add_comma()
            out.add_record(json.dumps(r))
    print(f"Cleaned {records['count']} records in {time.perf_counter() - t:.2f}s")

def cleanRecord(record):
    """
    Helper function for cleanDataset which cleans an individual records by
    getting the correct date and language fields using the zbMATH API.

    Args:
        record: Dictionary record to be cleaned
    """
    DISCLAIMER = "zbMATH Open Web Interface contents unavailable due to conflicting licenses."
    req_url = f"{GET_RECORD_PREFIX}{record['id']}&metadataPrefix=oai_dc"
    xml = requests.get(req_url).content
    root = etree.fromstring(xml)[2][0][1][0]
    record['date'] = int(root.find(f"{OAI_DC_TAG}date").text)
    lang = root.find(f"{OAI_DC_TAG}language").text
    if lang != DISCLAIMER:
        record['language'] = root.find(f"{OAI_DC_TAG}language").text
    #elif len(record['language']) > 20:
    #    lang = record['language']
    #    record['language'] = lang[:lang.index('\n')]
    return record
