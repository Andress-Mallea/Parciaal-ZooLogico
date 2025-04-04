from tkinter import *
from tkinter import messagebox
import codigos.my_sql.BD_mysql as BD_mysql
import codigos.my_sql.menu_mysql as menu_mysql
from playsound import *
import codigos.musica as musica
kur = 1
def sonidito():
    global kur  # Asegurarnos de que x se refiera a la variable global
    if kur == 1:
        playsound("codigos/assets/Kururin_sound.wav")
        kur = 0
    else:
        playsound("codigos/assets/Kuru_kuru_sound.wav")
        kur = 1
def inicio_sesion(main_menu):
    def conectar(user, password, database):
        try:
            BD_mysql.conecion(user, password, database)
        except Exception as ex:
            messagebox.showerror("ERROR", f"No se pudo conectar con la base de datos.\n{ex}")
    def hola():
        if user.get() == '' or password.get() == '':
            messagebox.showerror("ERROR", "Llena los datos antes de ingresar")   
        else:
            global a
            a = user.get()
            global b
            b = password.get()
            global c
            c = database.get()
            conectar(a,b, c)
            start_sqls.destroy()
            main_menu.destroy()
            musica.detenermusica()
            menu_mysql.mysql()

    def cerrar():
          start_sqls.destroy()
    def mostrar_password():
      if password.cget('show') == '*':
            password.config(show='')
      else:
            password.config(show='*')
    #raiz principal
    start_sqls = Toplevel()
    start_sqls.title("Iniciar sesion en Mysql")
    start_sqls.iconbitmap("codigos/assets/BDICON.ico")
    #main.geometry("1280x720")
    start_sqls.config(bg="#7BBECB")
    
    #imagen
    xd = PhotoImage(file="codigos/assets/padoru.png")
    label = Button(start_sqls ,image=xd, command=sonidito)
    label.place(x="300",y="100")
    label.config(cursor="hand2")

    #Ingresar datos
    titulo = Label(start_sqls, text="MY SQL", font=("Comic Sans SN", 10))
    titulo.grid(row="0",column="1", padx=10, pady=10)
    global user
    user = Entry(start_sqls)
    user.grid(row="1",column="1", padx=10, pady=10)
    n_user = Label(start_sqls, text="User", font=("Comic Sans SN", 10))
    n_user.grid(row="1",column="0", padx=10, pady=10)
    contrasena = False
    global password
    password = Entry(start_sqls)
    password.grid(row="2",column="1", padx=10, pady=10)
    p = Label(start_sqls, text="Password", font=("Comic Sans SN", 10))
    p.grid(row="2",column="0", padx=10, pady=10)
    eye = PhotoImage(file="codigos/assets/eye.png")
    eye_l = Button(start_sqls ,image=eye, command=mostrar_password)
    eye_l.grid(row="2",column="2", padx=0.5, pady=0.5)
    eye_l.config(cursor="hand2")
    if contrasena == True:
            password.config()
    else:
            password.config(show="*")

    #boton
    
    global database
    database = Entry(start_sqls)
    database.grid(row="3",column="1", padx=10, pady=10)
    n_db = Label(start_sqls, text="Database", font=("Comic Sans SN", 10))
    n_db.grid(row="3",column="0", padx=10, pady=10)
    boton = Button(start_sqls, text="Confirmar", command=hola)
    boton.grid(row="4",column="0", padx=10, pady=10)
    salir = Button(start_sqls, text="Cerrar", command=cerrar)
    salir.grid(row="4",column="1", padx=10, pady=10)
    #main
    start_sqls.mainloop()