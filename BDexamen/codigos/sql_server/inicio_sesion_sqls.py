from tkinter import *
from tkinter import messagebox
import codigos.sql_server.BD_sql_server as BD_sql_server
import codigos.sql_server.menu_sql_server as menu_sql_server
from playsound import *
import codigos.musica as musica
import socket 
global a
global b
kur = 1
DATABASE = "Proyecto_Zoologico"  

def sonidito():
    global kur  # Asegurarnos de que x se refiera a la variable global
    if kur == 1:
        playsound("codigos/assets/Kururin_sound.wav")
        kur = 0
    else:
        playsound("codigos/assets/Kuru_kuru_sound.wav")
        kur = 1

def inicio_sesion(main_menu):
    def conectar(server, username, password):
        try:
            BD_sql_server.conection(server, DATABASE, username, password)  # Usar la base de datos específica
        except Exception as ex:
            messagebox.showerror("ERROR", f"No se pudo conectar con la base de datos.\n{ex}")

    def hola():
        if user_entry.get() == '' or password_entry.get() == '':
            messagebox.showwarning("ERROR", "Llena los datos de usuario y contraseña antes de ingresar")
        else:
            servidor = socket.gethostname()  # Obtener automáticamente el nombre del servidor
            usuario = user_entry.get()
            contrasena = password_entry.get()
            conectar(servidor, usuario, contrasena)
            start_sqls.destroy()
            main_menu.destroy()
            musica.detenermusica()
            menu_sql_server.sqls(usuario)

    def cerrar():
        start_sqls.destroy()

    def mostrar_ocultar_password():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            mostrar_ocultar_boton.config(text="Ocultar")
        else:
            password_entry.config(show='*')
            mostrar_ocultar_boton.config(text="Mostrar")

    # raiz principal
    start_sqls = Toplevel()
    start_sqls.title("Iniciar sesion en SQLServer")
    start_sqls.iconbitmap("codigos/assets/BDICON.ico")
    start_sqls.config(bg="#7BBECB")
    x = 0
    # imagenSfrom playsound import playsound

    # Definir una varfrom playsound import playsound

    # Definir una variable global
    xd = PhotoImage(file="codigos/assets/padoru.png")
    label = Button(start_sqls, image=xd, command=sonidito)
    label.place(x="300", y="100")
    label.config(cursor="hand2")

    # Ingresar datos
    titulo = Label(start_sqls, text="SQL SERVER", font=("Comic Sans SN", 10))
    titulo.grid(row="0", column="1", padx=10, pady=10)

    # Se elimina la etiqueta y entrada del servidor
    # nombre_s = Label(start_sqls, text="Server", font=("Comic Sans SN", 10))
    # nombre_s.grid(row="1", column="0", padx=10, pady=10)
    # server_label = Label(start_sqls, text=socket.gethostname(), font=("Comic Sans SN", 10))
    # server_label.grid(row="1", column="1", padx=10, pady=10, sticky="w")

    global user_entry
    user_entry = Entry(start_sqls)
    user_entry.grid(row="1", column="1", padx=10, pady=10)
    nombre_u = Label(start_sqls, text="Usuario", font=("Comic Sans SN", 10))
    nombre_u.grid(row="1", column="0", padx=10, pady=10)

    global password_entry
    password_entry = Entry(start_sqls, show="*")  # Para ocultar la contraseña
    password_entry.grid(row="2", column="1", padx=10, pady=10)
    nombre_p = Label(start_sqls, text="Contraseña", font=("Comic Sans SN", 10))
    nombre_p.grid(row="2", column="0", padx=10, pady=10)

    # Botón para mostrar/ocultar la contraseña
    global mostrar_ocultar_boton
    mostrar_ocultar_boton = Button(start_sqls, text="Mostrar", command=mostrar_ocultar_password)
    mostrar_ocultar_boton.grid(row="2", column="2", padx=5, pady=5)
    mostrar_ocultar_boton.config(cursor="hand2")

    # boton
    boton = Button(start_sqls, text="Confirmar", command=hola)
    boton.grid(row="3", column="0", padx=10, pady=10)
    salir = Button(start_sqls, text="Cerrar", command=cerrar)
    salir.grid(row="3", column="1", padx=10, pady=10)
    # main
    start_sqls.mainloop()