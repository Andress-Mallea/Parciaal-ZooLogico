from tkinter import *
import codigos.sql_server.BD_sql_server as BD_sql_server 
import codigos.musica as musica
def sqls(usuario):
    main = Tk()
    musica.music("codigos/assets/sqlserver.ogg")
    main.title("Base de datos god")
    main.iconbitmap("codigos/assets/BDICON.ico")
    main.geometry("1280x720")
    main.config(bg="#F18A69")
    if(usuario == "DBA"):
        agregar = Button(main, text="Agregar", font=("Arial", 30), width=0, height=2, command=BD_sql_server.add)
        agregar.grid(row="0",column="0", padx=150, pady=50)
        modificar = Button(main, text="Modificar", font=("Arial", 30), width=0, height=2, command=BD_sql_server.update)
        modificar.grid(row="0",column="2", padx=100, pady=50)
        #migrar = Button(main, text="Migrar a Mysql", font=("Arial", 30), width=0, height=2, command=BD_sql_server.sqls_to_mysql)
        #migrar.grid(row="1",column="1", padx="0")
        eliminar = Button(main,text="Eliminar", font=("Arial", 30), width=0, height=2, command=BD_sql_server.delete)
        eliminar.grid(row="2",column="0", padx=110, pady=100)
        mostrar = Button(main, text="Mostrar", font=("Arial", 30), width=0, height=2, command=BD_sql_server.show)
        mostrar.grid(row="2",column="2", padx=110, pady=50)
    elif(usuario == "Vendedor"):
        registrar_venta_btn = Button(main, text="Registrar Venta", font=("Arial", 30), width=0, height=2, command=BD_sql_server.registrar_venta)
        registrar_venta_btn.grid(row="0", column="2", padx=110, pady=50)
        consultar_boletos_btn = Button(main, text="Consultar Boletos", font=("Arial", 30), width=0, height=2, command=BD_sql_server.consultar_boletos_vendedor)
        consultar_boletos_btn.grid(row="1", column="2",padx=110 , pady=50)
    elif(usuario == "Gerente"):
        # Opción de consulta por zona para el Gerente
        consultar_zona_btn = Button(main, text="Consultar Zona", font=("Arial", 30), width=0, height=2, command=BD_sql_server.consultar_zona)
        consultar_zona_btn.grid(row="0", column="1", pady=50) 
        # Opción de consulta de clientes para el Gerente
        consultar_cliente_btn = Button(main, text="Consultar Cliente", font=("Arial", 30), width=0, height=2, command=BD_sql_server.consultar_cliente)
        consultar_cliente_btn.grid(row="0", column="2", pady=50)
        # Opción para mostrar el total de visitas por zona para el Gerente
        mostrar_visitas_btn = Button(main, text="Visitas por Zona", font=("Arial", 30), width=0, height=2, command=BD_sql_server.mostrar_visitas_por_zona)
        mostrar_visitas_btn.grid(row="0", column="3", pady=50)
        #Mostrar todos los elementos de la tabla
        mostrar = Button(main, text="Mostrar", font=("Arial", 30), width=0, height=2, command=BD_sql_server.show)
        mostrar.grid(row="2",column="3", padx=110, pady=50)
        # Opción para mostrar facturas por cliente para el Gerente
        mostrar_facturas_btn = Button(main, text="Facturas por Cliente", font=("Arial", 30), width=0, height=2, command=BD_sql_server.mostrar_facturas_cliente)
        mostrar_facturas_btn.grid(row="3", column="1", pady=50)
        # Opción para mostrar el historial de boletos del cliente para el Gerente
        mostrar_historial_btn = Button(main, text="Historial Cliente", font=("Arial", 30), width=0, height=2, command=BD_sql_server.mostrar_historial_cliente)
        mostrar_historial_btn.grid(row="3", column="2", pady=50)
        # Opción para mostrar el reporte de ventas para el Gerente
        mostrar_reporte_btn = Button(main, text="Reporte de Ventas", font=("Arial", 30), width=0, height=2, command=BD_sql_server.mostrar_reporte_ventas)
        mostrar_reporte_btn.grid(row="3", column="3", pady=50)
        # Opción para buscar boletos con el stored procedure para el Gerente
        buscar_boletos_proc_btn = Button(main, text="Buscar Boletos (SP)", font=("Arial", 30), width=0, height=2, command=BD_sql_server.buscar_boletos_procedimiento)
        buscar_boletos_proc_btn.grid(row="2", column="1", pady=50)
    main.mainloop()
    musica.detenermusica()
