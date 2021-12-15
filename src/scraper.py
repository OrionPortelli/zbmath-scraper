from bs4 import BeautifulSoup
import requests

class Scraper:
    """Scrapes information about a given record from its HTML
     
    Attributes:
        link: String link to the page of the record to be scraped
        soup: Beautiful Soup instance using HTML from the given link
        SOFT_LEN: Length of the link to software pages (used to find unique software num)
    """

    SOFT_LEN = len("https://swmath.org/software/")

    def __init__(self, link):
        """Makes a scraper for a record with the provided link"""
        self.link = link
        html = requests.get(link).text
        self.soup = BeautifulSoup(html, "lxml")

    def getSoftware(self):
        """Retrives a dict with the id and names of the software used for the Record"""
        software = self.soup.find("div", class_="software").find_all("a")
        return {s['href'][self.SOFT_LEN:] : s.text for s in software}

    def getMSC(self):
        """Returns a set with the base level MSC assigned to the Record"""
        classes = self.soup.find("div", class_="classification").find_all("a")
        return set([c.text[0:2] for c in classes])

    def getDate(self):
        """Returns the integer date the Record was published"""
        date = self.soup.find("a", title="Articles in this Issue")
        return int(date.text[-5:-1])

    def getLanguage(self):
        """Returns the language used in the Record"""
        lang = self.soup.find("div", class_="title").find("i")
        return lang.text[1:-1]

    def getInfoJSON(self):
        """Returns a JSON encodable object with all relevant information from the Record"""
        # TODO: Should this return the ID of the record (on principle)
        # TODO: If this should, would the aggregate "getAllRecords" not include IDs
        pass
