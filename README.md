# Data-mining-project
A repository for the data mining project at ITC, Israel
This project aims to collect data from aliexpress for further analysis.
Currently the scraping engine on selenium was implemented to parse through the special offers page of aliexpress.
in order for the scraper.py to work, selenium should be properly installed and the variables in the file should correspond to files in the system.
How to set up selenium:
  0. refer to this guide : https://selenium-python.readthedocs.io/installation.html
  1. set up the libraries from requirments.txt
  2. downnload the webdriver I used ChromeDriver 107.0.5304.62 with 107. version of Google Chrome
  3. line 9 SER = Service(r"C:\Program Files (x86)\chromedriver.exe") should correspond to the full path to the driver
  3.1 if not using Google Chrome and Chromedriver lines 9-12 should be changed accordingly. DO IT AT YOUR OWN RISK! File is configured to work with Chrome
  4. in line 14 put a path to the output txt file for storing data. THIS FILE SHOULD BE CREATED BEFORE RUNNING THE SCRIPT!
  
  pagesaver.py can be used to save pages in html. this code will be used later in the project 
  
