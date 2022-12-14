import re
from library.converter import convert


class Product:
    """
    Dataclass for Product
        Attributes:
            id
            aliexpress_id
            link
            title
            rating
            n_reviews
            n_orders
            price_usd
            price_ils
            category_id
    """

    def __init__(self, url, soup):
        """
        Init product and sets attributes from BeautifulSoup soup
        """
        self.id = None
        self.category_id = None
        self.aliexpress_id = re.search(r"item/.+html", url).group(0)[
            5:-5
        ]  # remove "item/" and ".html"
        self.link = url
        self.title = soup.find("h1", class_="product-title-text").text.replace('"', '')

        # If there is no rating, it is not displayed on the product page
        if (rating := soup.find("span", class_="overview-rating-average")) is not None:
            self.rating = rating.text
        else:
            self.rating = "NULL"

        # If there are no reviews, they are not displayed on the product page
        if (
            n_reviews := soup.find(
                "span", {"exp_page": "detail_page", "exp_type": "reviews"}
            )
        ) is not None:
            self.n_reviews = re.search(
                r"\d+",
                n_reviews.text,
            ).group(0)
        else:
            self.n_reviews = 0

        # If there are no orders, they are not displayed on the product page
        if (n_orders := soup.find("span", class_="product-reviewer-sold")) is not None:
            self.n_orders = re.search(r"\d+", n_orders.text).group(0)
        else:
            self.n_orders = 0

        # Prices can be in different classes
        def get_price(html_tag):
            """Returns price as a float from html"""
            return re.search(r"\d+[\.,]\d+", html_tag.text).group(0).replace(",", ".")

        if (price := soup.find("span", class_="uniform-banner-box-price")) is not None:
            self.price_usd = get_price(price)
            self.price_ils = convert(self.price_usd)
        elif (price := soup.find("span", class_="product-price-value")) is not None:
            self.price_usd = get_price(price)
            self.price_ils = convert(self.price_usd)
        else:
            self.price_usd = "NULL"
            self.price_ils = "NULL"
