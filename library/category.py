import database.database_query_generator as dqg


def get_id_from_response(response):
    """Returns category id from database response"""
    return response[0]["id"]  # response is a list with a dictionary inside


def get_category_id(url, title, database_driver):
    """Returns category id from database. Adds a new category if it does not exist."""
    query = dqg.get_category_id(url, title)

    response = database_driver.pull(query)
    if not response:
        database_driver.push(dqg.add_category(url, title))
        response = database_driver.pull(query)

    return get_id_from_response(response)
