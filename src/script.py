#!/usr/bin/env python3

import py_client as pyc

sets = {'05', '11', '20', '62', '65'}
start = '2010'
end = '2015'

for s in sets:
    print(f"Collecting ID's for set {s}")
    pyc.getIdentifiers(outpath=f'data/{s}_ids.json', set=s, start=start, end=end)
    print(f"Scraping Records for set {s}")
    pyc.scrapeRecords(inpath=f'data/{s}_ids.json', outpath=f'data/{s}_records.json')
