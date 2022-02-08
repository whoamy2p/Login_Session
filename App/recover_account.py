#! usr/bin/env python3

from tkinter import *
from tkinter import ttk, messagebox
from pack_method.method import Generate_code, time_window, methods, data_encrypt
from pack_method.conection_db import request_db

class Recover:
    validate = methods ()
    dt = time_window ()
    encrypt = data_encrypt ()

    def generate_code (self):
        root = Tk ()
        root.iconbitmap ("App/media/img/icon/icon_Logo.ico")
        root.resizable (False, False)
        root.title ("Generate Code")

        container_ = Frame (root)
        container_.grid (row=0, column=0, padx=10, pady=10)

        Label (container_, text="I forgot the password. I want to receive a\n verification code to change my password\n", font=("Cambria 12"), background="#EEEEEE").grid (row=0, column=0, columnspan=2, sticky=W+E)

        Label (container_, text="Username *", font=("Cambria 12 bold"), background="#EEEEEE").grid (row=1, column=0, sticky=W, pady=10, padx=3)
        self.email = Entry (container_, font=("Cambria 12"), borderwidth=0, foreground="blue", width=28, justify=CENTER, background="#EEEEEE")
        self.email.grid (row=2, column=0, pady=5, columnspan=2)
        ttk.Separator (container_, orient="horizontal").grid (row=3, column=0, columnspan=2, sticky=W+E, pady=2, padx=10)

        self.message_username = Label (container_, font=("Cambria 11"), foreground="red")
        self.message_username.grid (row=4, column=0, columnspan=2, pady=2, padx=10)

        # #319B72  color turquesa oscuro
        Button (container_, text="Generate code", bd=1, font=("Cambria 12 bold"), activebackground="black", activeforeground="black", background="#319B72", foreground="white", width=13, command=lambda: Generate_code(self.email.get (), self.message_username)).grid (row=5, column=1, pady=8, sticky=E)

        Label (container_, text="\nEnter the verification code", font=("Cambria 12"), background="#EEEEEE").grid (row=6, column=0, columnspan=2, pady=13)

        Code = Entry (container_, font= ("Cambra 12"), bd=0, width=28, justify=CENTER, background="#EEEEEE")
        Code.grid (row=7, column=0, columnspan=2)#, background="#EEEEEE"
        ttk.Separator (container_, orient="horizontal").grid (row=8, column=0, columnspan=2, sticky=W+E, pady=2, padx=10)

        self.message_code = Label (container_, font=("Cambria 11"), foreground="red")
        self.message_code.grid (row=9, column=0, columnspan=2, pady=2, padx=10)

        Button (container_, text="Check", bd=1, font=("Cambria 12 bold"), activebackground="black", activeforeground="black", background="#319B72", foreground="white", width=13, command=lambda: self.validate.validate_code (Code.get (), root, self.message_code, self.Change_password, self.email.get (), self.encrypt)).grid (row=10, column=1, pady=8, sticky=E)

        root.mainloop ()
    
    def Change_password (self, email):
        self.user_email = email
        self.window_password = Toplevel ()
        self.window_password.iconbitmap ("App/media/img/icon/icon_Logo.ico")
        self.window_password.title ("Reset Email")

        container_reset = Frame (self.window_password)
        container_reset.grid (row=0, column=0, padx=10, pady=10)

        Label (container_reset, text="RESET EMAIL", font=("Cambria 14 bold"), foreground="black").grid (row=0, column=0, columnspan=2, padx=10, pady=15)

        email_set = Label (container_reset, text=f"{self.user_email}", font=("Cambria 13 bold"), foreground="blue")
        email_set.grid (row=1, column=0, columnspan=2, padx=10, pady=15)

        Label (container_reset, text="New Password", font=("Cambria 12"), foreground="black").grid (row=2, column=0, columnspan=2, padx=10, pady=15, sticky=W)

        self.new_password = Entry (container_reset, font= ("Cambra 12"), bd=0, width=28, justify=CENTER, background="#EEEEEE")
        self.new_password.grid (row=3, column=0, columnspan=2)#
        ttk.Separator (container_reset, orient="horizontal").grid (row=4, column=0, columnspan=2, sticky=W+E, pady=2, padx=10)

        Label (container_reset, text="Confirm Password", font=("Cambria 12"), foreground="black").grid (row=5, column=0, columnspan=2, padx=10, pady=15, sticky=W)

        self.confirm_password = Entry (container_reset, font= ("Cambra 12"), bd=0, width=28, justify=CENTER, background="#EEEEEE")
        self.confirm_password.grid (row=6, column=0, columnspan=2)#
        ttk.Separator (container_reset, orient="horizontal").grid (row=7, column=0, columnspan=2, sticky=W+E, pady=2, padx=10)

        self.message_password = Label (container_reset, font=("Cambria 11"), foreground="red")
        self.message_password.grid (row=8, column=0, columnspan=2, pady=2, padx=10)

        Button (container_reset, text="Send", bd=1, font=("Cambria 12 bold"), activebackground="black", activeforeground="black", background="#319B72", foreground="white", width=13, command=lambda: self.__send_password ()).grid (row=9, column=1, pady=15, sticky=E, padx=10)
    
    def __send_password (self):
        if self.new_password.get () == self.confirm_password.get ():
            __data = {
                "new_password": self.new_password.get (),
                "updated": self.dt.input_time (),
                "username": self.user_email
                }

            data_update = self.encrypt.Encrypt (__data)
            query = "UPDATE Auth_Users SET PASSWORD=?, UPDATED=? WHERE USERNAME=?"

            request_db (query, data_update)
            self.window_password.destroy ()

            messagebox.showinfo (title="Password changed", message=f"'{self.user_email}' account password has been\nchanged successfully")

        
        else:
            self.message_password.config (text="Passwords are not the same")
