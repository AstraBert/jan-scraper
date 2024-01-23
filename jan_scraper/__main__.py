"""
jan_scraper: interact with Jan.ai by sending messages and retrieving the response

"https://github.com/AstraBert/jan-scraper"
"""

import sys


try:
    import pyautogui
except Exception as e:
    print(f"An error occured: {e}", file=sys.stderr)
finally:
    try:
        from jan_scraper.scraper import scrape_jan
    except Exception as e:
        print(f"An error occured: {e}", file=sys.stderr)

