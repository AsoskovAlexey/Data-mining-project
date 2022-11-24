import re
from bs4 import BeautifulSoup
import time

class Page():
    
    __slots__ = ["__page"]
    
    def __init__(self, page):
        self.__page = page
        time.sleep(1)
    
    def get_page(self):
        return self.__page
    
    def set_page(self, page):
        self.__page = page
    
    def get_links(self):
        return [result.get("href")[2:] for result in self.__page.findAll("a", class_="_1lP57 _2f4Ho")]
    
    def get_n_pages(self):
        return int(re.search(r'\d+', self.__page.find('span', class_="total-page").text).group(0))