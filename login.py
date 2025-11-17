import os
import sys
import tkinter as tk
from tkinter import messagebox
import json
import hashlib
import datetime
import subprocess


def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)


class LoginSystem:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1080x720")
        self.window.configure(bg="#ffffff")
        self.window.title("Login System")

        # Accounts database file
        self.accounts_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "account", "accounts.json")

        # Create accounts directory and file if they don't exist
        accounts_dir = os.path.dirname(self.accounts_file)
        if not os.path.exists(accounts_dir):
            os.makedirs(accounts_dir)

        # Initialize accounts database
        self.initialize_accounts_database()

        # Load remembered account if exists
        self.remembered_account = self.load_remembered_account()

        self.setup_ui()

    def initialize_accounts_database(self):
        """Initialize the accounts database file if it doesn't exist"""
        if not os.path.exists(self.accounts_file):
            # Create empty accounts database
            accounts_data = {
                "users": {},
                "metadata": {
                    "total_accounts": 0,
                    "version": "1.0"
                }
            }
            self.save_accounts_data(accounts_data)

    def load_accounts_data(self):
        """Load accounts data from the JSON file"""
        try:
            with open(self.accounts_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file is corrupted or doesn't exist, create a new one
            return {
                "users": {},
                "metadata": {
                    "total_accounts": 0,
                    "version": "1.0"
                }
            }

    def save_accounts_data(self, accounts_data):
        """Save accounts data to the JSON file"""
        try:
            with open(self.accounts_file, 'w') as f:
                json.dump(accounts_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving accounts data: {e}")
            return False

    def load_remembered_account(self):
        """Load the remembered account from database"""
        accounts_data = self.load_accounts_data()
        for username, user_data in accounts_data["users"].items():
            if user_data.get("remember_password", False):
                return username
        return None

    def setup_ui(self):
        self.canvas = tk.Canvas(
            self.window,
            bg="#ffffff",
            width=1080,
            height=720,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        image_1 = tk.PhotoImage(file=load_asset("1.png"))
        self.canvas.create_image(540, 360, image=image_1)

        # Store images to prevent garbage collection
        self.images = {
            'button_new': tk.PhotoImage(file=load_asset("2.png")),
            'button_cancel': tk.PhotoImage(file=load_asset("4.png")),
            'button_login': tk.PhotoImage(file=load_asset("5.png")),
            'checkbox_unchecked': tk.PhotoImage(file=load_asset("6.png")),
            'checkbox_checked': tk.PhotoImage(file=load_asset("6.png"))
            # You can use different images for checked state
        }

        # New Account button
        button_new = tk.Button(
            image=self.images['button_new'],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            command=self.create_new_account
        )
        button_new.place(x=501, y=606, width=430, height=43)

        self.canvas.create_text(
            200,
            615,
            anchor="nw",
            text="Don't have an account?",
            fill="#ffffff",
            font=("Roboto", 24 * -1)
        )

        # Cancel button
        button_cancel = tk.Button(
            image=self.images['button_cancel'],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            command=self.cancel_login
        )
        button_cancel.place(x=682, y=427, width=353, height=40)

        # Login button
        button_login = tk.Button(
            image=self.images['button_login'],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            command=self.login
        )
        button_login.place(x=302, y=427, width=356, height=40)

        # Remember password checkbox - 3 TIMES BIGGER
        self.remember_var = tk.BooleanVar()

        # Password entry (with masking)
        self.password_var = tk.StringVar()
        self.password_var.trace('w', self.on_password_change)

        self.textarea_1 = tk.Entry(
            bd=0,
            bg="#000000",
            fg="#ffffff",
            insertbackground="#ffffff",
            highlightthickness=0,
            font=("Arial", 16),  # Consistent font with username
            show="*",  # Mask password with asterisks
            textvariable=self.password_var
        )
        self.textarea_1.place(x=291, y=244, width=744, height=44)
        self.textarea_1.bind('<KeyRelease>', self.on_password_key)

        # Username entry
        self.textarea_2 = tk.Entry(
            bd=0,
            bg="#000000",
            fg="#FFFFFF",
            insertbackground="#FFFFFF",
            highlightthickness=0,
            font=("Arial", 16)  # Consistent font with password
        )
        self.textarea_2.place(x=286, y=178, width=749, height=46)

        # Create custom checkbox - 3 times bigger than original (39x39 -> 117x117)
        self.checkbox = tk.Checkbutton(
            self.window,
            variable=self.remember_var,
            command=self.on_checkbox_toggle,
            bg="#ffffff",  # Match background
            activebackground="#ffffff",
            borderwidth=0,
            highlightthickness=0
        )

        self.checkbox.place(x=300, y=350, width=15, height=15)

        # Set initial checkbox state based on remembered account (AFTER creating textarea_2)
        if self.remembered_account:
            self.remember_var.set(True)
            # Auto-fill the remembered username
            self.textarea_2.insert(0, self.remembered_account)

        self.canvas.create_text(
            340,
            335,
            anchor="nw",
            text="Remember my password",
            fill="#ffffff",
            font=("Roboto", 32 * -1)
        )

        self.canvas.create_text(
            129,
            250,
            anchor="nw",
            text="Password",
            fill="#ffffff",
            font=("Roboto", 32 * -1)
        )

        self.canvas.create_text(
            59,
            178,
            anchor="nw",
            text="Account Name",
            fill="#ffffff",
            font=("Roboto", 32 * -1)
        )

        # Store references to prevent garbage collection
        self.window.image_1 = image_1

    def on_checkbox_toggle(self):
        """Handle checkbox state changes"""
        if self.remember_var.get():
            # Checkbox checked - remember current account
            current_username = self.textarea_2.get().strip()
            if current_username:
                self.update_remembered_account(current_username)
        else:
            # Checkbox unchecked - clear remembered account
            self.clear_remembered_account()

    def on_password_change(self, *args):
        """Handle password changes when remember me is checked"""
        if self.remember_var.get():
            current_username = self.textarea_2.get().strip()
            if current_username:
                self.update_remembered_account(current_username)

    def on_password_key(self, event):
        """Handle password field key events"""
        # You can add additional password field handling here if needed
        pass

    def update_remembered_account(self, username):
        """Update the remembered account in the database"""
        try:
            accounts_data = self.load_accounts_data()
            if username in accounts_data["users"]:
                # Set remember_password to True for this user
                accounts_data["users"][username]["remember_password"] = True
                # Clear remember_password for all other users
                for other_user in accounts_data["users"]:
                    if other_user != username:
                        accounts_data["users"][other_user]["remember_password"] = False

                self.save_accounts_data(accounts_data)
                self.remembered_account = username
        except Exception as e:
            print(f"Error updating remembered account: {e}")

    def clear_remembered_account(self):
        """Clear all remembered accounts"""
        try:
            accounts_data = self.load_accounts_data()
            for username in accounts_data["users"]:
                accounts_data["users"][username]["remember_password"] = False

            self.save_accounts_data(accounts_data)
            self.remembered_account = None
        except Exception as e:
            print(f"Error clearing remembered accounts: {e}")

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def account_exists(self, username):
        """Check if account exists in the database"""
        accounts_data = self.load_accounts_data()
        return username in accounts_data["users"]

    def create_new_account(self):
        """Create a new account based on the information in textboxes"""
        username = self.textarea_2.get().strip()
        password = self.password_var.get().strip()

        # Validate input
        if not username:
            messagebox.showerror("Error", "Please enter a username!")
            return

        if not password:
            messagebox.showerror("Error", "Please enter a password!")
            return

        if len(username) < 3:
            messagebox.showerror("Error", "Username must be at least 3 characters long!")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long!")
            return

        # Check if account already exists
        if self.account_exists(username):
            messagebox.showerror("Error", "Account already exists!")
            return

        try:
            # Load current accounts data
            accounts_data = self.load_accounts_data()

            # Create new account
            accounts_data["users"][username] = {
                "password_hash": self.hash_password(password),
                "remember_password": self.remember_var.get(),
                "created_at": self.get_current_timestamp()
            }

            # If remember me is checked, clear other remembered accounts
            if self.remember_var.get():
                for other_user in accounts_data["users"]:
                    if other_user != username:
                        accounts_data["users"][other_user]["remember_password"] = False

            # Update metadata
            accounts_data["metadata"]["total_accounts"] = len(accounts_data["users"])

            # Save updated accounts data
            if self.save_accounts_data(accounts_data):
                messagebox.showinfo("Success", "Account created successfully!")
                print(f"New account created: {username}")

                # Clear fields after successful creation
                self.textarea_2.delete(0, tk.END)
                self.password_var.set("")

                # Update remembered account
                if self.remember_var.get():
                    self.remembered_account = username
            else:
                messagebox.showerror("Error", "Failed to save account data!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {str(e)}")

    def login(self):
        """Login with existing account"""
        username = self.textarea_2.get().strip()
        password = self.password_var.get().strip()

        # Validate input
        if not username:
            messagebox.showerror("Error", "Please enter your username!")
            return

        if not password:
            messagebox.showerror("Error", "Please enter your password!")
            return

        # Check if account exists
        if not self.account_exists(username):
            messagebox.showerror("Error", "Account does not exist!")
            return

        try:
            # Load accounts data
            accounts_data = self.load_accounts_data()
            user_data = accounts_data["users"][username]

            # Verify password
            if user_data["password_hash"] == self.hash_password(password):
                messagebox.showinfo("Success", f"Welcome back, {username}!")
                print(f"User logged in: {username}")

                # Update remember password setting if changed
                if user_data["remember_password"] != self.remember_var.get():
                    user_data["remember_password"] = self.remember_var.get()
                    accounts_data["users"][username] = user_data

                    # If remembering, clear other remembered accounts
                    if self.remember_var.get():
                        for other_user in accounts_data["users"]:
                            if other_user != username:
                                accounts_data["users"][other_user]["remember_password"] = False

                    self.save_accounts_data(accounts_data)

                # Close login window and open statistic
                self.open_statistic_after_login()

            else:
                messagebox.showerror("Error", "Invalid password!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to login: {str(e)}")

    def open_statistic_after_login(self):
        """Close login window and open statistic.py"""
        self.window.destroy()
        # Open statistic.py
        subprocess.Popen([sys.executable, "statistic.py"])

    def get_current_timestamp(self):
        """Get current timestamp for account creation"""
        return datetime.datetime.now().isoformat()

    def cancel_login(self):
        """Close the login window"""
        self.window.quit()
        self.window.destroy()

    def run(self):
        """Run the application"""
        self.window.resizable(False, False)
        self.window.mainloop()


def main():
    login_system = LoginSystem()
    login_system.run()


if __name__ == "__main__":
    main()