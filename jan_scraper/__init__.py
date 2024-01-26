"""
jan_scraper: interact with Jan.ai by sending messages and retrieving the response

"https://github.com/AstraBert/jan-scraper"
"""


#Version
__version__ = "0.0.2b0"


##Errors
class UnableToFindLocationError(Exception):
    """Raise exception if jan_scraper is not installed correctly"""
    def __init__(self):
        pass

class MayActivateOnlyOneModelWarning(Warning):
    """Raise warning if API activation is automatized: may only activate one of the models you have installed, and it may not be your desired one"""

