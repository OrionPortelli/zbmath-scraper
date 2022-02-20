from scraper import Scraper
import api_client as api
import py_client
from json_builder import JsonBuilder

# Test file for functions for now
TEST_RECORDS = [5797851, 7367256]

def scraper_test(link):
    s = Scraper(link)

    print("Software:", s.getSoftware())
    print("MSC:", s.getMSC())
    print("Date:", s.getDate())
    print("Language:", s.getLanguage())
    print("DE Number:", s.getDENumber())

def json_test():
    with JsonBuilder("data/test.json") as out:
        tester = ["11111111", "11111112", "11111113", "11111114"]
        out.format_ids('005', '2020-01', '2020-02', '749')
        out.add_ID_page(tester)
        out.add_ID("1234567")
        out.close()


def client_test_multipage():
    py_client.getIdentifiers(outpath="data/multipage.json", set='05', start='2020-02-01', end='2020-02-14')

def client_test_onepage():
    py_client.getIdentifiers(outpath="data/onepage.json", set='05', start='2020-01-01', end='2020-01-04')

if __name__ == "__main__":
    client_test_multipage()
    client_test_onepage()
