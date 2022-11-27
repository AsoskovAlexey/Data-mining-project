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


def start():
    with open(DB_CONFIG_FILE) as json_file:
        config = json.load(json_file)

    db = MySQL(config)
    db_structure = read_file(DB_STRUCTURE_FILE)

    if {"Database": DB_NAME} not in db.pull("SHOW DATABASES;"):
        db.push(f"CREATE DATABASE {DB_NAME};")
        db.push(f"USE {DB_NAME};")
        for index, query in enumerate(
            db_structure.split(";")[:-1]
        ):  # Skip everything after the last ';'
            try:
                db.push(query)
            except:
                print(f"Unable to execute query: {query}")
        print("Done!")
        return
    else:
        print(
            f"Database: {DB_NAME} is already exists. Delete it and execute the script?\n",
            end="",
        )

        while True:
            user_input = input("Enter y or n\n").lower()
            if user_input == "y":
                db.push(f"DROP DATABASE {DB_NAME};")
                start()
                break
            elif user_input == "n":
                print("Exit")
                break
            else:
                print("Invalid input")


if __name__ == "__main__":
    start()
