from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setting up driver
SER = Service(r"C:\Program Files (x86)\chromedriver.exe")
OP = webdriver.ChromeOptions()
OP.add_argument("--start-maximized")  # the window should start maximised
driver = webdriver.Chrome(service=SER, options=OP)
URL_TEMPLATE = ".html"

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
    card = card_info.splitlines()
    card.append(prettify_url(url))
    card[4] = card[4].strip(" Sold")
    return card


def scroll():
    last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height != last_height:
        last_height = new_height


def scrape(url: str, maximum: int):
    """main scraping engine"""
    driver.get(url)
    elements_scraped = 10
    try:
        while elements_scraped <= maximum:
            WebDriverWait(driver, 10).until(  # wait until the element appears
                EC.presence_of_element_located((By.XPATH, path_to_element(elements_scraped))))
            collect_card_info(elements_scraped)
            scroll()
            elements_scraped += 10
    except Exception as err:
        print(f"Timeout! Page can not be parsed:{err}")
    driver.quit()


def collect_card_info(end: int):
    for i in range(end - 10, end):
        if i != 0:
            element = driver.find_element(by=By.XPATH, value=path_to_element(i))
            url = element.get_attribute('href')
            card_info = element.get_attribute('outerText')
            result_dict[get_id(url)] = unpack_card_info(card_info, url)
            print(f"collected {i} results")



def all_tests():
    assert get_id("""https://www.aliexpress.us/item/3256804460500632.html?pdp_ext_f=%7B%22ship_from%22%3A%22CN%22%2C%22s
        ku_id%22%3A%2212000029965651299%22%7D&scm=1007.34914.307035.0&scm_id=1007.34914.307035.0&scm-url=1007.34914.307035.0
        &pvid=ec7408e9-5690-4dac-ab32-d6f013f97e50&utparam=%257B%2522process_id%2522%253A%2522401%2522%252C%2522x_object_typ
        e%2522%253A%2522product%2522%252C%2522pvid%2522%253A%2522ec7408e9-5690-4dac-ab32-""") == "3256804460500632"


if __name__ == '__main__':
    scrape("https://campaign.aliexpress.com/wow/gcp/new-user-channel/index", 100)
    print("the dictionary has", len(result_dict), "entries")
    #all_tests()
