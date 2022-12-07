from database.database_driver import MySQL
from global_functions import read_configuration, read_file


def get_user_input(mode):
    """Returns the user_input based on the mode"""
    if mode == "force":
        print(f"mode: {mode}")
        return "y"
    elif mode == "ask":
        return input("Enter y or n\n").lower()
    elif mode == "skip":
        print(f"mode: {mode}")
        return "n"
    else:
        raise ValueError(
            f'Invalid mode specified: "{mode}". Use "ask","force" or "skip".'
        )


def execute_script(database_driver, database_configuration):
    """Executes database creation script"""
    print(
        f"Database creation script started. \n\tConfiguration:\
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
            print(f"Unable to execute query: {query}")
    print("Database created successfully.\nDatabase creation script ended.\n")


def start(mode="ask"):
    """
    Executes the database creation script

    Args:
        mode (str, optional): Defaults to "ask".
            'ask': asks what to do if database is already exists
            'force': force creation of new database
            'skip': skip database creation if the database already exists
    """
    configuration = read_configuration()["database"]
    db_driver = MySQL(configuration)
    if {"Database": configuration["database_name"]} not in db_driver.pull(
        "SHOW DATABASES;"
    ):
        execute_script(db_driver, configuration)
    else:
        print(
            f"Database: {configuration['database_name']} is already exists. Delete it and execute the script?",
        )
        while True:
            user_input = get_user_input(mode=mode)
            if user_input == "y":
                db_driver.push(f"DROP DATABASE {configuration['database_name']};")
                execute_script(db_driver, configuration)
                break
            elif user_input == "n":
                print("Database creation aborted.")
                break
            else:
                print("Invalid input")
