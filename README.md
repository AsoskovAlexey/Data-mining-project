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
3. Fill in your information in ```configuration.json```. Your user must have the right to create databases and tables, read and write to the database:exclamation:
4. The database will be created with the name you specify in this file.

Project authors : [Asoskov Aleksei](https://www.linkedin.com/in/aleksei-asoskov-b3051b257/), [Denis Laevskiy](https://www.linkedin.com/in/denis-laevskiy-79b715221/)
