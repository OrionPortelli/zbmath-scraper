from bs4 import BeautifulSoup
import requests
import re # Regex match date

class Scraper:
    """Scrapes information about a given record from its page HTML
     
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
        """Retrives a dict of all software cited in the Record
        
        Returns: A dict with the ID and name of all software used in the record, or None
        """
        try:
            root = self.soup.find("div", class_="software")
            # Check if the record contains software
            if root:
                software = root.find_all("a")
                return {s['href'][self.SOFT_LEN:] : s.text for s in software}
            return None
        except Exception as e:
            print(f"Exception scraping Software for {self.link}\n{e}")
            return None

    def getMSC(self):
        """Returns a set with the base level MSC assigned to the Record"""
        try:
            classes = self.soup.find("div", class_="classification").find_all("a")
            return set([c.text[0:2] for c in classes])
        except Exception as e:
            print(f"Exception scraping MSC for {self.link}\n{e}")
            return set([])

    def getDate(self):
        """Returns the integer year the Record was published"""
        try:
            # Try to get date from CITE popout
            date = self.soup.find("span", class_="tex2jax_ignore")
            if date:
                if re.match("(((20)[012]\d)|((19)\d{2}))", date.text[-21:-17]):
                    return int(date.text[-21:-17])
                else:
                    return int(date.text[-5:-1])
            # Otherwise try to find date using articles in the issue
            date = self.soup.find("a", title="Articles in this Issue")
            if date:
                if re.match("(((20)[012]\d)|((19)\d{2}))", date.text[-6:-2]):
                    return int(date.text[-6:-2])
                else:
                    return int(date.text[-5:-1])
            # Otherwise return no date found
            return None
        except Exception as e:
            print(f"Exception scraping Date for {self.link}\n{e}")
            return None

    def getLanguage(self):
        """Returns a string with the language used in the Record"""
        try:
            lang = self.soup.find("h2", class_="title").find("i")
            return lang.text[1:-1]
        except Exception as e:
            print(f"Exception scraping Language for {self.link}\n{e}")
            return None


    def getDENumber(self):
        """Returns the integer DE number ID of the Record"""
        # DE code grabbed directly from zbMath API call for XML content
        try:
            DE = (self.soup.find("div", class_="functions clearfix")
                .find("a", class_="xml"))
            return int(DE["href"][-7:])
        except Exception as e:
            print(f"Exception scraping DE Number for {self.link}\n{e}")
            return None

    def getInfoJSON(self):
        """Returns a JSON encodable object with all relevant information from the Record"""
        return {"id": self.getDENumber(), "software": self.getSoftware(), "msc": list(self.getMSC()),
            "language": self.getLanguage(), "date": self.getDate()}
