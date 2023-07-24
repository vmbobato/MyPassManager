import tkinter as tk
import random
import mysql.connector


def generate_password():
    alpha = "abcdefghijklmnopqrstuvwxyz"
    alphaCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num = "1234567890"
    spc_char = "[]{}\?!@#%&*()/=+"
    pwd = alpha + alphaCase + num + spc_char
    pwd = "".join(random.sample(pwd, 17))
    return pwd


class MyPasswordManager:
    def __init__(self):
        self.root = tk.Tk()
        self.font = ("Arial", 14)
        self.username_entry = None
        self.password_entry = None
        self.username_label = None
        self.password_label = None
        self.submit_button = None
        self.error_label = None
        self.add_label = None
        self.check_label = None
        self.logout_label = None
        self.website_entry = None
        self.website_label = None
        self.password_generated_label = None
        self.add_to_db = None
        self.welcome_label = None
        self.pwd_label = None
        self.go = None
        self.done_bt = None
        self.alert = None
        self.copy_button = None
        self.database = 'mypassmanager'
        self.authentication_table = 'auth'
        self.website_table = 'website_data'

        # customize the window
        self.root.title("MyPWD Manager - Login")
        self.root.geometry("400x300")

        # calculate the x and y coordinates to center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.root.winfo_reqwidth()) // 2
        y = (screen_height - self.root.winfo_reqheight()) // 2
        self.root.geometry("+{}+{}".format(x, y))

        # Initialize MySQL API
        self.connection = mysql.connector.connect(
            user="root",
            password="root",
            database=self.database
        )
        self.cursor = self.connection.cursor()

        self.main()
        self.root.mainloop()

    def main(self):
        self.root.title(f"MyPWD Manager")
        self.username_label = tk.Label(self.root, text="Username:", font=self.font)
        self.username_label.pack()
        self.username_entry = tk.Entry(self.root, font=self.font)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Password:", font=self.font)
        self.password_label.pack()
        self.password_entry = tk.Entry(self.root, show="*", font=self.font)
        self.password_entry.pack()

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_cred, font=self.font)
        self.submit_button.pack()

        self.error_label = tk.Label(self.root, fg="red", font=self.font)
        self.error_label.pack()

    def login(self):
        self.error_label.config(text="")
        self.root.title(f"MyPWD Manager / {username}")
        self.username_label.destroy()
        self.username_entry.destroy()
        self.password_label.destroy()
        self.password_entry.destroy()
        self.submit_button.destroy()
        string = f"Welcome to MyPWD Manager, {username}!\n"
        self.welcome_label = tk.Label(self.root, text=string, font=self.font)
        self.welcome_label.pack()

        self.add_label = tk.Button(self.root, text="Add".format(username),
                                   font=self.font, command=self.add)
        self.add_label.pack()

        self.check_label = tk.Button(self.root, text="Check".format(username),
                                     font=self.font, command=self.check)
        self.check_label.pack()

    def add(self):
        self.add_label.destroy()
        self.check_label.destroy()

        self.website_label = tk.Label(self.root, text="Website:", font=self.font)
        self.website_label.pack()

        self.website_entry = tk.Entry(self.root, font=self.font)
        self.website_entry.pack()

        gen_pwd = generate_password()
        self.password_generated_label = tk.Label(self.root, text="Generated Password: " + gen_pwd,
                                                 font=self.font)
        self.password_generated_label.pack()

        self.copy_button = tk.Button(self.root, text="Copy Pwd", font=self.font, command=lambda: self.copy(gen_pwd))
        self.copy_button.pack()

        self.add_to_db = tk.Button(self.root, text="Add to DB", font=self.font,
                                   command=lambda: self.add_data(gen_pwd, self.website_entry.get()))

        self.add_to_db.pack()

    def copy(self, txt):
        self.root.clipboard_clear()
        self.root.clipboard_append(txt)

    def check(self):
        self.add_label.destroy()
        self.check_label.destroy()

        self.website_label = tk.Label(self.root, text="Website:", font=self.font)
        self.website_label.pack()
        self.website_entry = tk.Entry(self.root, font=self.font)
        self.website_entry.pack()

        self.go = tk.Button(self.root, text="Check DB!".format(username), font=self.font, command=self.check_db)
        self.go.pack()

    def add_data(self, pwd, web):
        self.cursor.execute(f"INSERT INTO website_data (website, password) VALUES ('{web}', '{pwd}');")
        self.connection.commit()

        self.copy_button.destroy()
        self.add_to_db.destroy()
        self.website_entry.destroy()
        self.website_label.destroy()
        self.password_generated_label.destroy()
        self.password_generated_label.destroy()
        self.welcome_label.destroy()

        self.main()

    def check_db(self):
        website = self.website_entry.get()
        self.cursor.execute(f"SELECT * FROM {self.website_table} WHERE website='{website}'")
        pwd = self.cursor.fetchone()

        if pwd:
            self.pwd_label = tk.Label(self.root, text=f"Password: {pwd[2]}", font=self.font)
            self.pwd_label.pack()
            self.copy_button = tk.Button(self.root, text="Copy Pwd", font=self.font, command=lambda: self.copy(pwd[2]))
            self.copy_button.pack()
            self.done_bt = tk.Button(self.root, text="Done", font=self.font, command=self.clear_check)
            self.done_bt.pack()
        else:
            self.alert = tk.Label(self.root, text="Website Not Found", font=self.font)
            self.alert.pack()

    def clear_check(self):
        if self.alert:
            self.alert.destroy()
        self.copy_button.destroy()
        self.website_entry.destroy()
        self.pwd_label.destroy()
        self.done_bt.destroy()
        self.website_label.destroy()
        self.go.destroy()
        self.welcome_label.destroy()
        self.main()

    def check_cred(self):
        global username
        global password
        global logged
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.cursor.execute(f"SELECT * FROM {self.authentication_table} WHERE username='{username}'")
        row = self.cursor.fetchone()

        if row and password == row[2]:
            self.username_label.destroy()
            self.username_entry.destroy()
            self.password_label.destroy()
            self.password_entry.destroy()
            self.submit_button.destroy()
            self.login()
        else:
            self.error_label.config(text="Invalid Username and/or Password")


if __name__ == "__main__":
    App = MyPasswordManager()
