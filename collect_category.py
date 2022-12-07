from scraper import Scraper
from page import Page
from product import Product
from database.database_driver import MySQL
import database.database_creation_script as db_creation_script
from global_functions import read_json, read_configuration
from database.database_query_generator import create_product_query
from log.logger import Logger, add_brackets
import time


def get_human_readable_time(time):
    """Returns the human readable time"""
    return time.asctime(time.localtime(time))


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


def scrape_product(url, category, scraper, retries=3):
    """
    Tries to scrape a product with scroll_pause_time=0
    Increases the variable each unsuccessful attempt by 1 second
    """
    scroll_pause_time = scraper.scroll_pause_time
    scraper.scroll_pause_time = 0
    for i in range(retries):
        try:
            product = Product(url, category, scraper.get_page(url))
            scraper.scroll_pause_time = scroll_pause_time
            return product
        except AttributeError as e:
            if i < retries - 1:
                raise Exception(f"Unable to scrape product: {url}")
            else:
                scraper.scroll_pause_time += 1


def main():

    """
    Gets products from 1st page and inserts them into database
    """

    # Logger initialization
    logger = Logger()

    # NOTE: url and categories are hardcoded, but will be replaced in the future.
    category_url = "https://www.aliexpress.com/category/708042/cpus.html"
    category = 0

    configuration = read_configuration()

    # Database initialization
    db = MySQL(configuration["database"])
    db_creation_script.start(mode="force")
    db.use_database(configuration["database"]["database_name"])

    # Scraper initialization
    scraper_initialization_start_time = time.time()
    logger.write_log(
        add_brackets(
            f"Scraper initialization started: {get_human_readable_time(scraper_initialization_start_time)}"
        )
    )
    scraper = Scraper(silent_mode=True, scroll_pause_time=0)
    scraper.get_page(configuration["web"]["url"]["404_page"])
    scraper.add_cookies(read_json(configuration["web"]["cookies_file"]))
    scraper.scroll_pause_time = 1
    logger.write_log(
        add_brackets(
            f"Scraper initialization ended in: {time.time() - scraper_initialization_start_time:.2} seconds"
        )
    )

    page_with_products = Page(scraper.get_page(category_url))

    try:
        n_pages = page_with_products.get_n_pages()
    except AttributeError:
        print("Unable to get page, please try again later")
        return

    category_start_time = time.time()
    logger.write_log(
        add_brackets(
            f"Scraping from category started: {get_human_readable_time(category_start_time)}"
        )
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
                product = scrape_product(product_url, category, scraper)
                db.push(create_product_query(product))
                product_number += 1
                print(f"Product #{product_number}\tid: {product.id}")
            except Exception as e:
                n_errors += 1
                append_error_log(
                    f"Error #{n_errors}, {time.asctime(time.localtime(time.time()))}\nURL: {product_url}\nError: {e}",
                    configuration["error_log_file"],
                )

        page_scraping_time = time.time() - page_start_time
        total_time += page_scraping_time
        print_log(
            f"Scraping from page #{page} ended in: {round(page_scraping_time, 2)} seconds, average time: {round(total_time / page, 2)} seconds"
        )

    print_log(
        f"Scraping from category ended in: {round(time.time() - category_start_time, 2)} seconds"
    )


if __name__ == "__main__":
    main()
