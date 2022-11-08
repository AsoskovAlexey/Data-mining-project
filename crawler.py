from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Setting up driver
SER = Service(r"C:\Program Files (x86)\chromedriver.exe")
OP = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=SER, options=OP)


def path_to_element(elem_number: int):
    """returns a XPATH to element, works only on the special offer page"""
    return f" / html / body / div[2] / div / div / div[3] / div[2] / a[{elem_number}]"


def scrape(url: str):
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, path_to_element(1))))
        print("Connected!")
        collect_card_info()
    except Exception as err:
        print(f"Timeout! Page can not be parsed:{err}")
    finally:
        driver.quit()


def collect_card_info():
    for i in range(1, 40):
        element = driver.find_element(by=By.XPATH, value=path_to_element(i)).get_attribute('href')
        print(element)


if __name__ == '__main__':
    scrape("https://campaign.aliexpress.com/wow/gcp/new-user-channel/index")