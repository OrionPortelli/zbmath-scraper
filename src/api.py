from flask import Flask
from flask_restful import Api, Resource
from scraper import Scraper

app = Flask(__name__)
api = Api(app)

ROOT = "https://zbmath.org/?q=an:"

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

    # Currently returns entire text string of xml from API call
    # ID is DE number for the record, not the Zbl code
class Records(Resource):
    """Resource for retrieving zbMATH records via webscraping"""
    def get(self, id):
        """Retrieves the key fields from a given zbMATH record
        
        Args:
            id: The DE number of the record in question (Zbl code also accepted)
        
        Returns: JSON serializable dictionary representation of the records key fields
        """
        s = Scraper(f'{ROOT}{id}')
        return s.getInfoJSON()

api.add_resource(HelloWorld, '/')
api.add_resource(Records, '/records/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)