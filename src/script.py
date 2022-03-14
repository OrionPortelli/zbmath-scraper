#!/usr/bin/env python3

import py_client as pyc

sets = {'05', '11', '20', '62', '65'}
start = '2010-01'
end = '2010-02'

for s in sets:
    print(f"Scraping ID's for set {s}")
    pyc.getIdentifiers(outpath=f'data/{s}_ids.json', set=s, start=start, end=end)
    pyc.scrapeRecords(inpath=f'data/{s}_ids.json', outpath=f'data/{s}_records.json')