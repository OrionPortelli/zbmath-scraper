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

