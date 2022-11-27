import re


class Page:

    __slots__ = ["__page", "__links", "__n_pages"]

    def __init__(self, page):
        self.__page = page
        self.__links = [
            re.search(r'.+html', result.get("href")[2:]).group(0)
            for result in page.findAll("a", class_="_1lP57 _2f4Ho")
        ]
        self.__n_pages = None

    def get_page(self):
        return self.__page

    def get_links(self):
        return self.__links

    def get_n_pages(self):
        if self.__n_pages is None:
            self.__n_pages = int(
                re.search(
                    r"\d+", self.__page.find("span", class_="total-page").text
                ).group(0)
            )
        return self.__n_pages
