#!/usr/bin/env python3

# Script for continuing to scrape records
import py_client as pyc

pyc.continueScrape(idpath='data/62_ids.json', recordpath='data/62_records.json', limit=1990)
