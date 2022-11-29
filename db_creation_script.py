import json
from db import MySQL

DB_CONFIG_FILE = "db/db_config.json"
DB_STRUCTURE_FILE = "db/project_db_structure.sql"
DB_NAME = "aliexpress"


def read_file(path):
    """Returns a file as a string"""
    try:
        with open(path) as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: No such file: {path}")


def read_json(path):
    """Returns a data from json"""
    try:
        with open(path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise Exception(f"Error: No such file: {path}")


def start(force=False):
    """Executes the database creation script"""

    print(
        f"Database creation script started. \n\tConfiguration:\
        \n\t\tDB_CONFIG_FILE: {DB_CONFIG_FILE}\
        \n\t\tDB_STRUCTURE_FILE: {DB_STRUCTURE_FILE}\
        \n\t\tDB_NAME: {DB_NAME}\n"
    )

    config = read_json(DB_CONFIG_FILE)
    db = MySQL(config)

    if {"Database": DB_NAME} not in db.pull("SHOW DATABASES;"):
        db_structure = read_file(DB_STRUCTURE_FILE)
        db.push(f"CREATE DATABASE {DB_NAME};")
        db.push(f"USE {DB_NAME};")
        for query in db_structure.split(";")[:-1]:  # Skip everything after the last ';'
            try:
                db.push(query)
            except:
                print(f"Unable to execute query: {query}")
        print("Database created successfully.\nDatabase creation script ended.")
        return
    else:
        print(
            f"Database: {DB_NAME} is already exists. Delete it and execute the script?\n",
            end="",
        )

        while True:
            if force:
                user_input = 'y'
            else:
                user_input = input("Enter y or n\n").lower()
            if user_input == "y":
                db.push(f"DROP DATABASE {DB_NAME};")
                start()
                break
            elif user_input == "n":
                print("Database creation aborted.\nDatabase creation script ended.")
                break
            else:
                print("Invalid input")


if __name__ == "__main__":
    start()
