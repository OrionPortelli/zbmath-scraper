#!/usr/bin/env python3
# Cleans the dates from the specified file
from src.api.py_client import fullCollect, cleanDataset

input = "data/11_records.json"
output = "data/11_clean.json"

# Cleans a dirty date
cleanDataset(inpath=input, outpath=output)
