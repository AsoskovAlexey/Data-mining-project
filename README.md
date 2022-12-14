# Data-mining-project
### A repository for the data mining project at :mortar_board: ITC, Israel. 
This project aims to collect data from [Aliexpress](https://aliexpress.com) for further analysis. 
### Currently implemented features:
:heavy_check_mark: Command line interface for easy interaction

:heavy_check_mark: Database creation with MySQL

:heavy_check_mark: Automatic installation of webdriver

:heavy_check_mark: Logger to monitor the work 

:heavy_check_mark: Storing product data (prices in USD and ILS and the date they were retrived are stored in a separate table)

Currently, the scraping engine on *selenium* was implemented to parse any Aliexpress category or the [special offers page](https://campaign.aliexpress.com/wow/gcp/new-user-channel/index).
## In order to use:
1. set up the libraries from requirments.txt
2. Have *Google Chrome* set up on your computer
3. :exclamation:Fill in your information in ```configuration.json```. Your user must have the right to create databases and tables, read and write to the database:exclamation:
4. The database will be created with the name you specify in this file.

### Usage:
```python3 main.py "url" "category" -m "mode"```
- ```"url"``` is the link to the category you want to collect for [example](https://www.aliexpress.com/category/70802/keyboards.html?trafficChannel=main&catName=keyboards&CatId=70802&ltype=wholesale&SortType=default&page=1&pvid=326-350021%2C351-350027&isrefine=y)
- ```"category"``` - how the category will be named in the database
- *optional* ```-m``` or ```--mode``` - Mode of the database creation script, defaults to "ask" :
  -  "ask": asks what to do if database is already exists
  - "force": force creation of new database. :skull_and_crossbones: if the database already has some data, **all the data will be deleted**, as this option creates all the tables anew :exclamation:
  - "soft": skip database creation if the database already exists

Project authors : [Asoskov Aleksei](https://www.linkedin.com/in/aleksei-asoskov-b3051b257/), [Denis Laevskiy](https://www.linkedin.com/in/denis-laevskiy-79b715221/)
