import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# import re
# from selenium.common import TimeoutException
# from tqdm import tqdm
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


class Scraper:

    # Disable dynamic attributes
    __slots__ = ["__options", "__driver", "__scroll_pause_time", "__scroll_height"]

    def __init__(
        self,
        silent_mode=True,
        scroll_pause_time=2,
        scroll_height=1000,
        window_size=(1920, 1080),
    ):
        """
        Driver init
        """
        self.__options = Options()
        self.__options.headless = silent_mode
        self.__driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=self.__options
        )
        self.__driver.set_window_size(*window_size)
        self.__scroll_pause_time = scroll_pause_time
        self.__scroll_height = scroll_height

    def get_page(self, url):
        """
        Returns the page as BeautifulSoup soup
        """

        def scroll(self):
            """
            Scroll the page to the end
            """
            last_height = self.__driver.execute_script(
                "return document.body.scrollHeight"
            )
            scroll = 0
            while True:
                scroll += self.__scroll_height
                self.__driver.execute_script(f"window.scrollTo(0, {str(scroll)})")
                # Wait to load page
                time.sleep(self.__scroll_pause_time)
                # Calculate new scroll height and compare with last scroll height
                new_height = self.__driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height

        self.__driver.get(url)
        scroll(self)
        return BeautifulSoup(self.__driver.page_source, "lxml")

    def apply_page_settings(self, url):
        if self.__options.headless is False:
            user_input = ""
            self.__driver.get(url)
            user_input = input('Apply the settings and press "Enter"\n')
            print("Settings applied")
            del user_input
        else:
            raise Exception("Unable in silent_mode=True")
