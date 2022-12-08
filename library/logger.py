from library.global_functions import read_configuration, append_file
import time

class Logger:
    logger_id = 0

    __slots__ = ["__error_log_file", "__log_file", "__id", "name", "display_log"]

    def __init__(self, name=None, display_log=True):
        """Initialize the logger"""

        def get_personal_path(path):
            """Returns the path specified by logger name"""
            path = path.split("/")
            path[-1] = f"{self.name}_{path[-1]}"
            return "/".join(path)

        self.__id = Logger.logger_id
        Logger.logger_id += 1

        self.display_log = display_log
        if name is None:
            self.name = f"logger{self.__id}"
        else:
            self.name = name

        configuration = read_configuration()["log"]
        self.__error_log_file = get_personal_path(configuration["error_log_file"])
        self.__log_file = get_personal_path(configuration["log_file"])

    def write_log(self, text):
        """Write the log to the log file specified in the configuration"""
        if self.display_log:
            print(text)
        append_file(self.__log_file, text)

    def write_error_log(self, text):
        if self.display_log:
            print(text)
        """Write the log to the log file specified in the configuration"""
        append_file(self.__error_log_file, text)


def add_brackets(text, style="="):
    """Returns the text in the brackets"""
    brackets = len(text) * style
    return f"{brackets}\n{text}\n{brackets}\n"

def get_human_readable_time(time_to_convert):
    """Returns the human readable time"""
    return time.asctime(time.localtime(time_to_convert))