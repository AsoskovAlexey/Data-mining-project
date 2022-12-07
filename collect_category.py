from page import Page
from product import Product
from database.database_driver import MySQL
from global_functions import read_configuration, create_default_scraper
from database.database_query_generator import create_product_query
from log.logger import Logger, add_brackets, get_human_readable_time
import time


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


def scrape_category(category_url, category_id, display_log=True):

    """
    Gets products from 1st page and inserts them into database
    """
    
    configuration = read_configuration()
    
    # Logger initialization
    logger = Logger(display_log=display_log)

    # Database driver initialization
    db = MySQL(configuration["database"])
    db.use_database(configuration["database"]["database_name"])

    # Scraper initialization
    scraper_initialization_start_time = time.time()
    logger.write_log(
        add_brackets(
            f"Scraper initialization started, {get_human_readable_time(scraper_initialization_start_time)}"
        )
    )
    scraper = create_default_scraper()
    logger.write_log(
        add_brackets(
            f"Scraper initialization ended in: {time.time() - scraper_initialization_start_time:.2} seconds"
        )
    )

    page_with_products = Page(scraper.get_page(category_url))
    try:
        n_pages = page_with_products.get_n_pages()
    except AttributeError:
        logger.write_error_log("Unable to get page, please try again later")
        return

    category_start_time = time.time()
    logger.write_log(
        add_brackets(
            f'Scraping from category "{category_url}" started, {get_human_readable_time(category_start_time)}'
        )
    )

    # Counters
    product_number = 0
    total_time = 0
    n_errors = 0

    for page in range(1, n_pages + 1):
        current_url = category_url + f"?&page={page}"
        page_with_products = Page(scraper.get_page(current_url))
        page_start_time = time.time()
        logger.write_log(
            add_brackets(
                f"Scraping from page #{page} started, {get_human_readable_time(page_start_time)}"
            )
        )
        for product_url in page_with_products.get_links():
            try:
                product = scrape_product(product_url, category_id, scraper)
                db.push(create_product_query(product))
                product_number += 1
                logger.write_log(f"Product #{product_number}\tid: {product.id}")
            except Exception as e:
                n_errors += 1
                logger.write_error_log(
                    f"Error #{n_errors}, {get_human_readable_time(time.time())}\nURL: {product_url}\nError: {e}"
                )

        page_scraping_time = time.time() - page_start_time
        total_time += page_scraping_time
        logger.write_log(
            add_brackets(
                f"Scraping from page #{page} ended in: {page_scraping_time:.2} seconds, average time: {(total_time / page):.2} seconds"
            )
        )

    logger.write_log(
        add_brackets(
            f"Scraping from category ended in: {(time.time() - category_start_time):.2} seconds"
        )
    )
