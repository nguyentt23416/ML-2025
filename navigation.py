import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox


def navigate_to(target_file, current_window=None):
    """
    Navigate to another window by closing current and opening target
    """
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_path = os.path.join(current_dir, target_file)

        # Verify the file exists
        if not os.path.exists(target_path):
            messagebox.showerror("Error", f"File not found: {target_path}")
            return False

        print(f"Navigating to: {target_path}")  # Debug print

        # Close current window if provided
        if current_window:
            current_window.destroy()

        # Open target file
        subprocess.Popen([sys.executable, target_path])
        return True

    except Exception as e:
        error_msg = f"Failed to navigate to {target_file}: {str(e)}"
        messagebox.showerror("Navigation Error", error_msg)
        print(f"Navigation error details: {e}")
        return False


# Navigation functions for easy import
def open_statistic(current_window=None):
    return navigate_to("statistic.py", current_window)


def open_management(current_window=None):
    return navigate_to("management.py", current_window)


def open_prediction(current_window=None):
    return navigate_to("prediction.py", current_window)


def open_login(current_window=None):
    return navigate_to("login.py", current_window)

