from database.database_driver import MySQL
from library.global_functions import read_configuration, read_file
from library.logger import Logger, add_brackets, get_human_readable_time
import time
import re
import pymysql


def get_user_input(mode, logger):
    """Returns the user_input based on the mode"""
    if mode == "force":
        logger.write_log(f"mode: {mode}")
        return "y"
    elif mode == "ask":
        return input("Enter y or n\n").lower()
    elif mode == "soft":
        logger.write_log(f"mode: {mode}")
        return "n"
    else:
        raise ValueError(
            f'Invalid mode specified: "{mode}". Use "ask","force" or "soft".'
        )


def execute_script(database_driver, database_configuration, logger):
    """Executes database creation script"""
    db_start_time = time.time()
    logger.write_log(
        f"Database creation started. \n\tConfiguration:\
            \n\t\tstructure_file: {database_configuration['structure_file']}\
            \n\t\tdatabase_name: {database_configuration['database_name']}\n"
    )
    db_structure = read_file(database_configuration["structure_file"])
    
    
    database_driver.use_database(database_configuration["database_name"])
    for query in db_structure.split(";")[:-1]:  # Skip everything after the last ';'
        try:
            database_driver.push(query)
        except pymysql.err.OperationalError as e: # if table is already exists: drops it and recreate a new one
            e = str(e)
            table_name = re.search("Table '(.*)' already exists", e).groups()[
                0
            ]  # 0 means the first match
            database_driver.push(f"DROP TABLE {table_name};")
            logger.write_log(f'Table "{table_name}" droped')
            database_driver.push(query)
            logger.write_log(f'Table "{table_name}" recreated')
        except Exception as e:
            logger.write_log(f"Unable to execute query: {query}\nError: {e}")
    logger.write_log(
        f"\nDatabase created successfully in: {(time.time() - db_start_time):.2} seconds"
    )


def start(mode="ask", logger=None):
    """
    Executes the database creation script using the 'mode'

    Args:
        mode (str, optional): Defaults to "ask".
            'ask': asks what to do if database is already exists
            'force': force creation of new database
            'soft': skip database creation if the database already exists
    """
    # Logger initialization
    if logger is None:
        logger = Logger(name="database")

    logger.write_log(
        add_brackets(
            f"Database creation script started, {get_human_readable_time(time.time())}"
        )
    )

    configuration = read_configuration()["database"]
    db_driver = MySQL(configuration)
    if {"Database": configuration["database_name"]} not in db_driver.pull(
        "SHOW DATABASES;"
    ):
        
        db_driver.push(f"CREATE DATABASE {configuration['database_name']};")
        execute_script(db_driver, configuration, logger)
    else:
        logger.write_log(
            f"Database: {configuration['database_name']} is already exists. Delete it and execute the script?",
        )
        while True:
            user_input = get_user_input(mode, logger)
            if user_input == "y":
                #db_driver.push(f"DROP DATABASE {configuration['database_name']};")
                execute_script(db_driver, configuration, logger)
                break
            elif user_input == "n":
                logger.write_log(
                    f"Database creation aborted, {get_human_readable_time(time.time())}"
                )
                break
            else:
                logger.write_log("Invalid input")
    logger.write_log(
        add_brackets(
            f"Database creation script ended, {get_human_readable_time(time.time())}"
        )
    )
