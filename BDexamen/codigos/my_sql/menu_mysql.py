from tkinter import *
import codigos.my_sql.BD_mysql as BD_mysql 
import codigos.musica as musica
def mysql():
    musica.music("codigos/assets/mysql.ogg")
    main = Tk()
    main.title("Base de datos god")
    main.iconbitmap("codigos/assets/BDICON.ico")
    main.geometry("1280x720")
    main.config(bg="#9469F1")
    agregar = Button(main, text="Agregar", font=("Arial", 30), width=0, height=2, command=BD_mysql.add)
    agregar.grid(row="0",column="0", padx=150, pady=50)
    modificar = Button(main, text="Modificar", font=("Arial", 30), width=0, height=2,command=BD_mysql.mod)
    modificar.grid(row="0",column="2", padx=100, pady=50)
    migrar = Button(main, text="Migrar a Sql Server", font=("Arial", 30), width=0, height=2)
    migrar.grid(row="1",column="1", padx="0")
    eliminar = Button(main,text="Eliminar", font=("Arial", 30), width=0, height=2,command=BD_mysql.delete)
    eliminar.grid(row="2",column="0", padx=110, pady=100)
    mostrar = Button(main, text="Mostrar", font=("Arial", 30), width=0, height=2,command=BD_mysql.show)
    mostrar.grid(row="2",column="2", padx=110, pady=50)
    main.mainloop()
    musica.detenermusica()
