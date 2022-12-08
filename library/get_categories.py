from library.global_functions import create_default_scraper

scraper = create_default_scraper()
print(scraper.get_page("https://www.aliexpress.com/"))


