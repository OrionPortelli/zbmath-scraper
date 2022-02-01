from flask import Flask, request
from flask_restful import Api, Resource
from lxml import etree
import requests
from scraper import Scraper

app = Flask(__name__)
api = Api(app)

RECORD_ROOT = "https://zbmath.org/?q=an:"
API_ROOT = "https://oai.zbmath.org/v1/?verb="
TAG_PREFIX = "{http://www.openarchives.org/OAI/2.0/}" # Prefix of tags from zbMATH API
ID_PREFIX = len("oai:zbmath.org:") # Number of characters before a given identifier

# TODO: Record scraper can't handle records with no software
class Records(Resource):
    """Resource for retrieving zbMATH records via webscraping"""
    def get(self, id):
        """Retrieves the key fields from a given zbMATH record
        
        Args:
            id: The DE number of the record in question
        
        Returns: JSON serializable dictionary representation of the records key fields
        """
        s = Scraper(f'{RECORD_ROOT}{id}')
        return s.getInfoJSON()

# TODO: Handle first page not having a full list (never occurs)
class Classes(Resource):
    """Resource for retrieving available MSC codes using zbMATH api"""
    def get(self):
        """Retrives all available 2 digit MSC codes on zbMATH"""
        print("Collecting MSC codes")
        PAGES = 7 # 64 MSC codes and 10 per request (page)
        classes = {}
        for i in range(PAGES):
            if i == 0:
                xml = requests.get(f"{API_ROOT}ListSets").content
            else:
                xml = requests.get(f"{API_ROOT}ListSets&resumptionToken={token}").content
            root = etree.fromstring(xml)
            sets = root[2]

            for j in range(len(sets)-1):
                s = sets[j]
                classes[s[0].text] = s[1].text[6:]

            token = sets[-1].text 
            print(f"\tPage {i+1} complete")
        # Add the last item on the last page
        s = sets[-1]
        classes[s[0].text] = s[1].text[4:]

        return classes

class IdentifiersCount(Resource):
    """Resource for retrieving the number of zbMATH records with the given filter"""
    def get(self):
        """Retrieves the integer number of records that satisfy the given filters"""
        print("Retrieving identifiers quantity")

        # Retrieve query parameters (filters)
        msc = request.args.get('set', type = str)
        start = request.args.get('start', type = str)
        end = request.args.get('end', type = str)
        print(f"Filters:\n\tset={msc} | start={start} | end={end}")

        # Build zbMATH API request url
        req_url = (
            f"{API_ROOT}ListIdentifiers&metadataPrefix=oai_dc"
            + (f"&set={msc}" if msc else "")
            + (f"&from={start}" if start else "")
            + (f"&until={end}" if end else "")
        )

        # Request & parse XML to retrieve complete count 
        xml = requests.get(req_url).content
        root = etree.fromstring(xml)
        count = root[2][-1].get('completeListSize')

        return count

# TODO: Edge cases:
# TODO: Pages with 0 id's
# TODO: Pages with no resumption token
class Identifiers(Resource):
    """Resource for retrieving the all identifiers of zbMATH records given filters"""
    def get(self):
        """Retrieves all DE numbers for zbMATH records with the given filters"""
        print("Retriving identifiers")

        # Retrieve query parameters (filters)
        msc = request.args.get('set', type = str)
        start = request.args.get('start', type = str)
        end = request.args.get('end', type = str)
        print(f"Filters:\n\tset={msc} | start={start} | end={end}")

        # Build zbMATH API request base url
        req_url = (
            f"{API_ROOT}ListIdentifiers&metadataPrefix=oai_dc"
            + (f"&set={msc}" if msc else "")
            + (f"&from={start}" if start else "")
            + (f"&until={end}" if end else "")
        )

        # Request XML of first page
        xml = requests.get(req_url).content
        root = etree.fromstring(xml)[2]

        # Get first page ID's
        ids = []
        token = root[-1].text if root[-1].tag == f"{TAG_PREFIX}resumptionToken" else None
        for i in range(len(root) - 1):
            ids.append(int(root[i][0].text[ID_PREFIX:]))

        # Collect ID's from subsequent pages
        degub = 1
        while token:
            print("page =", degub)
            xml = requests.get(req_url + f"&resumptionToken={token}").content
            root = etree.fromstring(xml)[2]
            for i in range(len(root) - 1):
                ids.append(int(root[i][0].text[ID_PREFIX:]))
            token = root[-1].text if root[-1].tag == f'{TAG_PREFIX}resumptionToken' else None
            degub += 1
        print("escaped loop")

        # Append final ID
        ids.append(int(root[-1][0].text[ID_PREFIX:]))

        res = {'start' : start, 'end' : end, 'ids' : ids}
        return res
        
api.add_resource(Records, '/records/<int:id>')
api.add_resource(Classes, '/classes')
api.add_resource(IdentifiersCount, '/identifiers/count')
api.add_resource(Identifiers, '/identifiers')

if __name__ == "__main__":
    app.run(debug=True)
