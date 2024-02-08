"""
jan_scraper: interact with Jan.ai by sending messages and retrieving the response

"https://github.com/AstraBert/jan-scraper"
"""

# Version
__version__ = "0.1.0b1"


##Errors and Warnings
class UnableToFindLocationError(Exception):
    """Raise exception if jan_scraper is not installed correctly"""

    def __init__(self):
        pass


class MayActivateOnlyOneModelWarning(Warning):
    """Raise warning if API activation is automatized: may only activate one of the models you have installed, and it may not be your desired one"""


class Unrecognizable_Language_Warning(Warning):
    """Language provided is not among the ones supported by auto-detection... Switching to auto"""
