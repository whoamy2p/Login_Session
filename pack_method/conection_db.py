#! /usr/bin/env python3

from tkinter import messagebox
import sqlite3


"""
    Función que reliza las consultas a la base da datos y devulve un objeto
"""

def request_db (query, parameter=()):
    with sqlite3.connect ("Login.db") as conection:
        cursor = conection.cursor ()
        try:
            result = cursor.execute (query, parameter)
        except sqlite3.DatabaseError as dbt:
            messagebox.showerror (title="Database error", message="""Failed to connect to database. 
            Error of %s"""%dbt)
            print ("fallo al conectar a la abse de datos", dbt)
        
        conection.commit ()

        return result


#  ****** METODO ENCARGADO DE INGRESAR LOS USUARIOS REGISTRADOS A LA DDBB *******

def Insert_dataDB_users (parameter, validator, encryptCode, emaill, window):
    if validator.validate_data  (parameter):
        try:
            query = "INSERT INTO Auth_Users VALUES (NULL, ?,?,?,?,?,?,?,?)"
            
            if messagebox.askokcancel (title="Insert element", message="Are you sure you want to save the account? \n %s"%emaill):

                request_db (query, encryptCode.Encrypt (parameter))

                window.destroy ()
        except sqlite3.OperationalError as ots:
            print ("Error de: ", ots)
    
    else:
        messagebox.showerror (title="Field error", message="Please fill in all the fields or \ncancel the operation")

def Read_dataDB_Users (email):
    query = "SELECT ID FROM Auth_Users WHERE USERNAME=?"
    result = request_db (query, (email,))
    for k in result:
        return k

# ----------- INSERTANDO LOS CODIGOS DE VERIFICACIÓN A LA BASE DE DATOS ------------------


def Insert_codeDB (code, dt, id_user):
    query = "INSERT INTO Code_Verfication values(NULL, ?,?,?)"
    parameter_inf = [code, id_user, f"{dt.day}/{dt.month}/{dt.year}"]
    request_db (query, parameter_inf)
