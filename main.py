import tkinter as tk
import random
import json


def generate_password():
    alpha = "abcdefghijklmnopqrstuvwxyz"
    alphaCase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num = "1234567890"
    spc_char = "[]{}\?!@#%&*()/=+"
    pwd = alpha + alphaCase + num + spc_char
    pwd = "".join(random.sample(pwd, 14))
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

        # customize the window
        self.root.title("MyPWD Manager - Login")
        self.root.geometry("400x300")

        # calculate the x and y coordinates to center the window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.root.winfo_reqwidth()) // 2
        y = (screen_height - self.root.winfo_reqheight()) // 2
        self.root.geometry("+{}+{}".format(x, y))

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
        string = f"Welcome to MyPWD Manager, {username}!\n\n"
        self.welcome_label = tk.Label(self.root, text=string, font=self.font)
        self.welcome_label.pack()

        self.add_label = tk.Button(self.root, text="ADD".format(username),
                                   font=self.font, command=self.add)
        self.add_label.pack()

        self.check_label = tk.Button(self.root, text="CHECK".format(username),
                                     font=self.font, command=self.check)
        self.check_label.pack()

    def add(self):
        self.add_label.destroy()
        self.check_label.destroy()

        self.website_label = tk.Label(self.root, text="Website:", font=self.font)
        self.website_label.pack()

        self.website_entry = tk.Entry(self.root, font=self.font)
        self.website_entry.pack()

        password_generated = generate_password()
        self.password_generated_label = tk.Label(self.root, text="Generated Password: " + password_generated,
                                                 font=self.font)
        self.password_generated_label.pack()

        self.add_to_db = tk.Button(self.root, text="ADD to DB".format(username), font=self.font,
                                   command=lambda: self.add_data(password_generated, self.website_entry.get()))

        self.add_to_db.pack()

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
        data = {web: pwd}
        with open(web + '.json', 'w') as out:
            json.dump(data, out)
            out.close()
        self.add_to_db.destroy()
        self.website_entry.destroy()
        self.website_label.destroy()
        self.password_generated_label.destroy()
        self.password_generated_label.destroy()
        self.welcome_label.destroy()

        self.main()

    def check_db(self):
        website = self.website_entry.get()
        try:
            with open(website + '.json', 'r') as check_file:
                pwd_data = json.load(check_file)
                check_file.close()
            passwd = pwd_data.get(website)
            self.pwd_label = tk.Label(self.root, text="Password: " + passwd, font=self.font)
            self.pwd_label.pack()
            self.done_bt = tk.Button(self.root, text="Done", font=self.font, command=self.clear_check)
            self.done_bt.pack()
        except FileNotFoundError:
            self.alert = tk.Label(self.root, text="Website Not Found", font=self.font)
            self.alert.pack()

    def clear_check(self):
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
        if username == "vmb" and password == "root":
            self.username_label.destroy()
            self.username_entry.destroy()
            self.password_label.destroy()
            self.password_entry.destroy()
            self.submit_button.destroy()
            self.login()
        else:
            self.error_label.config(text="Invalid Username and/or Password")


App = MyPasswordManager()
