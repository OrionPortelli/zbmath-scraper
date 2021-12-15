from flask import Flask
from flask_restful import Api, Resource
import requests

app = Flask(__name__)
api = Api(app)

ROOT = "https://oai.zbmath.org/v1/"

class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

    # TODO: Find what fields are required, parse XML to get them
    # TODO: Learn how to use parameters, will I need to do everything in webscraping anyway?
    # Currently returns entire text string of xml from API call
    # ID is DE number for the record, not the Zbl code
class Records(Resource):
    # Returns a JSON object containing the article identifier, classifications, date, language
    # using the zbMATH API.
    # TODO: Make the default version of this use scraping, non-software version use lxml
    def get(self, id):
        response = requests.get(f'{ROOT}?verb=GetRecord&identifier=oai:zbmath.org:{id}&metadataPrefix=oai_dc')
        return response.text

api.add_resource(HelloWorld, '/')
api.add_resource(Records, '/records/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)