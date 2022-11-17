# Data-mining-project
### A repository for the data mining project at :mortar_board: ITC, Israel. 
This project aims to collect data from [Aliexpress](https://aliexpress.com) for further analysis. 
### Currently implemented features:
:heavy_check_mark: Webscraper called **crawler.py**

:heavy_check_mark: Export the result to a txt file

Currently the scraping engine on *selenium* was implemented to parse through the [special offers page](https://campaign.aliexpress.com/wow/gcp/new-user-channel/index) of Aliexpress. In order for the **scraper.py** to work, *selenium* should be properly installed and the variables in the file should correspond to files in the system:exclamation: 
## How to set up selenium: 

0. refer to this guide : https://selenium-python.readthedocs.io/installation.html
1. set up the libraries from requirments.txt
2. [download](https://selenium-python.readthedocs.io/installation.html) the webdriver (I used ChromeDriver 107.0.5304.62 with 107. version of Google Chrome)
3. line ```python 9. SER = Service(r"C:\Program Files (x86)\chromedriver.exe")``` should correspond to the full path to the driver
  - 3.1 if not using Google Chrome and Chromedriver lines 9-12 should be changed accordingly.:exclamation: DO IT AT YOUR OWN RISK:exclamation: File is configured to work with Chrome
4. in line 14 put a path to the *output.txt* file for storing data.

 The output is written in a dictionary-like structure and needs to be corrected (if you exited with a keyboard interrupt): 
 - remove the last entry if it was not written properly 
 - In order to make this a dictionary, {} have to be put around the text
  
  **pagesaver.py** can be used to save pages in html. :stopwatch: This code will be used later in the project 
  **newuser.html** is the result of pagesaver saving the special offer page.
