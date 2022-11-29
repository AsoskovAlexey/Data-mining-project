import re
from bs4 import BeautifulSoup


class Product:
    """
    Dataclass for Product
        Attributes:
            id
            link
            title
            rating
            n_reviews
            n_orders
            price
    """

    def __init__(self, url, soup):
        """
        Init product and sets attributes from BeautifulSoup soup
        """
        self.id = re.search(r"item/.+html", url).group(0)[
            5:-5
        ]  # remove "item/" and ".html"
        self.link = url
        self.title = soup.find("h1", class_="product-title-text").text
        self.rating = soup.find("span", class_="overview-rating-average").text
        self.n_reviews = re.search(
            r"\d+",
            soup.find("span", {"exp_page": "detail_page", "exp_type": "reviews"}).text,
        ).group(0)
        self.n_orders = re.search(
            r"\d+", soup.find("span", class_="product-reviewer-sold").text
        ).group(0)
        self.price = re.search(
            r"\d+[\.,]\d+", soup.find("span", class_="uniform-banner-box-price").text
        ).group(0).replace(",", '.')
        print(self.price)
