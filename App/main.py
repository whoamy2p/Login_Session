#! /usr/bin/env python3

from sys import path
path.append('..\\login_session')

from tkinter import *
from tkinter import ttk

from pack_method.method import time_window, data_encrypt, methods
from pack_method.conection_db import request_db, Insert_dataDB_users
from App.recover_account import Recover

class Login:
    sesion = False
    user_get = 0
    validator = methods ()
    encryptCode = data_encrypt ()
    recover = Recover ()

    def __init__(self):
        self.window = Tk ()
        self.window.title ("Login")
        self.window.iconbitmap ("App/media/img/icon/icon_Logo.ico")
        self.window.resizable (False, False)

        # -------   Cargamos un imagen de fondo en un label ----------------
        self.img = PhotoImage (file="App/media/img/port_login_800x700.png")
        Label (self.window, image=self.img ).grid (row=1, column=0, rowspan=2)

        # ---------- Creamos el contenedor contenedor del formulario
        self.container_login = Frame (self.window)
        self.container_login.place (x=230, y=115)

        self.img_circle_per = PhotoImage (file="App/media/img/perfil_login_180x180.png")
        self.foto = Label (self.container_login, image=self.img_circle_per, background="#EEEEEE").grid(row=0, column=1, pady=20)

        # ------------ Creamo un subcontenedor del formulario ---------------
        self.forms = Frame (self.container_login, bd=7, cursor="hand2")
        self.forms.grid (row=6, column=1, padx=15, sticky=N)

        Label (self.forms, text="Username *", font=("Cambria 12 bold")).grid (row=1, column=0, pady=8, sticky=W)
        self.email = Entry (self.forms, font=("Cambria 12 bold"), justify=CENTER, width=35, borderwidth=0, background="#EEEEEE")
        self.email.grid (row=2, column=0, sticky=W+E, pady=3, columnspan=2, ipady=6)
        ttk.Separator (self.forms, orient="horizontal").grid (row=3, column=0, columnspan=2, sticky=W+E)

        Label (self.forms, text="Password *", font=("Cambria 12 bold")).grid (row=4, column=0, pady=8, sticky=W)
        self.password = Entry (self.forms, font=("Cambria 12 bold"), justify=CENTER, show="*", bd=0, width=35, background="#EEEEEE")
        self.password.grid (row=5, column=0, sticky=W+E, pady=3, columnspan=2, ipady=6)
        ttk.Separator (self.forms, orient="horizontal").grid (row=6, column=0, columnspan=2, sticky=W+E)

        Button (self.forms, text="Did you forget your password?", relief=GROOVE, foreground="blue", bd=0, command=lambda: self.recover.generate_code ()).grid (row=7, column=1, sticky=W+E)

        self.Message_login = Label (self.forms, font=("Cambria 12"), foreground="red", background="#EEEEEE")
        self.Message_login.grid (row=8, column=0, columnspan=2, sticky=W+E, padx=4, pady=8)

        # botones de enviar y registrar
        Button (self.forms, text="Submit", font=("Cambria 12 bold"), activebackground="black", activeforeground="white", bg=None, relief="raise", bd=2, width=8, background="#3E77B6", command= lambda: self.__login_validator ()).grid (row=9, column=0, sticky=E+W, pady=15, padx=5)

        Button (self.forms, text="Sign up",font=("Cambria 12 bold"), activebackground="black", activeforeground="white", bg=None, relief="raise", bd=2, width=8, background="#9933FF", command=lambda: self.register ()).grid (row=9, column=1, sticky=W+E, pady=15, padx=5)
        
        self.window.mainloop ()

    """
    Metodo valida el usuario y contraseña con la DDBB
    """
    def __login_validator (self):
        email_r = self.email.get ()
        password_r = self.password.get ()

        # ****** Realizamos la consulta SQL **********
        query = "SELECT PASSWORD, USERNAME, NAME, LAST_NAME, ID FROM Auth_Users WHERE USERNAME='{}'".format (self.encryptCode.encrypt_one (email_r))

        # Devuelve un lista y dentro una tupla con los datos[()]
        data_result = list(request_db (query))
        if data_result:
            # ** Desencriptamos los datos que nos ha devuelto (contraseña, usuario, nombre, apellido, ID)
            data_db = self.encryptCode.Desencrypt ([data_result[0][0], data_result[0][1], data_result[0][2], data_result[0][3]])
            
            # le añadimos valores a estas variables de clases
            self.name_user = f"{data_db[2]} {data_db[3]}"
            self.user_id = data_result[0][4] 

            if self.validator.validate_email (email_r, data_db[1]) and self.validator.validate_password (password_r, data_db[0]):
                self.sesion = True
                self.window.destroy ()
            
            else:
                self.Message_login.config (text="Incorrect password")
                return False
        else:
            if not self.validator.validate_email (email_r, email_r):
                self.Message_login.config (text="Incorrect email")
            
            else:
                self.Message_login.config (text="Unregistered user")

    """
        METODO QUE CONTRUYE EL FORMULARIO DE REGISTRO
    """

    def register (self):
        self.window_register = Toplevel ()
        self.window_register.title ("Register")
        self.window_register.geometry ("1097x765")
        self.window_register.iconbitmap ("App/media/img/icon/icon_Logo.ico")
        self.window_register.resizable (False, False)
        self.window_register.config (background="#006666")

        # ----------- Contenedor de la imagen y formulario ---------------------
        self.container_form = Frame (self.window_register)
        self.container_form.place (x=80, y=50)

        self.background_img = PhotoImage (file="App/media/img/img_register_600x650.png")
        Label (self.container_form, image=self.background_img ,width=475, height=660).grid (row=0, column=0)

        # -------------- Contendor solo del formulario -----------------------
        self.container_register = Frame (self.container_form, bd=7, cursor="hand2")
        self.container_register.grid (row=0, column=1, sticky=N+S+W+E)

        Label (self.container_register, text="Sign up", font=("Forte 25 bold"), foreground="Purple", background="#EEEEEE", pady=11).grid (row=0, column=0, columnspan=2, sticky=W+E)

        Label (self.container_register, text="Name *", font=("Cambria 12 bold")).grid (row=1, column=0, pady=8, sticky=W, padx=5)
        self.name = Entry (self.container_register, font=("Cambria 12"), justify=CENTER, borderwidth=0, background="#EEEEEE")
        self.name.grid (row=2, column=0, sticky=W+E, pady=3, padx=5)
        ttk.Separator (self.container_register, orient="horizontal").grid (row=3, column=0, sticky=W+E, padx=5)

        Label (self.container_register, text="Last Name *", font=("Cambria 12 bold")).grid (row=1, column=1, pady=8, sticky=W, padx=5)
        self.last_name = Entry (self.container_register, font=("Cambria 12"), justify=CENTER, borderwidth=0, background="#EEEEEE")
        self.last_name.grid (row=2, column=1, sticky=W+E, pady=3, padx=5)
        ttk.Separator (self.container_register, orient="horizontal").grid (row=3, column=1, sticky=W+E, padx=5)

        Label (self.container_register, text="Username *", font=("Cambria 12 bold")).grid (row=4, column=0, columnspan=2, pady=8, sticky=W, padx=5)
        self.username = Entry (self.container_register, font=("Cambria 12"), justify=CENTER, borderwidth=0, background="#EEEEEE")
        self.username.grid (row=5, column=0, columnspan=2, sticky=W+E, pady=3, padx=5)
        ttk.Separator (self.container_register, orient="horizontal").grid (row=6, column=0, sticky=W+E, columnspan=2, padx=5)

        self.message_username = Label (self.container_register, font=("Ca,bria 12"), foreground="red", background="#EEEEEE")
        self.message_username.grid (row=7, column=0, columnspan=2, sticky=W+E, padx=5)

        Label (self.container_register, text="Passwword *", font=("Cambria 12 bold")).grid (row=8, column=0, columnspan=2, pady=8, sticky=W, padx=5)
        self.password_2 = Entry (self.container_register, font=("Cambria 12"), justify=CENTER, show="*", borderwidth=0, background="#EEEEEE")
        self.password_2.grid (row=9, column=0, columnspan=2, sticky=W+E, pady=3, padx=5)
        ttk.Separator (self.container_register, orient="horizontal").grid (row=10, column=0, sticky=W+E, columnspan=2, padx=5)

        Label (self.container_register, text="Password confirmation *", font=("Cambria 12 bold")).grid (row=11, column=0, columnspan=2, pady=8, sticky=W, padx=5)
        self.Password_confirmation= Entry (self.container_register, font=("Cambria 12"), justify=CENTER, show="*", borderwidth=0, background="#EEEEEE")
        self.Password_confirmation.grid (row=12, column=0, columnspan=2, sticky=W+E, pady=3, padx=5)
        ttk.Separator (self.container_register, orient="horizontal").grid (row=13, column=0, sticky=W+E, columnspan=2, padx=5)

        self.message_passwordw = Label (self.container_register, font=("Ca,bria 12"), foreground="red", background="#EEEEEE")
        self.message_passwordw.grid (row=14, column=0, columnspan=2, sticky=W+E, padx=5)

        # ------------- Contenedor de fechas -----------------
        Label (self.container_register, text="Date of birth *", font=("Cambria 12 bold")).grid (row=15, column=0, columnspan=2, pady=8, sticky=W, padx=5)

        self.frame1 = Frame (self.container_register)
        self.frame1.grid (row=16, column=0, columnspan=2, sticky=W+E, padx=10)

        self.day = ttk.Combobox (self.frame1, values=("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"),  width=9, font=("Cambria 12"))
        self.day.grid (row=0, column=0, sticky=W+E, ipady=3, pady=3, padx=15)
        self.month = ttk.Combobox (self.frame1, values=("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"), width=10, font=("Cambria 12"))
        self.month.grid (row=0, column=1, sticky=W+E, ipady=3, pady=3, padx=15)
        self.year = ttk.Combobox (self.frame1, values=("1970", "1971", "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979", "1980","1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2005", "2006", "2007", "2008", "2009","2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"),  width=9, font=("Cambria 12"))
        self.year.grid (row=0, column=2, sticky=W+E, ipady=3, pady=3, padx=15)

        Label (self.container_register, text="Sex *", font=("Cambria 12 bold")).grid (row=17, column=0, columnspan=2, pady=3, sticky=W, padx=20)

        self.frame_sex = Frame (self.container_register)
        self.frame_sex.grid (row=18, column=0, columnspan=2, padx=10)
        self.option = StringVar ()
        self.women = Radiobutton (self.frame_sex, text="Woman", variable=self.option, value="Woman", font=("Cambria 12"))
        self.women.grid (row=0, column=0, padx=20)

        self.man = Radiobutton (self.frame_sex, text="Man", variable=self.option, value="Man", font=("Cambria 12"))
        self.man.grid (row=0, column=1, padx=20)

        self.other = Radiobutton (self.frame_sex, text="Others", variable=self.option, value="Others", font=("Cambria 12"))
        self.other.grid (row=0, column=2, padx=20)

        robot = IntVar ()
        self.check = Checkbutton (self.container_register, text="I am not a robot", variable=robot, onvalue=1, offvalue=0, font=("Cambria 12 bold"), foreground="Blue")
        self.check.grid (row=19, column=0, sticky=W+E, padx=5, pady=3)

        #  #00FFFF : color turquesa
        Button (self.container_register, text="Submit", font=("Cambria 12 bold"), activebackground="black", activeforeground="white", bg="#00FFFF", relief="raise", width=16, bd=1, command=lambda: Insert_dataDB_users (self.__captureForm (), self.validator, self.encryptCode, self.username.get (), self.window_register)).grid (row=20, column=1, pady=15)

        Button (self.container_register, text="Do you already have an account? Log in", relief=GROOVE, foreground="blue", command=lambda: self.window_register.destroy ()).grid (row=21, column=0, sticky=W+E, padx=5)


    # ------------ Método que captura y valida los datos del formulario de registro
    def __captureForm (self):
        email_regi = self.username.get ()
        password_regi = self.password_2.get ()
        password_regi_conf = self.Password_confirmation.get ()

        if self.validator.validate_email (email_regi, email_regi) and self.validator.validate_password (password_regi, password_regi_conf):
            self.data_gui = {
                "name":self.name.get (), 
                "last_name":self.last_name.get (), 
                "username":self.username.get (), 
                "password":self.password_2.get (),  
                "date": "{}/{}/{}".format (self.day.get (), self.month.get (), self.year.get ()), 
                "genero":self.option.get (), 
                "created": time_window.input_time (self),
                "updated": time_window.input_time (self)
            }

            return self.data_gui
        
        else:
            if self.validator.validate_email (email_regi, email_regi):
                self.message_username.config (text="Email incorrect")
            
            elif password_regi != password_regi_conf:
                self.message_passwordw.config (text="Password incorrect")



if __name__ == "__main__":
    objet = Login ()