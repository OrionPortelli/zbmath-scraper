#!/usr/bin/env python3

# Script testing if API calls reset the limit
import py_client as pyc
import time
import requests

API_LINK = "https://oai.zbmath.org/"

# Run 1990 Requests (stop short of limit)
pyc.continueScrape(idpath='data/62_ids.json', recordpath='data/62_records.json', limit=1990)

# Trigger 600 request per minute limit on API, then wait for it to expire
print(requests.get(API_LINK).text)

time.sleep(180)

print(requests.get(API_LINK).text)
print("FAST FAIL")
print(requests.get(API_LINK).text[0:10])


# Scrape another 1990 requests
pyc.continueScrape(idpath='data/62_ids.json', recordpath='data/62_records.json', limit=1990)

# Repeat
