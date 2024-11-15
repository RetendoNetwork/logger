import os
import inspect
from datetime import datetime
from termcolor import colored


class Logger:
    def __init__(self, log_folder_root=".", enable_color=True):
        # Log directory setup
        self.log_folder_path = os.path.join(log_folder_root, "log")
        os.makedirs(self.log_folder_path, exist_ok=True)

        # Log file setup
        self.all_logs_file = self._create_log_file("all.log")
        self.critical_log_file = self._create_log_file("critical.log")
        self.error_log_file = self._create_log_file("error.log")
        self.warning_log_file = self._create_log_file("warning.log")
        self.success_log_file = self._create_log_file("success.log")
        self.info_log_file = self._create_log_file("info.log")

        self.max_prefix_length = max(len(prefix) for prefix in ["CRITICAL", "ERROR", "WARNING", "SUCCESS", "INFO"])

        # Color support
        self.enable_color = enable_color

    def _create_log_file(self, filename):
        path = os.path.join(self.log_folder_path, filename)
        return open(path, "a")

    def _get_caller_info(self):
        frame = inspect.currentframe().f_back.f_back.f_back  # Go 3 levels back to get the caller
        file = inspect.getfile(frame)
        line = frame.f_lineno
        func = frame.f_code.co_name
        package = file.split("/")[-1]

        return file.split("/")[-1], line, func, package

    def _log_line(self, message, prefix, prefix_colored, log_file):
        file, line, func, package = self._get_caller_info()
        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        prefix_length = len(prefix)
        spacing = " " * (self.max_prefix_length - prefix_length + 1)

        log_plain = f"[{date}] [{prefix}] {spacing}[func {func}] {package}/{file}:{line} : {message}"
        log_plain_spaced = f"[{date}] [{prefix}] {spacing}[func {func}] {package}/{file}:{line} : {message}"

        if self.enable_color:
            print(f"{colored(date, 'grey')} {prefix_colored} {spacing}{colored(f'func {func}', 'magenta')} "
                  f"{colored(package, 'green')} {colored(file, 'yellow')} {colored(line, 'yellow')} "
                  f"{colored(message, 'bold')}")
        else:
            print(log_plain_spaced)

        # Write to log files
        log_file.write(log_plain + "\n")
        self.all_logs_file.write(log_plain_spaced + "\n")

    def critical(self, message):
        self._log_line(message, "CRITICAL", colored("CRITICAL", "white", attrs=["bold", "reverse"]), self.critical_log_file)

    def error(self, message):
        self._log_line(message, "ERROR", colored("ERROR", "red", attrs=["bold"]), self.error_log_file)

    def warning(self, message):
        self._log_line(message, "WARNING", colored("WARNING", "yellow", attrs=["bold"]), self.warning_log_file)

    def success(self, message):
        self._log_line(message, "SUCCESS", colored("SUCCESS", "green", attrs=["bold"]), self.success_log_file)

    def info(self, message):
        self._log_line(message, "INFO", colored("INFO", "cyan", attrs=["bold"]), self.info_log_file)

    def criticalf(self, message, *args):
        self._log_line(message % args, "CRITICAL", colored("CRITICAL", "white", attrs=["bold", "reverse"]), self.critical_log_file)

    def errorf(self, message, *args):
        self._log_line(message % args, "ERROR", colored("ERROR", "red", attrs=["bold"]), self.error_log_file)

    def warningf(self, message, *args):
        self._log_line(message % args, "WARNING", colored("WARNING", "yellow", attrs=["bold"]), self.warning_log_file)

    def successf(self, message, *args):
        self._log_line(message % args, "SUCCESS", colored("SUCCESS", "green", attrs=["bold"]), self.success_log_file)

    def infof(self, message, *args):
        self._log_line(message % args, "INFO", colored("INFO", "cyan", attrs=["bold"]), self.info_log_file)

    def close(self):
        self.all_logs_file.close()
        self.critical_log_file.close()
        self.error_log_file.close()
        self.warning_log_file.close()
        self.success_log_file.close()
        self.info_log_file.close()


def NewLogger(log_folder_root="."):
    """Creation of a Logger instance with a given log directory."""
    return Logger(log_folder_root)