from tkinter import *
from tkinter import messagebox
import pyodbc
import mysql.connector
import codigos.sql_server.BD_sql_server as BD_sql_server

def migrar():
    # Conexión a MySQL
    def connect_to_mysql_without_database(host, user, password):
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

    def connect_to_mysql_with_database(host, database, user, password):
        return mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )

    # Extraer estructura del SQL Server
    def fetch_data_from_sql_server(cursor, table):
        cursor.execute(f"SELECT * FROM [{table}]")
        columns = [column[0] for column in cursor.description]
        columns = [col.replace('.', '') for col in columns]
        columns = [col.replace(' ', '') for col in columns]
        data = cursor.fetchall()
        data = [tuple(item.strip() if isinstance(item, str) else item for item in row) for row in data]  # Eliminar espacios en blanco de cada elemento
        return columns, data

    def create_mysql_table(mysql_cursor, table_name, columns):
        # Cambiar a `BLOB` para la columna `definition` si causa problemas
        columns_definitions = ", ".join([f"`{col}` BLOB" if col == 'definition' else f"`{col}` TEXT CHARACTER SET utf8mb4" for col in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns_definitions})"
        mysql_cursor.execute(create_table_query)

    # Insertar datos en MySQL
    def insert_data_into_mysql(mysql_cursor, table_name, columns, data):
        placeholders = ", ".join(["%s"] * len(columns))
        insert_query = f"INSERT INTO `{table_name}` ({', '.join(columns)}) VALUES ({placeholders})"
        mysql_cursor.executemany(insert_query, data)

    # Proceso de migración
    def migrate_data(mysql_config, table_name):
        try:
            # Usar la conexión global `mydb` de `BD_sql_server`
            sql_server_conn = BD_sql_server.mydb
            sql_server_cursor = sql_server_conn.cursor()
    
            # Conectar a MySQL
            mysql_conn = connect_to_mysql_with_database(**mysql_config)
            mysql_cursor = mysql_conn.cursor()
    
            # Obtener datos de SQL Server
            columns, data = fetch_data_from_sql_server(sql_server_cursor, table_name)
    
            # Crear tabla en MySQL
            create_mysql_table(mysql_cursor, table_name, columns)
    
            # Insertar datos en MySQL
            insert_data_into_mysql(mysql_cursor, table_name, columns, data)
    
            # Confirmar cambios
            mysql_conn.commit()
            print(f"Tabla `{table_name}` migrada exitosamente.")
    
            sql_server_cursor.close()
            mysql_cursor.close()
            mysql_conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la migración: {e}")

    def fetch_tables_names_from_sql_server(cursor):
        cursor.execute("SELECT name FROM sys.tables;")
        tablas = cursor.fetchall()
        # Filtrar la tabla sysdiagrams
        tables_names = [tabla[0] for tabla in tablas if 'sysdiagrams' not in tabla[0].lower()]
        return tables_names

    def on_submit():
        mysql_host = mysql_host_entry.get()
        mysql_user = mysql_user_entry.get()
        mysql_password = mysql_password_entry.get()
        sql_server_database = sql_server_database_entry.get()

        mysql_config_without_db = {
            "host": mysql_host,
            "user": mysql_user,
            "password": mysql_password
        }

        mysql_config_with_db = {
            "host": mysql_host,
            "database": sql_server_database,
            "user": mysql_user,
            "password": mysql_password
        }

        try:
            # Usar la conexión global `mydb` de `BD_sql_server`
            sql_server_conn = BD_sql_server.mydb
            sql_server_cursor = sql_server_conn.cursor()
    
            # Conectar a MySQL
            mysql_conn = connect_to_mysql_without_database(**mysql_config_without_db)
            mysql_cursor = mysql_conn.cursor()
    
            # Crear base de datos en MySQL
            mysql_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{sql_server_database}`")
            mysql_cursor.close()
            mysql_conn.close()
    
            tables_names = fetch_tables_names_from_sql_server(sql_server_cursor)
    
            # Desactivar verificaciones de claves foráneas antes de la migración
            mysql_conn = connect_to_mysql_with_database(**mysql_config_with_db)
            mysql_cursor = mysql_conn.cursor()
            mysql_cursor.execute("SET foreign_key_checks = 0;")
            mysql_cursor.close()
            mysql_conn.close()
    
            # Migrar las tablas en el orden correcto
            for table_name in tables_names:
                migrate_data(mysql_config_with_db, table_name)
    
            # Reactivar verificaciones de claves foráneas después de la migración
            mysql_conn = connect_to_mysql_with_database(**mysql_config_with_db)
            mysql_cursor = mysql_conn.cursor()
            mysql_cursor.execute("SET foreign_key_checks = 1;")
            mysql_cursor.close()
            mysql_conn.close()
    
            sql_server_cursor.close()
    
            messagebox.showinfo("Éxito", "Migración completada exitosamente.")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la migración: {e}")

    def mostrar_password():
        if mysql_password_entry.cget('show') == '':
            mysql_password_entry.config(show='*')
        else:
            mysql_password_entry.config(show='')

    # Interfaz gráfica de usuario
    root = Tk()
    root.title("Migración de Base de Datos")
    root.geometry("400x400")
    root.iconbitmap("codigos/assets/BDICON.ico")

    # Etiquetas y entradas de texto
    Label(root, text="Base de datos de SQL Server").grid(row=0, column=0, padx=10, pady=10)
    sql_server_database_entry = Entry(root)
    sql_server_database_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Host de MySQL").grid(row=1, column=0, padx=10, pady=10)
    mysql_host_entry = Entry(root)
    mysql_host_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(root, text="Usuario de MySQL").grid(row=2, column=0, padx=10, pady=10)
    mysql_user_entry = Entry(root)
    mysql_user_entry.grid(row=2, column=1, padx=10, pady=10)

    Label(root, text="Contraseña de MySQL").grid(row=3, column=0, padx=10, pady=10)
    mysql_password_entry = Entry(root, show="*")
    mysql_password_entry.grid(row=3, column=1, padx=10, pady=10)

    # Cargar la imagen del ojo y configurar el botón para mostrar/ocultar contraseña")
    toggle_button = Button(root, text="Mostrar", command=mostrar_password)
    toggle_button.grid(row=3, column=2, padx=10, pady=10)

    # Botón de envío
    submit_button = Button(root, text="Migrar", command=on_submit)
    submit_button.grid(row=4, columnspan=2, pady=20)

    root.mainloop()
