from page_scraper import Scraper
from page import Page
from product import Product
from db import MySQL
import db_creation_script
from global_functions import read_json
from global_variables import Constants
import time


def append_error_log(log, error_log_file):
    """Appends an error log"""
    print(log)
    with open(error_log_file, "a") as file:
        file.write(log + "\n")


def print_log(log, bracket="="):
    """Prints the log in an easy-to-read format"""
    bracket_multiplier = len(log)
    print("\n", bracket * bracket_multiplier, sep="")
    print(log)
    print(bracket * bracket_multiplier, "\n", sep="")


def scrape_product(url, scraper, retries=3):
    """
    Tries to scrape a product with scroll_pause_time=0
    Increases the variable each unsuccessful attempt by 1 second
    """
    scroll_pause_time = scraper.scroll_pause_time
    scraper.scroll_pause_time = 0
    for i in range(retries):
        try:
            product = Product(url, scraper.get_page(url))
            scraper.scroll_pause_time = scroll_pause_time
            return product
        except Exception as e:
            if i < retries - 1:
                raise Exception
            else:
                scraper.scroll_pause_time += 1


def main():

    """
    Gets products from 1st page and inserts them into database
    """

    main_start_time = time.time()
    print_log(f"Main function started: {time.asctime(time.localtime(main_start_time))}")

    # NOTE: url and categories are hardcoded, but will be replaced in the future.
    category_url = "https://www.aliexpress.com/category/708042/cpus.html"
    category = 0

    # Database initialization
    db = MySQL(read_json(Constants.DB_CONFIG_FILE))
    db_creation_script.start(mode="skip")
    db.push(f"USE {Constants.DB_NAME};")

    # Scraper initialization
    scraper_initialization_start_time = time.time()
    print_log(
        f"Scraper initialization started: {time.asctime(time.localtime(scraper_initialization_start_time))}"
    )
    scraper = Scraper(silent_mode=True, scroll_pause_time=0)
    scraper.get_page(Constants.URL_404)
    scraper.add_cookies(read_json(Constants.COOKIES_FILE))
    scraper.scroll_pause_time = 1
    print_log(
        f"Scraper initialization ended in: {round(time.time() - scraper_initialization_start_time, 2)} seconds"
    )

    page_with_products = Page(scraper.get_page(category_url))
    n_pages = page_with_products.get_n_pages()

    category_start_time = time.time()
    print_log(
        f"Scraping from category started: {time.asctime(time.localtime(category_start_time))}"
    )

    product_number = 0
    total_time = 0
    n_errors = 0
    for page in range(1, n_pages + 1):
        current_url = category_url + f"?&page={page}"
        page_with_products = Page(scraper.get_page(current_url))
        page_start_time = time.time()
        print_log(
            f"Scraping from page #{page} started: {time.asctime(time.localtime(page_start_time))}"
        )
        for product_url in page_with_products.get_links():
            try:
                product = scrape_product(product_url, scraper)
                db.push(
                    f'REPLACE INTO products (id, link, title, rating, n_reviews, n_orders, price, category_id)\
                    VALUES ({product.id}, "{product.link}", "{product.title}", {product.rating}, {product.n_reviews}, {product.n_orders}, {product.price}, {category});'
                )
                product_number += 1
                print(f"Product #{product_number}\tid: {product.id}")
            except Exception as e:
                n_errors += 1
                append_error_log(f"Error #{n_errors}, time: {time.asctime(time.localtime(time.time()))}\nURL: {product_url}\nError: {e}", Constants.ERROR_LOG_FILE)

        page_scraping_time = time.time() - page_start_time
        total_time += page_scraping_time
        print_log(
            f"Scraping from page #{page} ended in: {round(page_scraping_time, 2)} seconds, average time: {round(total_time / page, 2)} seconds"
        )

    print_log(
        f"Scraping from category ended in: {round(time.time() - category_start_time, 2)} seconds"
    )

    print_log(
        f"Main function ended in: {round(time.time() - main_start_time, 2)} seconds"
    )
    print_log(f"{time.asctime(time.localtime(time.time()))}")


if __name__ == "__main__":
    main()
