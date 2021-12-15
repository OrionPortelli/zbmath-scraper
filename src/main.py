from scraper import Scraper
import requests

# Test file for functions for now

def scraper_test():
    s = Scraper("https://zbmath.org/?q=an:1200.35057")
    print("Software:", s.getSoftware())
    print("MSC:", s.getMSC())
    print("Date:", s.getDate())
    print("Language:", s.getLanguage())

def api_test1():
    BASE = 'http://127.0.0.1:5000/'

    response = requests.get(BASE + 'records/5797851')
    print(response.json())

def api_test2():
    BASE = 'http://127.0.0.1:5000/'

    response = requests.get(BASE)
    print(response.text)

def get(id):
    root = "https://oai.zbmath.org/v1/"
    response = requests.get(f'{root}?verb=GetRecord&identifier=oai:zbmath.org:{id}&metadataPrefix=oai_dc')
    return response

if __name__ == "__main__":
    #print(get(5797851).text)
    #api_test1()
    scraper_test()