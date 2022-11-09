from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Setting up driver
SER = Service(r"C:\Program Files (x86)\chromedriver.exe")
OP = webdriver.ChromeOptions()
OP.add_argument("--start-maximized")  # the window should start maximised
driver = webdriver.Chrome(service=SER, options=OP)
URL_TEMPLATE = ".html"
DATAFILE = 'datafile.txt'

result_dict = {}  # create a dictionary for results


def path_to_element(elem_number: int):
    """returns a XPATH to element, works only on the special offer page"""
    return f" / html / body / div[2] / div / div / div[3] / div[2] / a[{elem_number}]"


def prettify_url(url):
    """creates a normal url from the nonsense aliexpress provides"""
    url = str(url)
    url_end = url.find(URL_TEMPLATE)
    return url[:url_end]


def get_id(url):
    """get an id of the item from the url"""
    url = str(url)
    id_end = url.find(URL_TEMPLATE)
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
    last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height != last_height:
        last_height = new_height


def write_into_txt(file):
    """write the output dictionary as txt file for further work"""
    with open(DATAFILE, 'w') as data_file:
        data_file.write(json.dumps(file))
    print(f"{len(file)} entries saved into datafile!")


def scrape(elements_scraped):
    """waits for elements to appear, scrolls the page down and collects card info"""
    WebDriverWait(driver, 10).until(  # wait until the element appears
        EC.presence_of_element_located((By.XPATH, path_to_element(elements_scraped))))
    scroll()
    collect_card_info(elements_scraped)


def main_sequence(url: str, maximum: int = 0):
    """main scraping sequence """
    driver.get(url)
    elements_scraped = 10
    try:
        if maximum != 0:  # runs a loop, that makes maximum-1 steps
            while elements_scraped <= maximum:
                scrape(elements_scraped)
                elements_scraped += 10
        else:
            while True:  # if no value was passed, runs infinitely
                scrape(elements_scraped)
                elements_scraped += 10
    except Exception as err:
        print(f"Timeout! Page can not be parsed:{err}")
    driver.quit()


def collect_card_info(end: int):
    """collects the information from individual item cards"""
    for i in range(end - 10, end):
        if i != 0:
            element = driver.find_element(by=By.XPATH, value=path_to_element(i))
            url = element.get_attribute('href')
            card_info = element.get_attribute('outerText')
            result_dict[get_id(url)] = unpack_card_info(card_info, url)
            print(f"collected {i} results")


if __name__ == '__main__':
    main_sequence("https://campaign.aliexpress.com/wow/gcp/new-user-channel/index", 2500)
    write_into_txt(result_dict)
