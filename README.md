# Data-mining-project

## A repository for the data mining project at :mortar_board: ITC, Israel. 
This project aims to collect data from [Aliexpress](https://aliexpress.com) for further analysis. 
A repository for the data mining project at mortar_board ITC, Israel.
This project aims to collect data from Aliexpress for further analysis.

## What it does:
Collects product data for each product from Aliexpress categogy and push it to the database.
Just run the **main.py** and follow the steps below:
0. Set up the **db_config.json** file in the **db** directory.
1. Auto database creation
2. database driver initialization
3. Scraper initialization
4. The Aliexpress page opens.You need to configure the **country, language, currency and accept the cookies**. After that, go back to the **console** and press **enter**.
5. Wait for the results.

## Currently implemented features:
1. Webscraper called **page_scraper.py**. Gets the **url**, scroll down the page and returns a **BeautifulSoup**.
2. Database creation script **db_creation_script.py**.
Creates the database from **path to database structure file**. You need to set up the **db/db_config.json**.
If the databe is already exists asks to delite it and execute the scrit again.
3. Implemented **MySQL** database driver, that allows to pull and push the data (or any changes) to/from the databese **db.py**.
