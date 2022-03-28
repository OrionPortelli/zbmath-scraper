#!/usr/bin/env python3
# Uses rate limit skip to collect all records in the desired filters
import src.api.py_client as py_client
sets = ['05']
start = '2010'
end = '2015'

# Collect records
for s in sets:
    #py_client.fullCollect(idpath=f'data/{s}_ids.json', recordpath=f'data/{s}_records.json', set=s, start=start, end=end)
    py_client.fullCollect(idpath=f'data/{s}_ids.json', recordpath=f'data/{s}_records.json', set=s, start=start, end=end, cont=True)

# Clean datasets
#for s in sets:
#    py_client.cleanDataset(inpath=f'data/{s}_records.json', outpath=f'data/{s}_clean.json', strict=False)
