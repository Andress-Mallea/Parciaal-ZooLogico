from tkinter import *
from tkinter import messagebox
import pyodbc

def show(mydb): 
    try:
        select_show = Toplevel()
        select_show.title("Base de datos god")
        select_show.iconbitmap("codigos/assets/BDICON.ico")
        
        def confirmacion():
            table_name = table_var.get()
            select_show.destroy()
            final_show(table_name)
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';")
        tables = [table[0] for table in mycursor.fetchall() if 'sysdiagrams' not in table[0].lower()]
        
        if not tables:
            messagebox.showerror("ERROR", "No hay tablas disponibles.")
            return
        
        table_var = StringVar()
        table_var.set(tables[0])  # Set default value
        
        for table in tables:
            Radiobutton(select_show, text=table, variable=table_var, value=table).pack(anchor=W)
        
        connfi = Button(select_show, text="Confirmar", command=confirmacion)
        connfi.pack()
        
        def final_show(table_name):
            mycursor = mydb.cursor()
            mycursor.execute(f"SELECT * FROM {table_name};")
            records = mycursor.fetchall()
            the_show = Toplevel()
            the_show.title("Base de datos god")
            the_show.iconbitmap("codigos/assets/BDICON.ico")
            
            mycursor.execute(f"""SELECT COLUMN_NAME 
                                FROM INFORMATION_SCHEMA.COLUMNS
                                WHERE TABLE_NAME = '{table_name}';
                                """)
            columns = [col[0] for col in mycursor.fetchall()]
            m = Label(the_show, text=', '.join(columns))
            m.pack()
            
            for record in records:
                n = Label(the_show, text=record)
                n.pack()
    
    except Exception as ex:
        messagebox.showerror("ERROR", f"El error es: \n{ex}")

def consultar_zona_con_conteo(mydb):
    def mostrar_resultado(zona_id):
        try:
            cursor = mydb.cursor()
            query = """
            SELECT
                z.ZonaID,
                z.Nombre_Zona,
                COUNT(a.AnimalID) AS Total_Animales
            FROM Zonas z
            LEFT JOIN Animales a ON z.ZonaID = a.ZonaID
            WHERE z.ZonaID = ?
            GROUP BY z.ZonaID, z.Nombre_Zona;
            """
            cursor.execute(query, (zona_id,))
            resultado = cursor.fetchone()

            resultado_ventana = Toplevel()
            resultado_ventana.title("Consulta por Zona")
            resultado_ventana.iconbitmap("codigos/assets/BDICON.ico")

            if resultado:
                Label(resultado_ventana, text=f"Zona ID: {resultado[0]}").pack(pady=5)
                Label(resultado_ventana, text=f"Nombre de la Zona: {resultado[1]}").pack(pady=5)
                Label(resultado_ventana, text=f"Total de Animales: {resultado[2]}").pack(pady=5)
            else:
                Label(resultado_ventana, text=f"No se encontró la Zona con ID: {zona_id}").pack(pady=10)

        except Exception as ex:
            messagebox.showerror("ERROR", f"Error al realizar la consulta: \n{ex}")

    ventana_input = Toplevel()
    ventana_input.title("Ingrese ID de Zona")
    ventana_input.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_input, text="Ingrese el ID de la Zona:").pack(padx=10, pady=10)
    zona_id_entry = Entry(ventana_input)
    zona_id_entry.pack(padx=10, pady=5)

    def obtener_id():
        try:
            zona_id = int(zona_id_entry.get())
            ventana_input.destroy()
            mostrar_resultado(zona_id)
        except ValueError:
            messagebox.showerror("ERROR", "Por favor, ingrese un ID de Zona válido (número entero).")

    Button(ventana_input, text="Consultar", command=obtener_id).pack(pady=10)
def consultar_cliente_boletos_gastado(mydb):
    def mostrar_resultados(nombre, apellido):
        try:
            cursor = mydb.cursor()
            query = """
            SELECT
                p.Nombre,
                p.Apellido,
                COUNT(b.ClienteID) AS Total_Boletos,
                SUM(b.Precio) AS Total_Gastado
            FROM Clientes cli
            JOIN Personas p ON cli.PersonaID = p.PersonaID
            JOIN Boletos b ON cli.ClienteID = b.ClienteID
            WHERE p.Nombre LIKE ? OR p.Apellido LIKE ?
            GROUP BY p.Nombre, p.Apellido;
            """
            nombre_param = f"{nombre}%" if nombre else "%"
            apellido_param = f"{apellido}%" if apellido else "%"
            cursor.execute(query, (nombre_param, apellido_param))
            resultados = cursor.fetchall()

            resultados_ventana = Toplevel()
            resultados_ventana.title("Consulta de Clientes")
            resultados_ventana.iconbitmap("codigos/assets/BDICON.ico")

            if resultados:
                Label(resultados_ventana, text="Resultados de la búsqueda:", font=("Arial", 12, "bold")).pack(pady=5)
                for resultado in resultados:
                    Label(resultados_ventana, text=f"Nombre: {resultado[0]}").pack(pady=2)
                    Label(resultados_ventana, text=f"Apellido: {resultado[1]}").pack(pady=2)
                    Label(resultados_ventana, text=f"Total Boletos: {resultado[2]}").pack(pady=2)
                    Label(resultados_ventana, text=f"Total Gastado: {resultado[3]}").pack(pady=2)
                    Label(resultados_ventana, text="-" * 20).pack()
            else:
                mensaje = "No se encontraron clientes con el nombre o apellido especificado."
                Label(resultados_ventana, text=mensaje).pack(pady=10)

        except Exception as ex:
            messagebox.showerror("ERROR", f"Error al realizar la consulta: \n{ex}")

    ventana_input = Toplevel()
    ventana_input.title("Ingrese Nombre y/o Apellido")
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

    Button(ventana_input, text="Buscar", command=realizar_consulta).pack(pady=10)

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
    def mostrar_resultados(cliente_id):
        try:
            cursor = mydb.cursor()
            query = """
            WITH HistorialBoletos AS (
                SELECT
                    b.Precio,
                    z.Nombre_Zona,
                    f.FacturaID
                FROM Boletos b
                JOIN Facturas f ON b.FacturaID = f.FacturaID
                JOIN Clientes cli ON b.ClienteID = cli.ClienteID
                JOIN Zonas z ON b.ZonaID = z.ZonaID
                WHERE cli.ClienteID = ?
            )
            SELECT
                FacturaID,
                Precio,
                Nombre_Zona,
                COUNT(*) OVER() AS Total_Boletos_Cliente
            FROM HistorialBoletos;
            """
            cursor.execute(query, (cliente_id,))
            resultados = cursor.fetchall()

            resultados_ventana = Toplevel()
            resultados_ventana.title(f"Historial de Boletos del Cliente {cliente_id}")
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
                total_boletos = resultados[0][3] if resultados else 0
                Label(scrollable_frame, text=f"Historial de Boletos - Cliente ID: {cliente_id}", font=("Arial", 12, "bold")).pack(pady=5)
                Label(scrollable_frame, text=f"Total de Boletos Comprados: {total_boletos}", font=("Arial", 10, "italic")).pack(pady=5)
                Label(scrollable_frame, text=" ".join((str(i) for i in range(5)))).pack()
                for resultado in resultados:
                    factura_id, precio, nombre_zona, _ = resultado
                    Label(scrollable_frame, text=f"Factura ID: {factura_id}").pack(pady=2)
                    Label(scrollable_frame, text=f"  Precio: {precio}").pack(padx=10)
                    Label(scrollable_frame, text=f"  Zona Visitada: {nombre_zona}").pack(padx=10)
            else:
                mensaje = f"No se encontraron boletos para el Cliente ID: {cliente_id}"
                Label(scrollable_frame, text=mensaje).pack(pady=10)

        except Exception as ex:
            messagebox.showerror("ERROR", f"Error al realizar la consulta: \n{ex}")

    ventana_input = Toplevel()
    ventana_input.title("Ingrese Cliente ID")
    ventana_input.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_input, text="Ingrese el ID del Cliente:").pack(padx=10, pady=10)
    cliente_id_entry = Entry(ventana_input)
    cliente_id_entry.pack(padx=10, pady=5)

    def realizar_consulta():
        try:
            cliente_id = int(cliente_id_entry.get())
            ventana_input.destroy()
            mostrar_resultados(cliente_id)
        except ValueError:
            messagebox.showerror("ERROR", "Por favor, ingrese un ID de Cliente válido (número entero).")

    Button(ventana_input, text="Mostrar Historial", command=realizar_consulta).pack(pady=10)
    
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

