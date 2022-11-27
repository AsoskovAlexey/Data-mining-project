import pymysql


class MySQL:
    """
    A middleware layer between the MySQL server and python for python
    """

    __slots__ = ["__connection"]

    def __init__(self, config):
        """
        Initialize a connection for the MySQL server
        """
        self.__connection = pymysql.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            cursorclass=pymysql.cursors.DictCursor,
        )

    def pull(self, query):
        """
        Method for queries, to receive data from the database
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def push(self, query):
        """
        Method for queries, to insert any changes or data into the database
        """
        with self.__connection.cursor() as cursor:
            cursor.execute(query)
            self.__connection.commit()
