from tkinter import *
from tkinter import messagebox
import pyodbc

# Función para obtener nombres de columnas de la tabla
def obtener_nombres_columnas(mydb, table_name):
    cursor = mydb.cursor()
    cursor.execute(f"""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}';
    """)
    columnas = cursor.fetchall()
    nombres_columnas = [columna[0] for columna in columnas]
    return nombres_columnas

# Función para mostrar la ventana y eliminar un registro
def final_show(mydb, table_name):
    def eliminar_fila():
        fila_id = var.get()
        if fila_id is not None:
            try:
                cursor = mydb.cursor()
                query = f"DELETE FROM {table_name} WHERE [{id_column}] = ?"
                cursor.execute(query, fila_id)
                mydb.commit()
                messagebox.showinfo("Éxito", "Registro eliminado exitosamente")
                the_show.destroy()
            except Exception as ex:
                messagebox.showerror("ERROR", f"El error es: \n{ex}")
        else:
            messagebox.showerror("ERROR", "Seleccione una fila para eliminar")

    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    records = cursor.fetchall()
    columnas = obtener_nombres_columnas(mydb, table_name)
    
    # Asumimos que la primera columna es el identificador
    id_column = columnas[0]

    the_show = Toplevel()
    the_show.title(f"Eliminar datos de {table_name}")
    the_show.iconbitmap("codigos/assets/BDICON.ico")
    
    # Crear Canvas y Scrollbar
    canvas = Canvas(the_show)
    scrollbar = Scrollbar(the_show, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Colocar el Canvas y la Scrollbar en la ventana
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Mostrar columnas como encabezado
    encabezado = ', '.join(columnas)
    Label(scrollable_frame, text=encabezado, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
    
    # Mostrar registros con Radiobutton para seleccionar la fila a eliminar
    var = IntVar()
    for i, record in enumerate(records, start=1):
        Radiobutton(scrollable_frame, text=record, variable=var, value=record[0]).grid(row=i, column=0, pady=5)
    
    # Botón para confirmar la eliminación
    Button(scrollable_frame, text="Eliminar", command=eliminar_fila).grid(row=len(records)+1, column=0, pady=10)
    Button(scrollable_frame, text="Cancelar", command=the_show.destroy).grid(row=len(records)+1, column=1, ipadx=55, pady=10)

# Función principal para eliminar registro
def delete(mydb): 
    try:
        select_show = Toplevel()
        select_show.title("Base de datos god")
        select_show.iconbitmap("codigos/assets/BDICON.ico")

        def confirmacion():
            table_name = table_var.get()
            select_show.destroy()
            final_show(mydb, table_name)
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
        tables = [table[0] for table in mycursor.fetchall() if 'sysdiagram' not in table[0].lower()]

        if not tables:
            messagebox.showerror("ERROR", "No hay tablas disponibles que no sean sysdiagrams.")
            return

        table_var = StringVar()
        table_var.set(tables[0])  # Set default value

        for table in tables:
            Radiobutton(select_show, text=table, variable=table_var, value=table).pack(anchor=W)
        
        Button(select_show, text="Confirmar", command=confirmacion).pack()
        
    except Exception as ex:
        messagebox.showerror("ERROR", f"El error es: \n{ex}")
