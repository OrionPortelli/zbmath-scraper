from flask import Flask
from flask_restful import Api, Resource
from lxml import etree
import requests
from scraper import Scraper

app = Flask(__name__)
api = Api(app)

RECORD_ROOT = "https://zbmath.org/?q=an:"
API_ROOT = "https://oai.zbmath.org/v1/?verb="

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

class Classes(Resource):
    """Resource for retrieving available MSC codes using zbMATH api"""
    def get(self):
        """Retrives all available 2 digit MSC codes on zbMATH"""
        print("Collecting MSC codes")
        PAGES = 7 # 64 MSC codes and 10 per request (page)
        classes = {}
        for i in range(PAGES):
            if i == 0:
                xml = requests.get("https://oai.zbmath.org/v1/?verb=ListSets").content
            else:
                xml = requests.get(f"https://oai.zbmath.org/v1/?verb=ListSets&resumptionToken={token}").content
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

api.add_resource(Records, '/records/<int:id>')
api.add_resource(Classes, '/classes')

if __name__ == "__main__":
    app.run(debug=True)