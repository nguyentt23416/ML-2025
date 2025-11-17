import subprocess
import sys
import os


class AppController:
    def __init__(self):
        self.current_process = None

    def open_login(self):
        self._close_current()
        self.current_process = subprocess.Popen([sys.executable, "login.py"])

    def open_statistic(self):
        self._close_current()
        self.current_process = subprocess.Popen([sys.executable, "statistic.py"])

    def open_management(self):
        self._close_current()
        self.current_process = subprocess.Popen([sys.executable, "management.py"])

    def open_prediction(self):
        self._close_current()
        self.current_process = subprocess.Popen([sys.executable, "prediction.py"])

    def logout(self):
        self._close_current()
        self.current_process = subprocess.Popen([sys.executable, "login.py"])

    def _close_current(self):
        if self.current_process:
            self.current_process.terminate()
            self.current_process.wait()


controller = AppController()