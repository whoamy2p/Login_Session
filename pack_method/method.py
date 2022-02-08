#! /usr/bin/env python3

from datetime import datetime
import re
from random import randrange
from tkinter import END, messagebox

import httplib2
from pack_method.conection_db import request_db, Insert_codeDB, Read_dataDB_Users
from App.APIS.gmail import email_send

dtt = datetime.now ()

class methods:

    """
        Método que valida los correos ingresados desde la interfaz y
        corrobora si ese usuario ingresado esta registrado o no en la Aplicación
    """
    def validate_email (self, email, email_con):
        if re.findall ("[@]gmail.com$", email) or re.findall ("[@]outlook.com$", email) or re.findall ("[@]yahoo.com$", email):
            if email == email_con:
                return True
            else:
                return False
        
        else:
            return False

    """
        Método que valida las contraseñas ingresados desde la interfaz y
        corrobora si es la contraseña de ese usuario x
    """
    def validate_password (self, password, password_con):
        if password == password_con:
            return True

        else:
            return False

    """
        Método que valida que todos los campos de un formmulario este llenado
    """
    def validate_data (self, data):
        for value in data.values():
            value = str (value)
            if value.isspace () or value == "":
                return False
                
        else:
            return True
    
    """
         Método que permite validar el codigo generado para restaurar la contraseña 
    """

    def validate_code (self, code, window, message, change_password, email, encrypt):
        query = "SELECT CODE, ID_USR FROM Code_Verfication WHERE CODE=?"
        code = int(code)
        RESULT = request_db (query, (code,))
        id_usr = Read_dataDB_Users (encrypt.encrypt_one(email))
        
        for k in RESULT:
            v = list(filter (lambda x: x.isdigit (), str(k[0])))
            
            if code == k[0] and len(v) == 6 and k[1] == id_usr[0]:
                window.destroy ()
                change_password (email)

            else:
                message.config (text="Code is incorrect")
        


# ************ metodos de hora y fecha ***********************

class time_window:
    def input_time (self):
        dt = datetime.now ()
        if dt.month <= 9:
            return "{}/0{}/{}".format (dt.day, dt.month, dt.year)
        
        return "{}/{}/{}".format (dt.day, dt.month, dt.year)

    def input_hour (self):
        dt = datetime.now ()
        return "{}:{}:{}".format (dt.hour, dt.minute, dt.second)


# ***************** MÉTODOS DE ECRIPTACIÓN Y DESENCRIPTACIÓN *******************

class data_encrypt:
    def Encrypt (self, dictionary):
        encrypt = []

        for data in dictionary.values ():
            result = ""
            for element in data:
                if element.isspace ():
                    result += element
                    continue

                code = ord (element) + 5

                result += chr(code)
            encrypt.append (result)
        
        return encrypt

    def Desencrypt (self, lista):
        desencrypt = []

        for data in lista:
            result = ""
            for element in str(data):
                if element.isspace ():
                    result += element
                    continue
                    
                code = ord (element) - 5
                result += chr(code)

            desencrypt.append (result)

        return desencrypt


    def encrypt_one (self, parameter):
        data_message = ""

        for element in parameter:
            if element.isspace ():
                data_message += element
                continue
                
            code = ord (element) + 5
            data_message += chr(code)

        return data_message

"""
    Metodo que genera el codigo unico
"""
def random_code ():
    random = ""
    contador = 0
    while len(random) < 6:
        var = randrange (0,9)
        if var == 0 and contador == 0:
            continue
        
        contador += 1
        random += str (var)
    
    return int(random)

"""
    Metodo que envia el codigo generado a la DDBB y envia el codigo al correo electronico del usuario que lo solicito
"""
def Generate_code (email, message):
    code = random_code ()
    encrypted = data_encrypt ()
    validate = methods ()
    if validate.validate_email(email, email):
        query = "SELECT NAME, LAST_NAME, ID FROM Auth_Users WHERE USERNAME=?"
        try:
            data = request_db (query, (encrypted.encrypt_one (email),))
            for k in data:
                data_usr = encrypted.Desencrypt (k)
            Insert_codeDB (code, dtt, k[2])
            users = "%s %s"%(data_usr[0], data_usr[1])
            email_send (users, code, email)
        except UnboundLocalError as ut:
            message.config (text="Email does not exist")
        except httplib2.error.ServerNotFoundError as google_e:
            message.config (text="Connect to the internet")
            return
        
        messagebox.showinfo (title="Send message", message=f"A code has been sent to reset the \naccount password '{email}'")
    
    else:
        message.config (text="Incorrect email")
