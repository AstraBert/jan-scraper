"""
jan_scraper: interact with Jan.ai by sending messages and retrieving the response

"https://github.com/AstraBert/jan-scraper"
"""


#Version
__version__ = "0.0.1b1"


##Errors
class UnableToFindLocationError(Exception):
    """Raise exception if jan_scraper is not installed correctly"""
    def __init__(self):
        pass

