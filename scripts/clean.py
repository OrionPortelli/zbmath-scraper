#!/usr/bin/env python3
# Cleans the dates from the specified file
from src.api.py_client import fullCollect, cleanDataset

set = '62'

input = f"data/{set}_records.json"
output = f"data/{set}_clean.json"

# Cleans a dirty date
cleanDataset(inpath=input, outpath=output, strict=False)
