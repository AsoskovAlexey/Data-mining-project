from library.global_functions import read_configuration
from library.logger import Logger, add_brackets, get_human_readable_time
from database.database_driver import MySQL
from library.scraper import create_default_scraper
from library.category import get_category_id, get_id_from_response
from library.page import Page
from library.product import Product
import database.database_query_generator as dqg
import time


def scrape_product(url, retries=3):
    """
    Tries to scrape a product with scroll_pause_time=0
    Increases the scroll_pause_time variable each unsuccessful attempt by 1 second
    """
    scroll_pause_time = scraper.scroll_pause_time
    scraper.scroll_pause_time = 0  # 0: instant scrolling
    for i in range(retries):
        try:
            product = Product(url, scraper.get_page(url))
            scraper.scroll_pause_time = scroll_pause_time
            return product
        except AttributeError as e:
            if i == retries - 1:  # -1: range does not include "stop"
                raise Exception(f"Unable to scrape product: {url}\nError: {e}")
            else:
                scraper.scroll_pause_time += (
                    1  # increases pause time between scrolls by 1 second
                )


def insert_product_data(product):
    """
    Inserts a new product data into the database.
    Updates the prices if the product is already exists
    """
    query = dqg.get_product_id(product.aliexpress_id)

    response = db.pull(query)
    if not response:
        db.push(dqg.add_product(product))
        response = db.pull(query)

    product.id = get_id_from_response(response)
    db.push(dqg.add_price(product))


def initialize_all(display_log=True):
    """
    Initializes logger, database_driver and scraper

    Args:
        display_log (bool, optional): if True, duplicates the logs to the console. Defaults to True.

    Returns:
        initialized logger, database_driver and scraper
    """
    configuration = read_configuration()

    # Logger initialization
    logger = Logger(display_log=display_log)

    # Database driver initialization
    database_driver = MySQL(configuration["database"])
    database_driver.use_database(configuration["database"]["database_name"])

    # Scraper initialization
    scraper = create_default_scraper()

    return logger, database_driver, scraper


def get_n_pages(category_url):
    """Returns the number of pages in the given category"""
    page_with_products = Page(scraper.get_page(category_url))
    try:
        return page_with_products.get_n_pages()
    except AttributeError:
        message = "Unable to get page, please try again later"
        logger.write_error_log(message)
        raise Exception(message)


def process_product(product_url):
    """Gets the product data and inserts it into the database"""
    global product_number, n_errors

    try:
        product = scrape_product(product_url)
        product.category_id = category_id
        insert_product_data(product)
        product_number += 1
        logger.write_log(f"Product #{product_number}\tid: {product.id}")
    except Exception as e:  # Global exception, catches all unexpected errors and writes them to the error_log
        n_errors += 1
        logger.write_error_log(
            f"Error #{n_errors}, {get_human_readable_time(time.time())}\nURL: {product_url}\nError: {e}"
        )


def process_page(current_url, page):
    """Gets products from the page, gets product data for each product and inserts it into the database"""
    global total_products_scraping_time
    page_with_products = Page(scraper.get_page(current_url))
    page_start_time = time.time()
    logger.write_log(
        add_brackets(
            f"Scraping from page #{page} started, {get_human_readable_time(page_start_time)}"
        )
    )
    for product_url in page_with_products.get_links():
        process_product(product_url)

    page_scraping_time = time.time() - page_start_time
    total_products_scraping_time += page_scraping_time
    logger.write_log(
        add_brackets(
            f"Scraping from page #{page} ended in: {page_scraping_time:.2f} seconds, average time: {(total_products_scraping_time / page):.2f} seconds"
        )
    )


def start_engine(category_url, title, display_log=True):

    """
    Gets products from the category and inserts them into database
    """
    # Initialization
    global logger, db, scraper, category_id, product_number, total_products_scraping_time, n_errors
    logger, db, scraper = initialize_all(display_log=display_log)

    # Start
    category_start_time = time.time()
    logger.write_log(
        add_brackets(
            f'Scraping from category "{title}" started, {get_human_readable_time(category_start_time)}'
        )
    )

    category_id = get_category_id(category_url, title, db)
    #n_pages = get_n_pages(category_url)
    n_pages = 60 # ! HOTFIX. TODO: Update according to changes on aliexpress

    # Counters
    product_number = 0
    total_products_scraping_time = 0
    n_errors = 0

    for page in range(1, n_pages + 1):
        current_url = category_url + f"?&page={page}"
        process_page(current_url, page)

    logger.write_log(
        add_brackets(
            f"Scraping from category ended in: {(time.time() - category_start_time):.2f} seconds"
        )
    )
