from tkinter import *
from tkinter import messagebox
import pyodbc
import codigos.sql_server.show_sqls as show_sqls
import codigos.sql_server.add_sqls as add_sqls
import codigos.sql_server.del_sqls as del_sqls
import codigos.sql_server.modificar_sqls as modificar_sqls
import codigos.sql_server.migrar_sqls_to_mysql as migrar_sqls_to_mysql
from playsound import *
# 1. Crear conexion SQL Server
mydb = None
def conection(server, database, username, password):
    try:
        global mydb
        mydb = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                               f"SERVER={server};"
                               f"DATABASE={database};"
                               f"UID={username};"
                               f"PWD={password}")
        messagebox.showinfo("Conexion", "Se ha conectado exitosamente!")
    except Exception as ex:
        messagebox.showerror("ERROR", f"El error es: \n{ex}")
def show():
    playsound("codigos/assets/Select.wav")
    show_sqls.show(mydb)
def delete():
    playsound("codigos/assets/Select.wav")
    del_sqls.delete(mydb)
def add():
    playsound("codigos/assets/Select.wav")
    add_sqls.add(mydb)
def update():
    playsound("codigos/assets/Select.wav")
    modificar_sqls.modify(mydb)
def sqls_to_mysql():
    playsound("codigos/assets/Select.wav")
    migrar_sqls_to_mysql.migrar()  
def consultar_zona():
    playsound("codigos/assets/Select.wav")
    show_sqls.consultar_zona_con_conteo(mydb)
def consultar_cliente():
    playsound("codigos/assets/Select.wav")
    show_sqls.consultar_cliente_boletos_gastado(mydb)
def mostrar_visitas_por_zona():
    playsound("codigos/assets/Select.wav")
    show_sqls.mostrar_total_visitas_por_zona(mydb)
def mostrar_facturas_cliente():
    playsound("codigos/assets/Select.wav")
    show_sqls.mostrar_facturas_por_cliente(mydb)
def mostrar_historial_cliente():
    playsound("codigos/assets/Select.wav")
    show_sqls.mostrar_historial_boletos_cliente(mydb)
def mostrar_reporte_ventas():
    playsound("codigos/assets/Select.wav")
    show_sqls.mostrar_vista_reporte_ventas(mydb)
def buscar_boletos_procedimiento():
    playsound("codigos/assets/Select.wav")
    show_sqls.ejecutar_procedimiento_boletos_cliente(mydb)
def registrar_venta():
    playsound("codigos/assets/Select.wav")
    add_sqls.registrar_venta_pendiente(mydb)
def consultar_boletos_vendedor():
    playsound("codigos/assets/Select.wav")
    show_sqls.mostrar_boletos_vendedor(mydb)
