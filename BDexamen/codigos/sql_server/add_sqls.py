from tkinter import *
from tkinter import messagebox
import pyodbc
import datetime
from tkinter import simpledialog
from tkinter import ttk

def obtener_info_columnas(mydb, table_name):
    cursor = mydb.cursor()
    cursor.execute(f"""
        SELECT COLUMN_NAME, COLUMNPROPERTY(OBJECT_ID('{table_name}'), COLUMN_NAME, 'IsIdentity') AS IsIdentity
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}';
    """)
    columnas_info = cursor.fetchall()
    nombres_columnas = [columna[0] for columna in columnas_info]
    es_identity = {columna[0]: bool(columna[1]) for columna in columnas_info}
    return nombres_columnas, es_identity

# Función para mostrar la ventana y añadir un registro
def final_show(mydb, table_name):
    columnas, es_identity = obtener_info_columnas(mydb, table_name)
    columnas_insertar = [col for col in columnas if not es_identity.get(col)]  # No incluir IDENTITY

    the_show = Toplevel()
    the_show.title(f"Añadir datos a {table_name}")
    the_show.iconbitmap("codigos/assets/BDICON.ico")
    entries = {}

    for i, columna in enumerate(columnas_insertar):
        label = Label(the_show, text=columna)
        label.grid(row=i, column=0, padx=10, pady=5)
        entry = Entry(the_show)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[columna] = entry

    def insertar_registro():
        nombres_columnas_insertar = ", ".join([f"[{col}]" for col in columnas_insertar])
        placeholders = ", ".join(["?" for _ in columnas_insertar])
        valores = [entries[col].get() for col in columnas_insertar]

        try:
            cursor = mydb.cursor()
            query = f"INSERT INTO {table_name} ({nombres_columnas_insertar}) VALUES ({placeholders})"
            cursor.execute(query, valores)
            mydb.commit()
            messagebox.showinfo("Éxito", "Registro añadido exitosamente")
            the_show.destroy()
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            messagebox.showerror("ERROR", f"Error al insertar registro: \n{ex}")
        except Exception as ex:
            messagebox.showerror("ERROR", f"Error general: \n{ex}")

    def cancelar():
        the_show.destroy()

    boton_insertar = Button(the_show, text="Insertar", command=insertar_registro)
    boton_insertar.grid(row=len(columnas_insertar), column=0, pady=10)
    boton_cancelar = Button(the_show, text="Cancelar", command=cancelar)
    boton_cancelar.grid(row=len(columnas_insertar), column=1, pady=10)

# Función principal para añadir registro
def add(mydb):
    try:
        select_show = Toplevel()
        select_show.title("Seleccionar tabla para añadir")
        select_show.iconbitmap("codigos/assets/BDICON.ico")

        def confirmacion():
            table_name = table_var.get()
            select_show.destroy()
            final_show(mydb, table_name)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME <> 'sysdiagrams';")
        tables = [table[0] for table in mycursor.fetchall()]

        if not tables:
            messagebox.showerror("ERROR", "No hay tablas disponibles para añadir.")
            return

        table_var = StringVar()
        table_var.set(tables[0])  # Set default value

        for table in tables:
            Radiobutton(select_show, text=table, variable=table_var, value=table).pack(anchor=W)

        connfi = Button(select_show, text="Confirmar", command=confirmacion)
        connfi.pack()

    except Exception as ex:
        messagebox.showerror("ERROR", f"El error es: \n{ex}")
        
PRECIOS_BOLETOS = {"Adulto": 50.00, "Niño": 35.00, "Estudiante": 40.00, "Jubilado": 30.00}
TIPOS_BOLETO_DISPONIBLES = list(PRECIOS_BOLETOS.keys())

def registrar_venta_pendiente(mydb):
    ventana_registro = Toplevel()
    ventana_registro.title("Registrar Venta (Vendedor)")
    ventana_registro.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_registro, text="NIT para la Factura:", font=("Arial", 10)).pack(pady=5)
    nit_entry = Entry(ventana_registro)
    nit_entry.pack(pady=5)

    def mostrar_formulario_boletos(num_boletos, zonas_disponibles):
        formulario_boletos = Toplevel(ventana_registro)
        formulario_boletos.title("Detalles de Boletos")
        formulario_boletos.iconbitmap("codigos/assets/BDICON.ico")

        entradas_boletos = []
        total_acumulado_var = StringVar(value="0.00")

        # Crear Canvas y Scrollbar para el formulario de boletos
        canvas_boletos = Canvas(formulario_boletos)
        scrollbar_boletos = Scrollbar(formulario_boletos, orient="vertical", command=canvas_boletos.yview)
        scrollable_frame_boletos = Frame(canvas_boletos)

        scrollable_frame_boletos.bind(
            "<Configure>",
            lambda e: canvas_boletos.configure(
                scrollregion=canvas_boletos.bbox("all")
            )
        )

        canvas_boletos.create_window((0, 0), window=scrollable_frame_boletos, anchor="nw")
        canvas_boletos.configure(yscrollcommand=scrollbar_boletos.set)

        scrollbar_boletos.pack(side="right", fill="y")
        canvas_boletos.pack(side="left", fill="both", expand=True)

        def calcular_total():
            total = 0.0
            for entrada in entradas_boletos:
                tipo_seleccionado = entrada['tipo_boleto_var'].get()
                precio = PRECIOS_BOLETOS.get(tipo_seleccionado, 0.0)
                total += precio
            total_acumulado_var.set(f"{total:.2f}")

        for i in range(num_boletos):
            Label(scrollable_frame_boletos, text=f"--- Boleto {i+1} ---").pack(pady=5)
            frame_boleto = Frame(scrollable_frame_boletos)
            frame_boleto.pack(pady=2)

            Label(frame_boleto, text="Zona:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
            zona_var = StringVar(formulario_boletos)
            zona_combo = ttk.Combobox(frame_boleto, textvariable=zona_var, values=zonas_disponibles)
            zona_combo.grid(row=0, column=1, padx=5, pady=5)

            Label(frame_boleto, text="Tipo de Boleto:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
            tipo_boleto_var = StringVar(value=TIPOS_BOLETO_DISPONIBLES[0] if TIPOS_BOLETO_DISPONIBLES else "")
            frame_tipos = Frame(frame_boleto)
            frame_tipos.grid(row=1, column=1, padx=5, pady=5, sticky="w")
            for j, tipo in enumerate(TIPOS_BOLETO_DISPONIBLES):
                Radiobutton(frame_tipos, text=tipo, variable=tipo_boleto_var, value=tipo, command=calcular_total).pack(side="left")

            entradas_boletos.append({
                "zona_var": zona_var,
                "tipo_boleto_var": tipo_boleto_var
            })

        Label(scrollable_frame_boletos, text="--- Factura ---").pack(pady=5)
        Label(scrollable_frame_boletos, text="Total:", font=("Arial", 10)).pack(pady=2)
        total_label = Label(scrollable_frame_boletos, textvariable=total_acumulado_var, font=("Arial", 12, "bold"))
        total_label.pack(pady=2)

        def registrar_boletos_final():
            nit = nit_entry.get().strip()
            if not nit:
                messagebox.showerror("Error", "Por favor, ingrese el NIT para la factura.")
                return

            try:
                cursor = mydb.cursor()
                total_factura = float(total_acumulado_var.get())
                cantidad_boletos = len(entradas_boletos)

                # Insertar en Facturas
                cursor.execute("""
                    INSERT INTO Facturas (Nit, CantidadDeBoletos, Total, FechaDeEmision)
                    VALUES (?, ?, ?, GETDATE())
                """, (nit, cantidad_boletos, total_factura))
                mydb.commit()
                cursor.execute("SELECT @@IDENTITY")
                factura_id = cursor.fetchone()[0]

                for entrada in entradas_boletos:
                    zona_nombre = entrada["zona_var"].get()
                    tipo_boleto = entrada["tipo_boleto_var"].get()
                    precio = PRECIOS_BOLETOS.get(tipo_boleto, 0.0)

                    # Crear un nuevo cliente (siempre se crea un nuevo cliente por cada venta)
                    nombre = simpledialog.askstring("Nuevo Cliente", "Ingrese el nombre del cliente:", parent=formulario_boletos)
                    if not nombre: return
                    apellido = simpledialog.askstring("Nuevo Cliente", "Ingrese el apellido del cliente:", parent=formulario_boletos)
                    if not apellido: return

                    cursor.execute("""
                        INSERT INTO Personas (Nombre, Apellido)
                        VALUES (?, ?)
                    """, (nombre, apellido))
                    mydb.commit()
                    cursor.execute("SELECT @@IDENTITY")
                    persona_id = cursor.fetchone()[0]
                    cursor.execute("""
                        INSERT INTO Clientes (PersonaID, Fecha_registro)
                        VALUES (?, GETDATE())
                    """, (persona_id,))
                    mydb.commit()
                    cliente_id = cursor.execute("SELECT @@IDENTITY").fetchone()[0]

                    # Obtener ZonaID
                    cursor.execute("SELECT ZonaID FROM Zonas WHERE Nombre_Zona = ?", (zona_nombre,))
                    zona_result = cursor.fetchone()
                    if not zona_result:
                        messagebox.showerror("Error", f"La zona '{zona_nombre}' no existe.")
                        return
                    zona_id = zona_result[0]

                    cursor.execute("""
                        INSERT INTO Boletos (ClienteID, ZonaID, FacturaID, Precio, Tipo_boleto, Fecha_visita)
                        VALUES (?, ?, ?, ?, ?, GETDATE())
                    """, (cliente_id, zona_id, factura_id, precio, tipo_boleto))

                mydb.commit()
                messagebox.showinfo("Éxito", f"Venta registrada exitosamente. Factura ID: {factura_id}")
                formulario_boletos.destroy()
                ventana_registro.destroy()

            except pyodbc.Error as ex:
                mydb.rollback()
                messagebox.showerror("Error", f"Error al registrar la venta: \n{ex}")
            except Exception as ex:
                mydb.rollback()
                messagebox.showerror("Error", f"Error general: \n{ex}")

        Button(formulario_boletos, text="Registrar Boletos", command=registrar_boletos_final).pack(pady=10)
        calcular_total()

    def pedir_cantidad_boletos():
        try:
            num_boletos = simpledialog.askinteger("Cantidad", "¿Cuántos boletos desea registrar?", parent=ventana_registro, minvalue=1)
            if num_boletos is not None:
                # Obtener la lista de zonas disponibles
                cursor = mydb.cursor()
                cursor.execute("SELECT Nombre_Zona FROM Zonas ORDER BY Nombre_Zona")
                zonas_disponibles = [row[0] for row in cursor.fetchall()]
                if not zonas_disponibles:
                    messagebox.showerror("Error", "No hay zonas disponibles para seleccionar.")
                    return
                mostrar_formulario_boletos(num_boletos, zonas_disponibles)
        except TclError: # Manejar el cierre de la ventana de diálogo sin ingresar valor
            pass

    pedir_cantidad_boletos()