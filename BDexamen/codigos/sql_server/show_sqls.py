from tkinter import *
from tkinter import messagebox
import pyodbc
from tkinter import ttk

def show(mydb):
    try:
        select_show = Toplevel()
        select_show.title("Seleccionar tabla para mostrar")
        select_show.iconbitmap("codigos/assets/BDICON.ico")

        def confirmacion():
            table_name = table_var.get()
            select_show.destroy()
            final_show(table_name)

        mycursor = mydb.cursor()
        mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_NAME <> 'sysdiagrams'")
        tables = [table[0] for table in mycursor.fetchall()]

        if not tables:
            messagebox.showerror("ERROR", "No hay tablas disponibles.")
            return

        table_var = StringVar()
        table_var.set(tables[0])  # Set default value

        for table in tables:
            Radiobutton(select_show, text=table, variable=table_var, value=table).pack(anchor=W, padx=10, pady=2)

        connfi = Button(select_show, text="Mostrar Tabla", command=confirmacion)
        connfi.pack(pady=10)

    except Exception as ex:
        messagebox.showerror("ERROR", f"El error es: \n{ex}")

    def final_show(table_name):
        the_show = Toplevel()
        the_show.title(f"Datos de la tabla: {table_name}")
        the_show.iconbitmap("codigos/assets/BDICON.ico")

        try:
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT * FROM {table_name};")
            records = mycursor.fetchall()

            mycursor.execute(f"""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}';
            """)
            columns = [col[0] for col in mycursor.fetchall()]

            if not records:
                Label(the_show, text=f"La tabla '{table_name}' está vacía.", padx=10, pady=10).pack()
                return

            # Crear un frame para el Treeview y la Scrollbar
            frame = ttk.Frame(the_show)
            frame.pack(fill='both', expand=True, padx=10, pady=10)

            # Crear Scrollbar vertical
            scrollbar_y = ttk.Scrollbar(frame, orient='vertical')
            scrollbar_y.pack(side='right', fill='y')

            # Crear Treeview
            tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar_y.set)

            # Configurar las columnas del Treeview
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100, anchor='w') # Ajusta el ancho según necesites

            # Insertar los datos en el Treeview
            for record in records:
                # Mostrar 'NULL' si el valor es None
                formatted_record = tuple(['NULL' if value is None else value for value in record])
                tree.insert('', END, values=formatted_record)

            # Configurar la Scrollbar para que funcione con el Treeview
            scrollbar_y.config(command=tree.yview)

            # Empaquetar el Treeview
            tree.pack(side='left', fill='both', expand=True)

        except Exception as ex:
            messagebox.showerror("ERROR", f"Error al mostrar la tabla '{table_name}': \n{ex}")
            
def consultar_zona_con_conteo(mydb):
    def mostrar_detalles(nombre_zona):
        try:
            cursor = mydb.cursor()
            cursor.execute("""
                SELECT COUNT(b.ZonaID) AS TotalVisitas
                FROM Boletos b
                JOIN Zonas z ON b.ZonaID = z.ZonaID
                WHERE z.Nombre_Zona = ?
            """, (nombre_zona,))
            resultado_conteo = cursor.fetchone()
            total_visitas = resultado_conteo[0] if resultado_conteo else 0

            cursor.execute("""
                SELECT DISTINCT p.Nombre, p.Apellido
                FROM Boletos b
                JOIN Zonas z ON b.ZonaID = z.ZonaID
                JOIN Clientes c ON b.ClienteID = c.ClienteID
                JOIN Personas p ON c.PersonaID = p.PersonaID
                WHERE z.Nombre_Zona = ?
                ORDER BY p.Apellido, p.Nombre
            """, (nombre_zona,))
            clientes_visitantes = cursor.fetchall()

            cursor.execute("""
                SELECT DISTINCT b.Fecha_visita
                FROM Boletos b
                JOIN Zonas z ON b.ZonaID = z.ZonaID
                WHERE z.Nombre_Zona = ?
                ORDER BY b.Fecha_visita
            """, (nombre_zona,))
            fechas_visita = [row[0] for row in cursor.fetchall()]

            detalles_ventana = Toplevel()
            detalles_ventana.title(f"Detalles de Visitas: {nombre_zona}")
            detalles_ventana.iconbitmap("codigos/assets/BDICON.ico")

            Label(detalles_ventana, text=f"Detalles de visitas para la zona '{nombre_zona}':", font=("Arial", 12, "bold")).pack(pady=5)
            Label(detalles_ventana, text=f"Total de visitas: {total_visitas}").pack(padx=10, pady=2, anchor="w")

            if clientes_visitantes:
                Label(detalles_ventana, text="Clientes visitantes:", font=("Arial", 10, "italic")).pack(padx=10, pady=2, anchor="w")
                for nombre, apellido in clientes_visitantes:
                    Label(detalles_ventana, text=f"- {nombre} {apellido}").pack(padx=20, pady=1, anchor="w")
            else:
                Label(detalles_ventana, text="Clientes visitantes: Ninguno").pack(padx=10, pady=2, anchor="w")

            if fechas_visita:
                Label(detalles_ventana, text="Fechas de visita:", font=("Arial", 10, "italic")).pack(padx=10, pady=2, anchor="w")
                for fecha in fechas_visita:
                    Label(detalles_ventana, text=f"- {fecha}").pack(padx=20, pady=1, anchor="w")
            else:
                Label(detalles_ventana, text="Fechas de visita: Ninguna").pack(padx=10, pady=2, anchor="w")

        except pyodbc.Error as ex:
            messagebox.showerror("ERROR", f"Error al consultar la base de datos: \n{ex}")
        except Exception as ex:
            messagebox.showerror("ERROR", f"Error general: \n{ex}")

    def seleccionar_zona():
        try:
            zona_seleccionada_index = lista_zonas.curselection()
            if zona_seleccionada_index:
                zona_seleccionada = lista_zonas.get(zona_seleccionada_index[0])
                ventana_seleccion_zona.destroy()
                mostrar_detalles(zona_seleccionada)
            else:
                messagebox.showinfo("Selección", "Por favor, seleccione una zona de la lista.")
        except TclError:
            messagebox.showerror("Error", "No se ha seleccionado ninguna zona.")


    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT Nombre_Zona FROM Zonas ORDER BY Nombre_Zona")
        zonas = [row[0] for row in cursor.fetchall()]

        if not zonas:
            messagebox.showinfo("Consulta de Zona", "No hay zonas registradas en la base de datos.")
            return

        ventana_seleccion_zona = Toplevel()
        ventana_seleccion_zona.title("Seleccionar Zona")
        ventana_seleccion_zona.iconbitmap("codigos/assets/BDICON.ico")

        Label(ventana_seleccion_zona, text="Seleccione una zona para ver el conteo y detalles de las visitas:", font=("Arial", 10)).pack(padx=10, pady=10)

        scrollbar = Scrollbar(ventana_seleccion_zona)
        scrollbar.pack(side=RIGHT, fill=Y)

        lista_zonas = Listbox(ventana_seleccion_zona, yscrollcommand=scrollbar.set, height=10, width=30)
        for zona in zonas:
            lista_zonas.insert(END, zona)
        lista_zonas.pack(padx=10, pady=10)

        scrollbar.config(command=lista_zonas.yview)

        boton_seleccionar = Button(ventana_seleccion_zona, text="Ver Conteo y Detalles", command=seleccionar_zona)
        boton_seleccionar.pack(pady=10)

    except pyodbc.Error as ex:
        messagebox.showerror("ERROR", f"Error al obtener la lista de zonas: \n{ex}")
    except Exception as ex:
        messagebox.showerror("ERROR", f"Error general: \n{ex}")

def consultar_cliente_boletos_gastado(mydb):
    def mostrar_gasto(nombre_cliente, apellido_cliente):
        try:
            cursor = mydb.cursor()
            query = """
                SELECT
                    per.Nombre,
                    per.Apellido,
                    f.NIT,
                    COUNT(b.FacturaID) AS CantidadBoletos,
                    SUM(b.Precio) AS TotalGastado
                FROM Clientes c
                JOIN Personas per ON c.PersonaID = per.PersonaID
                LEFT JOIN Boletos b ON c.ClienteID = b.ClienteID
                LEFT JOIN Facturas f ON b.FacturaID = f.FacturaID
                WHERE per.Nombre LIKE ? AND per.Apellido LIKE ?
                GROUP BY per.Nombre, per.Apellido, f.NIT
                ORDER BY per.Apellido, per.Nombre
            """
            nombre_param = f"{nombre_cliente}%" if nombre_cliente else "%"
            apellido_param = f"{apellido_cliente}%" if apellido_cliente else "%"
            cursor.execute(query, (nombre_param, apellido_param))
            resultados = cursor.fetchall()

            if resultados:
                resultados_ventana = Toplevel()
                resultados_ventana.title("Clientes - Boletos Comprados y Gastado")
                resultados_ventana.iconbitmap("codigos/assets/BDICON.ico")

                canvas = Canvas(resultados_ventana)
                scrollbar = Scrollbar(resultados_ventana, orient="vertical", command=canvas.yview)
                scrollable_frame = Frame(canvas)

                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(
                        scrollregion=canvas.bbox("all")
                    )
                )

                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                Label(scrollable_frame, text="Resultados de la búsqueda:", font=("Arial", 12, "bold")).pack(pady=5)
                for row in resultados:
                    nombre, apellido, nit, cantidad, total_gastado = row
                    Label(scrollable_frame, text=f"Nombre: {nombre} {apellido}").pack(padx=10, pady=2, anchor="w")
                    Label(scrollable_frame, text=f"NIT: {nit if nit else 'Sin NIT asociado'}").pack(padx=10, pady=2, anchor="w")
                    Label(scrollable_frame, text=f"Boletos Comprados: {cantidad}").pack(padx=10, pady=2, anchor="w")
                    Label(scrollable_frame, text=f"Total Gastado: {total_gastado:.2f}").pack(padx=10, pady=2, anchor="w")
                    Label(scrollable_frame, text="-" * 30).pack(pady=5)
            else:
                messagebox.showinfo("Consulta", "No se encontraron clientes con ese nombre.")

        except pyodbc.Error as ex:
            messagebox.showerror("ERROR", f"Error al consultar la base de datos: \n{ex}")
        except Exception as ex:
            messagebox.showerror("ERROR", f"Error general: \n{ex}")

    ventana_buscar = Toplevel()
    ventana_buscar.title("Buscar Cliente")
    ventana_buscar.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_buscar, text="Nombre del Cliente:", font=("Arial", 10)).pack(padx=10, pady=10)
    nombre_entry = Entry(ventana_buscar)
    nombre_entry.pack(padx=10, pady=5)

    Label(ventana_buscar, text="Apellido del Cliente:", font=("Arial", 10)).pack(padx=10, pady=10)
    apellido_entry = Entry(ventana_buscar)
    apellido_entry.pack(padx=10, pady=5)

    buscar_button = Button(ventana_buscar, text="Buscar", command=lambda: mostrar_gasto(nombre_entry.get().strip(), apellido_entry.get().strip()))
    buscar_button.pack(pady=10)

def mostrar_total_visitas_por_zona(mydb):
    try:
        cursor = mydb.cursor()
        query = """
        SELECT
            b.ZonaID,
            z.Nombre_Zona,
            COUNT(b.ClienteID) AS TotalVisitas
        FROM Boletos b
        JOIN Zonas z ON b.ZonaID = z.ZonaID
        GROUP BY b.ZonaID, z.Nombre_Zona
        ORDER BY TotalVisitas DESC;
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        resultados_ventana = Toplevel()
        resultados_ventana.title("Total de Visitas por Zona")
        resultados_ventana.iconbitmap("codigos/assets/BDICON.ico")

        # Crear Canvas y Scrollbar
        canvas = Canvas(resultados_ventana)
        scrollbar = Scrollbar(resultados_ventana, orient="vertical", command=canvas.yview)
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

        if resultados:
            Label(scrollable_frame, text="Total de Visitas por Zona:", font=("Arial", 12, "bold")).pack(pady=5)
            for resultado in resultados:
                Label(scrollable_frame, text=f"Zona ID: {resultado[0]}").pack(pady=2)
                Label(scrollable_frame, text=f"Nombre de la Zona: {resultado[1]}").pack(pady=2)
                Label(scrollable_frame, text=f"Total Visitas: {resultado[2]}").pack(pady=2)
                Label(scrollable_frame, text="-" * 20).pack()
        else:
            Label(scrollable_frame, text="No hay visitas registradas.").pack(pady=10)

    except Exception as ex:
        messagebox.showerror("ERROR", f"Error al realizar la consulta: \n{ex}")

def mostrar_facturas_por_cliente(mydb):
    def mostrar_resultados(nombre, apellido):
        try:
            cursor = mydb.cursor()
            query = """
            SELECT
                f.FacturaID,
                p.Nombre,
                p.Apellido,
                b.ZonaID,
                z.Nombre_Zona
            FROM Facturas f
            JOIN Boletos b ON f.FacturaID = b.FacturaID
            JOIN Clientes cli ON b.ClienteID = cli.ClienteID
            JOIN Personas p ON cli.PersonaID = p.PersonaID
            JOIN Zonas z ON b.ZonaID = z.ZonaID
            WHERE p.Nombre LIKE ? OR p.Apellido LIKE ?
            ORDER BY p.Apellido, p.Nombre, f.FacturaID;
            """
            nombre_param = f"{nombre}%" if nombre else "%"
            apellido_param = f"{apellido}%" if apellido else "%"
            cursor.execute(query, (nombre_param, apellido_param))
            resultados = cursor.fetchall()

            resultados_ventana = Toplevel()
            resultados_ventana.title("Facturas por Cliente")
            resultados_ventana.iconbitmap("codigos/assets/BDICON.ico")

            # Crear Canvas y Scrollbar
            canvas = Canvas(resultados_ventana)
            scrollbar = Scrollbar(resultados_ventana, orient="vertical", command=canvas.yview)
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

            if resultados:
                Label(scrollable_frame, text="Facturas por Cliente:", font=("Arial", 12, "bold")).pack(pady=5)
                factura_actual = None
                for resultado in resultados:
                    factura_id, nombre_cliente, apellido_cliente, zona_id, nombre_zona = resultado
                    if factura_id != factura_actual:
                        if factura_actual is not None:
                            Label(scrollable_frame, text="-" * 30).pack()
                        Label(scrollable_frame, text=f"Factura ID: {factura_id}", font=("Arial", 10, "bold")).pack(pady=2)
                        Label(scrollable_frame, text=f"Cliente: {nombre_cliente} {apellido_cliente}", font=("Arial", 10, "italic")).pack(pady=2)
                        factura_actual = factura_id
                    Label(scrollable_frame, text=f"  Zona ID: {zona_id}, Nombre: {nombre_zona}").pack(padx=10, pady=1)
                Label(scrollable_frame, text="-" * 30).pack() # Separador final
            else:
                mensaje = "No se encontraron facturas para el nombre o apellido especificado."
                Label(scrollable_frame, text=mensaje).pack(pady=10)

        except Exception as ex:
            messagebox.showerror("ERROR", f"Error al realizar la consulta: \n{ex}")

    ventana_input = Toplevel()
    ventana_input.title("Ingrese Nombre y/o Apellido del Cliente")
    ventana_input.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_input, text="Ingrese el Nombre (opcional):").pack(padx=10, pady=5)
    nombre_entry = Entry(ventana_input)
    nombre_entry.pack(padx=10, pady=5)

    Label(ventana_input, text="Ingrese el Apellido (opcional):").pack(padx=10, pady=5)
    apellido_entry = Entry(ventana_input)
    apellido_entry.pack(padx=10, pady=5)

    def realizar_consulta():
        nombre = nombre_entry.get().strip()
        apellido = apellido_entry.get().strip()
        ventana_input.destroy()
        mostrar_resultados(nombre, apellido)

    Button(ventana_input, text="Buscar Facturas", command=realizar_consulta).pack(pady=10)

def mostrar_historial_boletos_cliente(mydb):
    def mostrar_historial(nombre_cliente, apellido_cliente):
        try:
            cursor = mydb.cursor()
            query = """
                SELECT
                    f.FacturaID,
                    f.Nit,
                    per.Nombre AS NombreCliente,
                    per.Apellido AS ApellidoCliente,
                    b.Precio,
                    z.Nombre_Zona,
                    b.Tipo_boleto,
                    b.Fecha_visita
                FROM Boletos b
                JOIN Facturas f ON b.FacturaID = f.FacturaID
                JOIN Clientes c ON b.ClienteID = c.ClienteID
                JOIN Personas per ON c.PersonaID = per.PersonaID
                JOIN Zonas z ON b.ZonaID = z.ZonaID
                WHERE per.Nombre LIKE ? AND per.Apellido LIKE ?
                ORDER BY f.FacturaID, b.Fecha_visita
            """
            nombre_param = f"{nombre_cliente}%" if nombre_cliente else "%"
            apellido_param = f"{apellido_cliente}%" if apellido_cliente else "%"
            cursor.execute(query, (nombre_param, apellido_param))
            historial = cursor.fetchall()

            historial_ventana = Toplevel()
            historial_ventana.title("Historial de Boletos del Cliente")
            historial_ventana.iconbitmap("codigos/assets/BDICON.ico")

            canvas = Canvas(historial_ventana)
            scrollbar = Scrollbar(historial_ventana, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            if historial:
                historial_por_factura = {}
                for row in historial:
                    factura_id, nit, nombre_cli, apellido_cli, precio, nombre_zona, tipo_boleto, fecha_visita = row
                    if factura_id not in historial_por_factura:
                        historial_por_factura[factura_id] = {
                            'nit': nit,
                            'nombre_cliente': f"{nombre_cli} {apellido_cli}",
                            'boletos': []
                        }
                    historial_por_factura[factura_id]['boletos'].append({
                        'precio': precio,
                        'nombre_zona': nombre_zona,
                        'tipo_boleto': tipo_boleto,
                        'fecha_visita': fecha_visita
                    })

                Label(scrollable_frame, text="Historial de boletos por factura:", font=("Arial", 12, "bold")).pack(pady=5)
                for factura_id, detalles_factura in historial_por_factura.items():
                    Label(scrollable_frame, text=f"Cliente: {detalles_factura['nombre_cliente']}", font=("Arial", 10, "italic")).pack(padx=10, pady=2, anchor="w")
                    Label(scrollable_frame, text=f"NIT: {detalles_factura['nit']}", font=("Arial", 10, "italic")).pack(padx=10, pady=2, anchor="w")
                    Label(scrollable_frame, text=f"Factura ID: {factura_id}", font=("Arial", 11, "bold")).pack(padx=10, pady=2, anchor="w")
                    Label(scrollable_frame, text="-" * 30).pack(pady=2)
                    for boleto in detalles_factura['boletos']:
                        Label(scrollable_frame, text=f"  Precio: {boleto['precio']}").pack(padx=20, pady=1, anchor="w")
                        Label(scrollable_frame, text=f"  Zona: {boleto['nombre_zona']}").pack(padx=20, pady=1, anchor="w")
                        Label(scrollable_frame, text=f"  Tipo de Boleto: {boleto['tipo_boleto']}").pack(padx=20, pady=1, anchor="w")
                        Label(scrollable_frame, text=f"  Fecha de Visita: {boleto['fecha_visita']}").pack(padx=20, pady=1, anchor="w")
                    Label(scrollable_frame, text="-" * 30).pack(pady=5)

            else:
                Label(scrollable_frame, text=f"No se encontró historial de boletos para: {nombre_cliente} {apellido_cliente}").pack(pady=10)

        except pyodbc.Error as ex:
            messagebox.showerror("ERROR", f"Error al consultar la base de datos: \n{ex}")
        except Exception as ex:
            messagebox.showerror("ERROR", f"Error general: \n{ex}")

    ventana_buscar = Toplevel()
    ventana_buscar.title("Buscar Historial por Nombre")
    ventana_buscar.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_buscar, text="Nombre del Cliente:", font=("Arial", 10)).pack(padx=10, pady=10)
    nombre_entry = Entry(ventana_buscar)
    nombre_entry.pack(padx=10, pady=5)

    Label(ventana_buscar, text="Apellido del Cliente:", font=("Arial", 10)).pack(padx=10, pady=10)
    apellido_entry = Entry(ventana_buscar)
    apellido_entry.pack(padx=10, pady=5)

    buscar_button = Button(ventana_buscar, text="Buscar Historial", command=lambda: mostrar_historial(nombre_entry.get().strip(), apellido_entry.get().strip()))
    buscar_button.pack(pady=10)

def mostrar_vista_reporte_ventas(mydb):
    try:
        cursor = mydb.cursor()
        query = "SELECT Nombre, Apellido, Precio, FacturaID, Nombre_Zona FROM Vista_Reporte_Ventas;"
        cursor.execute(query)
        resultados = cursor.fetchall()

        resultados_ventana = Toplevel()
        resultados_ventana.title("Reporte de Ventas")
        resultados_ventana.iconbitmap("codigos/assets/BDICON.ico")

        # Crear Canvas y Scrollbar
        canvas = Canvas(resultados_ventana)
        scrollbar = Scrollbar(resultados_ventana, orient="vertical", command=canvas.yview)
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

        if resultados:
            Label(scrollable_frame, text="Reporte de Ventas:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=5, pady=5)
            # Mostrar encabezados con grid
            encabezados = ["Nombre", "Apellido", "Precio", "Factura ID", "Zona"]
            for i, encabezado in enumerate(encabezados):
                Label(scrollable_frame, text=encabezado, font=("Arial", 10, "bold")).grid(row=1, column=i, padx=5, pady=2)

            for i, resultado in enumerate(resultados, start=2):
                nombre, apellido, precio, factura_id, nombre_zona = resultado
                Label(scrollable_frame, text=nombre).grid(row=i, column=0, padx=5, pady=2, sticky="w")
                Label(scrollable_frame, text=apellido).grid(row=i, column=1, padx=5, pady=2, sticky="w")
                Label(scrollable_frame, text=precio).grid(row=i, column=2, padx=5, pady=2, sticky="e")
                Label(scrollable_frame, text=factura_id).grid(row=i, column=3, padx=5, pady=2, sticky="w")
                Label(scrollable_frame, text=nombre_zona).grid(row=i, column=4, padx=5, pady=2, sticky="w")
        else:
            Label(scrollable_frame, text="No se encontraron datos en la vista.").pack(pady=10) # Aquí podríamos usar grid también

    except Exception as ex:
        messagebox.showerror("ERROR", f"Error al mostrar la vista: \n{ex}")
def ejecutar_procedimiento_boletos_cliente(mydb):
    def mostrar_resultados(nombre, apellido):
        try:
            cursor = mydb.cursor()
            cursor.execute("EXEC ObtenerBoletosClienteAvanzado @Nombre=?, @Apellido=?", (nombre, apellido))
            resultados = cursor.fetchall()

            resultados_ventana = Toplevel()
            resultados_ventana.title("Boletos por Cliente (Procedimiento)")
            resultados_ventana.iconbitmap("codigos/assets/BDICON.ico")

            # Crear Canvas y Scrollbar
            canvas = Canvas(resultados_ventana)
            scrollbar = Scrollbar(resultados_ventana, orient="vertical", command=canvas.yview)
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

            if resultados:
                Label(scrollable_frame, text="Boletos por Cliente:", font=("Arial", 12, "bold")).pack(pady=5)
                for resultado in resultados:
                    factura_id, cantidaddeboletos, precio, tipoboleto, zona_id, nombre_zona = resultado
                    Label(scrollable_frame, text=f"Factura ID: {factura_id}").pack(pady=2)
                    Label(scrollable_frame, text=f"  Cantidad de Boletos: {cantidaddeboletos}").pack(padx=10)
                    Label(scrollable_frame, text=f"  Precio: {precio}").pack(padx=10)
                    Label(scrollable_frame, text=f"  Tipo de Boleto: {tipoboleto}").pack(padx=10)
                    Label(scrollable_frame, text=f"  Zona ID: {zona_id}, Nombre: {nombre_zona}").pack(padx=10)
            else:
                mensaje = "No se encontraron boletos para el nombre o apellido especificado."
                Label(scrollable_frame, text=mensaje).pack(pady=10)

        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            if sqlstate == '42000':
                messagebox.showerror("ERROR", f"Error al ejecutar el procedimiento:\nVerifica que el procedimiento 'ObtenerBoletosClienteAvanzado' exista en la base de datos.")
            else:
                messagebox.showerror("ERROR", f"Error al ejecutar el procedimiento: \n{ex}")
        except Exception as ex:
            messagebox.showerror("ERROR", f"Error general: \n{ex}")

    ventana_input = Toplevel()
    ventana_input.title("Ingrese Nombre y/o Apellido del Cliente")
    ventana_input.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_input, text="Ingrese el Nombre (opcional):").pack(padx=10, pady=5)
    nombre_entry = Entry(ventana_input)
    nombre_entry.pack(padx=10, pady=5)

    Label(ventana_input, text="Ingrese el Apellido (opcional):").pack(padx=10, pady=5)
    apellido_entry = Entry(ventana_input)
    apellido_entry.pack(padx=10, pady=5)

    def realizar_consulta():
        nombre = nombre_entry.get().strip()
        apellido = apellido_entry.get().strip()
        ventana_input.destroy()
        mostrar_resultados(nombre, apellido)

    Button(ventana_input, text="Buscar Boletos", command=realizar_consulta).pack(pady=10)
def mostrar_boletos_vendedor(mydb):
    def mostrar_resultados(nombre, apellido):
        try:
            cursor = mydb.cursor()
            query = """
            SELECT
                p.Nombre AS NombreCliente,
                p.Apellido AS ApellidoCliente,
                f.FacturaID,
                b.Precio,
                z.Nombre_Zona,
                b.Fecha_visita
            FROM Boletos b
            JOIN Facturas f ON b.FacturaID = f.FacturaID
            JOIN Clientes c ON b.ClienteID = c.ClienteID
            JOIN Personas p ON c.PersonaID = p.PersonaID
            JOIN Zonas z ON b.ZonaID = z.ZonaID
            WHERE p.Nombre LIKE ? OR p.Apellido LIKE ?;
            """
            nombre_param = f"{nombre}%" if nombre else "%"
            apellido_param = f"{apellido}%" if apellido else "%"
            cursor.execute(query, (nombre_param, apellido_param))
            resultados = cursor.fetchall()

            resultados_ventana = Toplevel()
            resultados_ventana.title("Consulta de Boletos (Vendedor)")
            resultados_ventana.iconbitmap("codigos/assets/BDICON.ico")

            # Crear Canvas y Scrollbar
            canvas = Canvas(resultados_ventana)
            scrollbar = Scrollbar(resultados_ventana, orient="vertical", command=canvas.yview)
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

            if resultados:
                Label(scrollable_frame, text="Boletos Encontrados:", font=("Arial", 12, "bold")).pack(pady=5)
                for resultado in resultados:
                    nombre_cliente, apellido_cliente, factura_id, precio, nombre_zona, fecha_visita = resultado
                    Label(scrollable_frame, text=f"Cliente: {nombre_cliente} {apellido_cliente}").pack(pady=2)
                    Label(scrollable_frame, text=f"  Factura ID: {factura_id}").pack(padx=10)
                    Label(scrollable_frame, text=f"  Precio: {precio}").pack(padx=10)
                    Label(scrollable_frame, text=f"  Zona: {nombre_zona}").pack(padx=10)
                    Label(scrollable_frame, text=f"  Fecha Visita: {fecha_visita}").pack(padx=10)
            else:
                mensaje = "No se encontraron boletos para el nombre o apellido especificado."
                Label(scrollable_frame, text=mensaje).pack(pady=10)

        except Exception as ex:
            messagebox.showerror("ERROR", f"Error al realizar la consulta: \n{ex}")

    ventana_input = Toplevel()
    ventana_input.title("Buscar Boletos (Vendedor)")
    ventana_input.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_input, text="Ingrese el Nombre del Cliente (opcional):").pack(padx=10, pady=5)
    nombre_entry = Entry(ventana_input)
    nombre_entry.pack(padx=10, pady=5)

    Label(ventana_input, text="Ingrese el Apellido del Cliente (opcional):").pack(padx=10, pady=5)
    apellido_entry = Entry(ventana_input)
    apellido_entry.pack(padx=10, pady=5)

    def realizar_consulta():
        nombre = nombre_entry.get().strip()
        apellido = apellido_entry.get().strip()
        ventana_input.destroy()
        mostrar_resultados(nombre, apellido)

    Button(ventana_input, text="Buscar", command=realizar_consulta).pack(pady=10)

def mostrar_tabla_auditoria_empleados(mydb):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT ID_Auditoria, EmpleadoID, Cambio, DetalleCambio, Fecha, Usuario FROM Auditoria_Empleados")
        registros_auditoria = cursor.fetchall()

        if not registros_auditoria:
            messagebox.showinfo("Auditoría de Empleados", "La tabla Auditoria_Empleados está vacía.")
            return

        ventana_auditoria = Toplevel()
        ventana_auditoria.title("Tabla Auditoria_Empleados")
        ventana_auditoria.iconbitmap("codigos/assets/BDICON.ico")

        tree = ttk.Treeview(ventana_auditoria, columns=("ID_Auditoria", "EmpleadoID", "Cambio", "DetalleCambio", "Fecha", "Usuario"), show="headings")

        # Definir encabezados de las columnas
        tree.heading("ID_Auditoria", text="ID Auditoría")
        tree.heading("EmpleadoID", text="Empleado ID")
        tree.heading("Cambio", text="Cambio")
        tree.heading("DetalleCambio", text="Detalle del Cambio")
        tree.heading("Fecha", text="Fecha")
        tree.heading("Usuario", text="Usuario")

        # Establecer un ancho fijo para cada columna
        ancho_fijo = 150
        tree.column("ID_Auditoria", width=ancho_fijo)
        tree.column("EmpleadoID", width=ancho_fijo)
        tree.column("Cambio", width=ancho_fijo)
        tree.column("DetalleCambio", width=ancho_fijo)
        tree.column("Fecha", width=ancho_fijo)
        tree.column("Usuario", width=ancho_fijo)

        # Insertar los datos en la tabla
        for registro in registros_auditoria:
            tree.insert("", END, values=registro)

        # Agregar scrollbars si es necesario
        scrollbar_vertical = Scrollbar(ventana_auditoria, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.pack(side=RIGHT, fill=Y)

        scrollbar_horizontal = Scrollbar(ventana_auditoria, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side=BOTTOM, fill=X)

        tree.pack(fill="both", expand=True)

    except pyodbc.Error as ex:
        messagebox.showerror("ERROR", f"Error al consultar la tabla Auditoria_Empleados: \n{ex}")
    except Exception as ex:
        messagebox.showerror("ERROR", f"Error general: \n{ex}")
