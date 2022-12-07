from global_functions import read_configuration, append_file


class Logger:
    logger_id = 0

    __slots__ = ["__error_log_file", "__log_file", "__id", "__name"]

    def __init__(self):
        """Initialize the logger"""

        def get_personal_path(path):
            """Returns the path specified by logger id"""
            path = path.split("/")
            path[-1] = f"{self.__name}_{path[-1]}"
            return "/".join(path)

        self.__id = Logger.logger_id
        self.__name = f"logger{self.__id}"
        Logger.logger_id += 1

        configuration = read_configuration()["log"]

        self.__error_log_file = get_personal_path(configuration["error_log_file"])
        self.__log_file = get_personal_path(configuration["log_file"])

    def write_log(self, text, display=True):
        """Write the log to the log file specified in the configuration"""
        if display:
            print(text)
        append_file(self.__log_file, text)

    def write_error_log(self, text, display=True):
        if display:
            print(text)
        """Write the log to the log file specified in the configuration"""
        append_file(self.__error_log_file, text)


def add_brackets(text, style="="):
    """Returns the text in the brackets"""
    brackets = len(text) * style
    return f"{brackets}\n{text}\n{brackets}\n"
