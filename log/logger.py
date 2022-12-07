from global_functions import read_configuration, append_file


class Logger:
    def __init__(self):
        """Initialize the logger"""
        configuration = read_configuration()["log"]
        self.__error_log_file = configuration["error_log_file"]
        self.__log_file = configuration["log_file"]

    def write_log(self, text):
        """Write the log to the log file specified in the configuration"""
        append_file(self.__log_file, text)

    def write_error_log(self, text):
        """Write the log to the log file specified in the configuration"""
        append_file(self.__error_log_file, text)


def add_brackets(text, style="="):
    """Prints the log in an easy-to-read format"""
    brackets = len(text) * style
    return f"{brackets}\n{text}\n{brackets}\n"
