from tkinter import *
import codigos.sql_server.inicio_sesion_sqls as inicio_sesion_sqls
import codigos.my_sql.inicio_sesion_mysql as inicio_sesion_mysql
from playsound import *
import codigos.musica as musica
def menu_inicio():
    def abrir_sqls():
        playsound("codigos/assets/Select.wav")
        inicio_sesion_sqls.inicio_sesion(main_menu)
    def abrir_mysql():
        playsound("codigos/assets/Select.wav")
        inicio_sesion_mysql.inicio_sesion(main_menu)
    main_menu = Tk()
    main_menu.title("Base de datos god")
    main_menu.iconbitmap("codigos/assets/BDICON.ico")
    main_menu.geometry("1280x720")
    main_menu.config(bg="#7BBECB")
    titulo = PhotoImage(file="codigos/assets/titulo.png")
    titulo_label = Label(image=titulo)
    titulo_label.pack(side="top")
    titulo_label.config(cursor="hand2")
    padoru = PhotoImage(file="codigos/assets/padoru.png")
    sqls = Button(main_menu, text="SQL Server", font=("Arial", 30), width=0, height=2,command=abrir_sqls)
    sqls.pack(side="top", padx=10, pady=50)
    sqls.config(cursor="hand2")
    #mysql = Button(main_menu, text="My sql", font=("Arial", 30), width=10, height=2,command=abrir_mysql)
    #mysql.pack(side="top", padx=10, pady=10)
    #mysql.config(cursor="hand2")
    main_menu.mainloop()