import datetime
import os


class ConsoleColor:
    GRAY = '\033[90m'
    RED = '\033[91m'
    RED_BOLD = '\033[1m\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Logger:
    def __init__(self, filename: str = None):
        self.datetime_format = '%Y-%m-%d %H:%M:%S'
        self.filename = filename + '.log' if filename else None

    def _log(self, message_type: str, color: str, message: str, extra: dict = {}):
        datetime_str = datetime.datetime.now().strftime(self.datetime_format)
        log_entry = f"{ConsoleColor.BOLD}{datetime_str}{ConsoleColor.END} {color}[{message_type}]{ConsoleColor.END} {message}"
        if extra:
            log_entry += f" {extra}"

        print(log_entry)

        if self.filename:
            with open(self.filename, 'a') as f:
                f.write(log_entry + os.linesep)

    def spam(self, message: str, extra: dict = {}):
        self._log('SPAM', ConsoleColor.GRAY, message, extra)

    def error(self, message: str, extra: dict = {}):
        self._log('ERROR', ConsoleColor.RED, message, extra)

    def critical(self, message: str, extra: dict = {}):
        self._log('CRITICAL', ConsoleColor.RED_BOLD, message, extra)

    def success(self, message: str, extra: dict = {}):
        self._log('SUCCESS', ConsoleColor.GREEN, message, extra)

    def debug(self, message: str, extra: dict = {}):
        self._log('DEBUG', ConsoleColor.GREEN, message, extra)

    def warning(self, message: str, extra: dict = {}):
        self._log('WARNING', ConsoleColor.YELLOW, message, extra)

    def verbose(self, message: str, extra: dict = {}):
        self._log('VERBOSE', ConsoleColor.BLUE, message, extra)

    def notice(self, message: str, extra: dict = {}):
        self._log('NOTICE', ConsoleColor.PURPLE, message, extra)

    def header(self, message: str, extra: dict = {}):
        self._log('HEADER', ConsoleColor.CYAN, message, extra)

    def info(self, message: str, extra: dict = {}):
        self._log('INFO', ConsoleColor.WHITE, message, extra)

    def print_logs(self, page=1, page_size=10):
        if not self.filename:
            print("No log file specified.")
            return

        if not os.path.exists(self.filename):
            print("Log file does not exist.")
            return

        with open(self.filename, 'r') as f:
            lines = f.readlines()
            total_pages = (len(lines) + page_size - 1) // page_size
            start = len(lines) - page_size * (page)
            end = start + page_size

            print(f"Showing logs from page {page} of {total_pages}:\n")

            for line in lines[start:end]:
                print(line.strip())

            if page == total_pages:
                if page == 1:
                    print("\nReached the last page. Press any key to exit.")
                else:
                    print("\nReached the last page. Type 'p' for the previous page, or any other key to exit.")
            else:
                print("\nType 'n' for the next page, 'p' for the previous page, or any other key to exit.")

            key = input().lower()
            if key == 'n' and page < total_pages:
                page += 1
                self.print_logs(page, page_size)
            elif key == 'p' and page > 1:
                page -= 1
                self.print_logs(page, page_size)
