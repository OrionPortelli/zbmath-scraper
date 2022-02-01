# CS4098 zbMath Analytics

Python wrapper for zbMATH API with additional web-scraping tools for swMATH.

## REST API Documentation

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
