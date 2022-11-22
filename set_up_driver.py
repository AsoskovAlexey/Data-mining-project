from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def set_up_driver():
    SER = Service(r"C:\Program Files (x86)\chromedriver.exe")
    OP = webdriver.ChromeOptions()
    OP.add_argument("--start-maximized")  # the window should start maximised
    driver = webdriver.Chrome(service=SER, options=OP)
    return driver
