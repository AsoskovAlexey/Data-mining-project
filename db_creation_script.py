from db import MySQL
from global_functions import read_json, read_file
from global_variables import Constants


def get_user_input(mode):
    """Returns the user_input based on the mode"""
    if mode == "force":
        print("Yes")
        return "y"
    elif mode == "ask":
        return input("Enter y or n\n").lower()
    elif mode == "skip":
        print("No")
        return "n"
    else:
        raise ValueError(
            f'Invalid mode specified: "{mode}". Use "ask","force" or "skip".'
        )


def start(mode="ask"):
    """
    Executes the database creation script

    Args:
        mode (str, optional): Defaults to "ask".
            'ask': asks what to do if database is already exists
            'force': force creation of new database
            'skip': skip database creation if the database already exists
    """

    config = read_json(Constants.DB_CONFIG_FILE)
    db = MySQL(config)

    if {"Database": Constants.DB_NAME} not in db.pull("SHOW DATABASES;"):
        print(
            f"\nDatabase creation script started. \n\tConfiguration:\
            \n\t\tDB_CONFIG_FILE: {Constants.DB_CONFIG_FILE}\
            \n\t\tDB_STRUCTURE_FILE: {Constants.DB_STRUCTURE_FILE}\
            \n\t\tDB_NAME: {Constants.DB_NAME}\n"
        )
        db_structure = read_file(Constants.DB_STRUCTURE_FILE)
        db.push(f"CREATE DATABASE {Constants.DB_NAME};")
        db.push(f"USE {Constants.DB_NAME};")
        for query in db_structure.split(";")[:-1]:  # Skip everything after the last ';'
            try:
                db.push(query)
            except:
                print(f"Unable to execute query: {query}")
        print("Database created successfully.\nDatabase creation script ended.\n")
        return
    else:
        print(
            f"Database: {Constants.DB_NAME} is already exists. Delete it and execute the script?",
        )

        while True:
            user_input = get_user_input(mode=mode)

            if user_input == "y":
                db.push(f"DROP DATABASE {Constants.DB_NAME};")
                start()
                break
            elif user_input == "n":
                print("Database creation aborted.\nDatabase creation script ended.")
                break
            else:
                print("Invalid input")


if __name__ == "__main__":
    start()
