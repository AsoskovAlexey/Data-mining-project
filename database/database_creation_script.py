from database.database_driver import MySQL
from library.global_functions import read_configuration, read_file
from library.logger import Logger, add_brackets, get_human_readable_time
import time


def get_user_input(mode, logger):
    """Returns the user_input based on the mode"""
    if mode == "force":
        logger.write_log(f"mode: {mode}")
        return "y"
    elif mode == "ask":
        return input("Enter y or n\n").lower()
    elif mode == "skip":
        logger.write_log(f"mode: {mode}")
        return "n"
    else:
        raise ValueError(
            f'Invalid mode specified: "{mode}". Use "ask","force" or "skip".'
        )


def execute_script(database_driver, database_configuration, logger, db_start_time):
    """Executes database creation script"""
    logger.write_log(
        f"Database creation started. \n\tConfiguration:\
            \n\t\tstructure_file: {database_configuration['structure_file']}\
            \n\t\tdatabase_name: {database_configuration['database_name']}\n"
    )
    db_structure = read_file(database_configuration["structure_file"])
    database_driver.push(f"CREATE DATABASE {database_configuration['database_name']};")
    database_driver.use_database(database_configuration["database_name"])
    for query in db_structure.split(";")[:-1]:  # Skip everything after the last ';'
        try:
            database_driver.push(query)
        except:
            logger.write_log(f"Unable to execute query: {query}")
    logger.write_log(f"Database created successfully in: {(time.time() - db_start_time):.2} seconds")
    logger.write_log(add_brackets(f"Database creation script ended, {get_human_readable_time(time.time())}"))


def start(mode="ask", logger=None):
    """
    Executes the database creation script using the 'mode'

    Args:
        mode (str, optional): Defaults to "ask".
            'ask': asks what to do if database is already exists
            'force': force creation of new database
            'skip': skip database creation if the database already exists
    """
    db_start_time = time.time()
    # Logger initialization
    if logger is None:
        logger = Logger(name='database')
    
    logger.write_log(add_brackets(f'Database creation script started, {get_human_readable_time(db_start_time)}'))
    
    configuration = read_configuration()["database"]
    db_driver = MySQL(configuration)
    if {"Database": configuration["database_name"]} not in db_driver.pull(
        "SHOW DATABASES;"
    ):
        execute_script(db_driver, configuration, logger)
    else:
        logger.write_log(
            f"Database: {configuration['database_name']} is already exists. Delete it and execute the script?",
        )
        while True:
            user_input = get_user_input(mode, logger)
            if user_input == "y":
                db_driver.push(f"DROP DATABASE {configuration['database_name']};")
                execute_script(db_driver, configuration, logger, db_start_time)
                break
            elif user_input == "n":
                logger.write_log(f"Database creation aborted, {get_human_readable_time(time.time())}")
                break
            else:
                logger.write_log("Invalid input")
