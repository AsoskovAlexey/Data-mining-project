import selenium.common.exceptions
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import load_settings
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from set_up_driver import set_up_driver

settings = load_settings.Settings()
driver = set_up_driver()


def path_to_element(xpath: str, elem_number: int):
    """returns a XPATH to element, works only on the special offer page"""
    return f"{xpath}{elem_number}]"


def prettify_url(url):
    """creates a normal url from the nonsense aliexpress provides"""
    url = str(url)
    url_end = url.find(settings.URL_TEMPLATE)
    return url[:url_end]


def get_id(url):
    """get an id of the item from the url"""
    url = str(url)
    id_end = url.find(settings.URL_TEMPLATE)
    id_start = url.find(r"m/") + 7  # to cut off the first part of the url
    return url[id_start:id_end]


def unpack_card_info(card_info, url):
    """unpacks info from the card contents into a list"""
    card = card_info.splitlines()
    card.append(prettify_url(url))
    card[4] = card[4].strip(" Sold")
    return card


def scroll():
    """scrolls the page down"""
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def write_into_txt(key, entry):
    """write the output dictionary as txt file for further work"""
    line_to_write = f"'{key}':{entry},"
    with open(settings.DATAFILE, 'a+') as data_file:
        data_file.write(line_to_write)


def scrape(elements_scraped):
    """waits for elements to appear, scrolls the page down and collects card info"""
    WebDriverWait(driver, 10).until(  # wait until the element appears
        EC.presence_of_element_located((By.XPATH, path_to_element(settings.XPATH_mask, elements_scraped))))
    scroll()
    collect_card_info(elements_scraped)


def finalise_file():
    pass


def main_sequence(url: str, maximum: int = 0):
    """main scraping sequence """
    driver.get(url)
    elements_scraped = 10
    try:
        if maximum != 0:  # runs a loop, that makes maximum-1 steps
            for elements_scraped in tqdm(range(elements_scraped, maximum+1, 10)):
                scrape(elements_scraped)
                elements_scraped += 10
        else:
            while True:  # if no value was passed, runs infinitely
                scrape(elements_scraped)
                elements_scraped += 10
    except (selenium.common.exceptions.WebDriverException, selenium.common.exceptions.TimeoutException) as err:
        print(f"Timeout! Page can not be parsed:{err}")
    driver.quit()


def collect_card_info(end: int):
    """collects the information from individual item cards"""
    for i in range(end - 10, end):
        if i != 0:
            element = driver.find_element(by=By.XPATH, value=path_to_element(settings.XPATH_mask, i))
            url = element.get_attribute('href')
            card_info = element.get_attribute('outerText')
            write_into_txt(get_id(url), unpack_card_info(card_info, url))


if __name__ == '__main__':
    main_sequence("https://campaign.aliexpress.com/wow/gcp/new-user-channel/index", 100)
    print("sequence finished")
