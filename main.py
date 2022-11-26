
from page_scraper import Scraper
from page import Page
import re


url = "https://www.aliexpress.com/category/708042/cpus.html?spm=a2g0o.home.104.5.650c2145wzJtZH"

scraper = Scraper(silent_mode=True, scroll_pause_time=2)

# Set language, country and currency
# NOTE: silent_mode must be set to False !!! Don't close the browser
#scraper.apply_page_settings(url)



# Debugging
page = Page(scraper.get_page(url))
    
print(page.get_links()[0])

