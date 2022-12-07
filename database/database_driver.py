import pymysql


class MySQL:
    """
    A middleware layer between the MySQL server and python for python
    """

    __slots__ = ["__connection"]

    def __init__(self, configuration):
        """
        Initialize a connection for the MySQL server
        """
        self.__connection = pymysql.connect(
            host=configuration["host"],
            user=configuration["user"],
            password=configuration["password"],
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

    def use_database(self, database_name):
        try:
            self.push(f"USE {database_name};")
        except pymysql.err.OperationalError:
            raise ValueError(f"Error: No such database: {database_name}")
