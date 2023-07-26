import tkinter as tk
import random
import pandas as pd
import mysql.connector
import sys


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
            user=sys.argv[1],
            password=sys.argv[2],
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
        self.clear_screen()
        self.root.title(f"MyPWD Manager / {username}")
        string = f"\nWelcome to MyPWD Manager, {username}!\n"
        self.welcome_label = tk.Label(self.root, text=string, font=self.font)
        self.welcome_label.pack()

        self.add_label = tk.Button(self.root, text="Add".format(username),
                                   font=self.font, command=self.add)
        self.add_label.pack()

        self.check_label = tk.Button(self.root, text="Check".format(username),
                                     font=self.font, command=self.check)
        self.check_label.pack()

    def add(self):
        self.clear_screen()

        string = f"Welcome to MyPWD Manager, {username}!\n"
        self.welcome_label = tk.Label(self.root, text=string, font=self.font)
        self.welcome_label.pack()

        self.website_label = tk.Label(self.root, text="Website:", font=self.font)
        self.website_label.pack()

        self.website_entry = tk.Entry(self.root, font=self.font)
        self.website_entry.pack()

        gen_pwd = generate_password()
        self.password_generated_label = tk.Label(self.root, text=f"Generated Password: {gen_pwd}",
                                                 font=self.font)
        self.password_generated_label.pack()

        self.copy_button = tk.Button(self.root, text="Copy Pwd", font=self.font, command=lambda: self.copy(gen_pwd))
        self.copy_button.pack()

        self.add_to_db = tk.Button(self.root, text="Add to DB", font=self.font,
                                   command=lambda: self.add_data(gen_pwd, self.website_entry.get()))

        self.add_to_db.pack()

        self.back_button = tk.Button(self.root, text="<- Back", font=self.font, command=self.login)
        self.back_button.pack()

    def copy(self, txt):
        self.root.clipboard_clear()
        self.root.clipboard_append(txt)

    def check(self):
        self.clear_screen()

        string = f"Welcome to MyPWD Manager, {username}!\n"
        self.welcome_label = tk.Label(self.root, text=string, font=self.font)
        self.welcome_label.pack()

        website_list_options = ['-']

        self.cursor.execute(f"SELECT website FROM {self.website_table};")
        df = pd.DataFrame(self.cursor.fetchall())
        df.rename(columns={0: 'website'}, inplace=True)

        for website in df['website']:
            website_list_options.append(website)

        self.website_label = tk.Label(self.root, text="Website:", font=self.font)
        self.website_label.pack()

        self.option_var = tk.StringVar(self.root)
        self.option_var.set(website_list_options[0])

        self.option_menu = tk.OptionMenu(self.root, self.option_var, *website_list_options)
        self.option_menu.pack()

        self.go = tk.Button(self.root, text="Check Pwd".format(username), font=self.font, command=self.check_db)
        self.go.pack()

        self.back_button = tk.Button(self.root, text="<- Back", font=self.font, command=self.login)
        self.back_button.pack()

    def add_data(self, pwd, web):
        self.cursor.execute(f"INSERT INTO website_data (website, password) VALUES ('{web}', '{pwd}');")
        self.connection.commit()

        self.clear_screen()

        self.login()

    def check_db(self):
        website = self.option_var.get()
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
        self.clear_screen()
        self.login()

    def check_cred(self):
        global username
        global password
        global logged
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.cursor.execute(f"SELECT * FROM {self.authentication_table} WHERE username='{username}'")
        row = self.cursor.fetchone()

        if row and password == row[2]:
            self.clear_screen()
            self.login()
        else:
            self.error_label.config(text="Invalid Username and/or Password")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    App = MyPasswordManager()
