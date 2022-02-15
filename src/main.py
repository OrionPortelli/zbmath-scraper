from scraper import Scraper
import api_client as apy
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


if __name__ == "__main__":
    json_test()
