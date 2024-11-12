import os
import logging
import time
from colorama import Fore, Back, Style, init
from pathlib import Path
import inspect

init(autoreset=True)

flags = 'a'
log_template = "[{}] [{}] {} [{} {}:{}] : {}"

prefixes = {
    "critical": {"plain": "CRITICAL", "colored": Fore.WHITE + Back.RED + Style.BRIGHT + "CRITICAL"},
    "error": {"plain": "ERROR", "colored": Fore.RED + Style.BRIGHT + "ERROR"},
    "warning": {"plain": "WARNING", "colored": Fore.YELLOW + Style.BRIGHT + "WARNING"},
    "success": {"plain": "SUCCESS", "colored": Fore.GREEN + Style.BRIGHT + "SUCCESS"},
    "info": {"plain": "INFO", "colored": Fore.CYAN + Style.BRIGHT + "INFO"},
}

class Logger:
    def __init__(self, log_folder_root="."):
        log_folder_path = Path(log_folder_root) / "log"
        log_folder_path.mkdir(parents=True, exist_ok=True)

        self.all_logs_file = open(log_folder_path / "all.log", flags)
        self.critical_log_file = open(log_folder_path / "critical.log", flags)
        self.error_log_file = open(log_folder_path / "error.log", flags)
        self.warning_log_file = open(log_folder_path / "warning.log", flags)
        self.success_log_file = open(log_folder_path / "success.log", flags)
        self.info_log_file = open(log_folder_path / "info.log", flags)

    def _log_line(self, message, prefix, prefix_colored, log_file):
        file, line, function, package_name = self._get_caller_info()
        date = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())

        spacing = " " * (len(prefixes["critical"]["plain"]) - len(prefix) + 1)

        log_plain = log_template.format(date, prefix, " ", function, package_name, line, message)
        log_plain_spaced = log_template.format(date, prefix, spacing, function, package_name, line, message)

        print(log_template.format(Fore.LIGHTBLACK_EX + date, prefix_colored, spacing, Fore.MAGENTA + function, Fore.GREEN + package_name, Fore.GREEN + file, Fore.YELLOW + line, Style.BRIGHT + message))

        log_file.write(log_plain + "\n")
        self.all_logs_file.write(log_plain_spaced + "\n")

    def _get_caller_info(self):
        frame = inspect.currentframe().f_back.f_back.f_back
        filename = os.path.basename(frame.f_code.co_filename)
        line = frame.f_lineno
        function = frame.f_code.co_name
        package_name = frame.f_globals["__name__"]
        return filename, str(line), function + "()", package_name

    def critical(self, message):
        self._log_line(message, prefixes["critical"]["plain"], prefixes["critical"]["colored"], self.critical_log_file)

    def error(self, message):
        self._log_line(message, prefixes["error"]["plain"], prefixes["error"]["colored"], self.error_log_file)

    def warning(self, message):
        self._log_line(message, prefixes["warning"]["plain"], prefixes["warning"]["colored"], self.warning_log_file)

    def success(self, message):
        self._log_line(message, prefixes["success"]["plain"], prefixes["success"]["colored"], self.success_log_file)

    def info(self, message):
        self._log_line(message, prefixes["info"]["plain"], prefixes["info"]["colored"], self.info_log_file)

    def criticalf(self, message, *args):
        self.critical(message.format(*args))

    def errorf(self, message, *args):
        self.error(message.format(*args))

    def warningf(self, message, *args):
        self.warning(message.format(*args))

    def successf(self, message, *args):
        self.success(message.format(*args))

    def infof(self, message, *args):
        self.info(message.format(*args))

    def close(self):
        self.all_logs_file.close()
        self.critical_log_file.close()
        self.error_log_file.close()
        self.warning_log_file.close()
        self.success_log_file.close()
        self.info_log_file.close()