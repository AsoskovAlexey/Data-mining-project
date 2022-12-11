import database.database_creation_script as db_creation_script
from library.logger import Logger
from library.collect_category import start_engine
import argparse


def get_arguments():
    """
    This function gets the arguments from the command line.
    Returns the arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "url",
        help='URL of the aliexpress category (or any search) page you want to scrape. Example: "https://www.aliexpress.com/category/708042/cpus.html"',
    )

    parser.add_argument(
        "title",
        help='Title of the aliexpress category page. Example: "CPUs"',
    )

    parser.add_argument(
        "-m",
        "--mode",
        help='Mode of the database creation script: Defaults to "ask".\
            "ask": asks what to do if database is already exists\
            "force": force creation of new database\
            "soft": skip database creation if the database already exists',
    )

    return parser.parse_args()


def main():
    args = get_arguments()
    main_logger = Logger(name="main")
    if args.mode is None:
        args.mode = 'ask'
    db_creation_script.start(mode=args.mode, logger=main_logger)
    start_engine(args.url, args.title)


if __name__ == "__main__":
    main()
