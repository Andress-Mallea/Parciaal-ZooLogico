from tkinter import *
from tkinter import messagebox
import mysql.connector

def show(mydb): 
    try:
        select_show = Toplevel()
        select_show.title("Base de datos god")
        select_show.iconbitmap("codigos/assets/BDICON.ico")
        
        def confirmacion():
            table_name = table_var.get()
            select_show.destroy()
            final_show(mydb, table_name)
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = DATABASE() AND TABLE_TYPE = 'BASE TABLE';")
        tables = [table[0] for table in mycursor.fetchall()]
        
        if not tables:
            messagebox.showerror("ERROR", "No hay tablas disponibles.")
            return
        
        table_var = StringVar()
        table_var.set(tables[0])  # Set default value
        
        for table in tables:
            Radiobutton(select_show, text=table, variable=table_var, value=table).pack(anchor=W)
        
        connfi = Button(select_show, text="Confirmar", command=confirmacion)
        connfi.pack()
        
        def final_show(mydb, table_name):
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT * FROM `{table_name}`;")
            records = mycursor.fetchall()
            the_show = Toplevel()
            the_show.title("Base de datos god")
            the_show.iconbitmap("codigos/assets/BDICON.ico")
            
            mycursor.execute(f"""SELECT COLUMN_NAME 
                                FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = '{table_name}';
                                """)
            columns = [col[0] for col in mycursor.fetchall()]
            m = Label(the_show, text=', '.join(columns))
            m.pack()
            
            for record in records:
                n = Label(the_show, text=record)
                n.pack()

    except Exception as ex:
        messagebox.showerror("ERROR", f"El error es: \n{ex}")
