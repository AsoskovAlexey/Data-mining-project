import database.database_creation_script as db_creation_script
from log.logger import Logger
from collect_category import scrape_category


def main():
    main_logger = Logger(name="main")
    db_creation_script.start(mode="force", logger=main_logger)
    
    scrape_category("https://www.aliexpress.com/category/708042/cpus.html", 0)

if __name__ == "__main__":
    main()