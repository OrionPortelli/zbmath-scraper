# CS4098 zbMath Analytics

Python wrapper for zbMATH API with additional web-scraping tools for swMATH. Composed of 3 main parts:


1. **API Client:** A Python client for the aforementioned REST api. All calls are RESTful and share match those in the above API.
2. **Python Client:** A non-REST API for python users to write data to a file
3. **Flask-RESTful API:** A REST api which can be hosted then used to make various requests.

## 1. API Client

A basic python facing client for RESTful access to zbMATH information. Contains the following function (detailed functionality in docstrings)

`getRecord(id)`
Retrieves the main fields from a given zbMATH record.

`getClasses()`
Retrives all available 2 digit MSC codes on zbMATH.

`getIDCount(set, start, end)`
Returns the integer number of records that satisfy the given filters.

## 2. Python Client
A non-REST python client API for mass collection of zbMATH data and writing to JSON files.

`getIdentifiers(outpath, set, start, end)`
Writes all DE numbers for zbMATH records with the given filters to the specified file.

`scrapeRecords(inpath, outpath)`
Scrapes key information from all records in the input file and writes it to a json file.

`continueScrape()`
TBC

## 3. REST API Documentation

### `GET /records/{id}`

**Description**

Retrieve the following data from a given zbMATH record

**Definition**

`GET records/{id}`

**Response**
```
{
    "id": "5797851",
    "software": {
        "554": "Mathematica"
    },
    "msc": [
        "35",
        "42",
        "34",
        "65",
        "33"
    ],
    "language": "English",
    "date": 2010
}
```

### `GET /classes`

**Description**

Retrieve all high level MSC classifications from zbMATH

**Definition**

`GET classes`

**Response**
```
{
    "00": "General and overarching topics; collections",
    "01": "History and biography",
    ...
    "97": "Mathematics education",
    "JFM": "Jahrbuch f\u00fcr Mathematik"
}
```

### `GET /identifiers`

**Description**

Retrieves the identifiers (DE numbers) of every record in the zbMATH database

(Can be used in conjunction with several filters to narrow results)

**Definition**

`GET identifiers`

**Parameters**

set \[Optional\] - Two digit MSC code or 'JFM'  
from \[Optional\] - Starting date for filter range (e.g. 1970-01-01T00:00:00Z)  
to \[Optional\] - End date for filter range (e.g. 2020-01-01T00:00:00Z)  

**Response**
```
{
    "ids": [
        0000001,
        0000002,
        ...
        9999999
    ]
}
```

### `GET /identifiers/count`

**Description**

Retrives the number of records in the zbMATH database matching the filters

**Definition**

`GET identifiers/count`

**Parameters**

set \[Optional\] - Two digit MSC code or 'JFM'  
from \[Optional\] - Starting date for filter range (e.g. 1970-01-01T00:00:00Z)  
to \[Optional\] - End date for filter range (e.g. 2020-01-01T00:00:00Z)  

**Response**
```
{
    "count": 4343756
}
```
