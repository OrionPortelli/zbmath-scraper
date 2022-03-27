#!/usr/bin/env python3
# Module uses reset skip to collect all records in the desired filters
from api.py_client import fullCollect, cleanDataset

# Gets a dirty date
fullCollect(idpath='data/clean_id.json', recordpath='data/clean_record.json', set='20', start='2013-11-28', end='2013-11-30')

# Cleans a dirty date
#cleanDataset(inpath='data/clean_record.json', outpath='data/clean_record.json')
