import mysql.connector
from tkinter import messagebox
from mysql.connector import Error
import codigos.my_sql.add_mysql as add_mysql 
import codigos.my_sql.del_mysql as del_mysql
import codigos.my_sql.modificar_mysql as modificar_mysql
import codigos.my_sql.show_mysql as show_mysql
from playsound import *
def conecion(user, password, database):
    try:
        global mydb
        mydb = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database=database,
            port="3306"
        )
        messagebox.showinfo("Conexion Mysql","Conexion exitosa!")

    except Error as e:
        messagebox.showerror("Error",f"El Error es: \n{e}")

def add():
    playsound("codigos/assets/Select.wav")
    add_mysql.add(mydb)
def show():
    playsound("codigos/assets/Select.wav")
    show_mysql.show(mydb)
def delete():
    playsound("codigos/assets/Select.wav")
    del_mysql.delete(mydb)
def mod():
    playsound("codigos/assets/Select.wav")
    modificar_mysql.modify(mydb)
def mysql_to_sqls():
    playsound("codigos/assets/Select.wav")
    pass