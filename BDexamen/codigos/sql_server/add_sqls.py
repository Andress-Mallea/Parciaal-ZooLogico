from tkinter import *
from tkinter import messagebox
import pyodbc

def add(mydb): 
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
        tables = [table[0] for table in mycursor.fetchall() if 'sysdiagram' not in table[0].lower()]

        if not tables:
            messagebox.showerror("ERROR", "No hay tablas disponibles que no sean sysdiagrams.")
            return

        table_var = StringVar()
        table_var.set(tables[0])  # Set default value

        for table in tables:
            Radiobutton(select_show, text=table, variable=table_var, value=table).pack(anchor=W)

        connfi = Button(select_show, text="Confirmar", command=confirmacion)
        connfi.pack()
        
        def obtener_nombres_columnas(table_name):
            cursor = mydb.cursor()
            cursor.execute(f"""SELECT COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = '{table_name}';
                        """)
            columnas = cursor.fetchall()
            nombres_columnas = [columna[0] for columna in columnas]
            return nombres_columnas

        def final_show(table_name):
            columnas = obtener_nombres_columnas(table_name)
            the_show = Toplevel()
            the_show.title(f"Añadir datos a {table_name}")
            the_show.iconbitmap("codigos/assets/BDICON.ico")
            entries = {}
            for i, columna in enumerate(columnas):
                label = Label(the_show, text=columna)
                label.grid(row=i, column=0, padx=10, pady=5)
                entry = Entry(the_show)
                entry.grid(row=i, column=1, padx=10, pady=5)
                entries[columna] = entry

            def insertar_registro():
                valores = [entry.get() for entry in entries.values()]
                columnas_str = ", ".join([f"[{columna}]" for columna in columnas])
                valores_str = ", ".join([f"{valor}" if valor.isdigit() else f"'{valor}'" for valor in valores])
                
                try:
                    cursor = mydb.cursor()
                    cursor.execute(f"INSERT INTO {table_name} ({columnas_str}) VALUES ({valores_str})")
                    mydb.commit()
                    messagebox.showinfo("Éxito", "Registro añadido exitosamente")
                    the_show.destroy()
                except Exception as ex:
                    messagebox.showerror("ERROR", f"El error es: \n{ex}")

            def cancelar():
                the_show.destroy()

            boton_insertar = Button(the_show, text="Insertar", command=insertar_registro)
            boton_insertar.grid(row=len(columnas), column=0, pady=10)
            boton_cancelar = Button(the_show, text="Cancelar", command=cancelar)
            boton_cancelar.grid(row=len(columnas), column=1, pady=10)

    except Exception as ex:
        messagebox.showerror("ERROR", f"El error es: \n{ex}")

def registrar_venta_pendiente(mydb):
    def mostrar_formulario_boletos(num_boletos):
        formulario_boletos = Toplevel(ventana_registro)
        formulario_boletos.title("Detalles de Boletos")
        formulario_boletos.iconbitmap("codigos/assets/BDICON.ico")

        entradas_boletos = []
        for i in range(num_boletos):
            Label(formulario_boletos, text=f"--- Boleto {i+1} ---").pack(pady=5)
            frame_boleto = Frame(formulario_boletos)
            frame_boleto.pack(pady=2)

            Label(frame_boleto, text="Zona ID:").grid(row=0, column=0, padx=5, pady=5)
            zona_id_entry = Entry(frame_boleto)
            zona_id_entry.grid(row=0, column=1, padx=5, pady=5)

            Label(frame_boleto, text="Precio:").grid(row=1, column=0, padx=5, pady=5)
            precio_entry = Entry(frame_boleto)
            precio_entry.grid(row=1, column=1, padx=5, pady=5)

            Label(frame_boleto, text="Tipo de Boleto:").grid(row=2, column=0, padx=5, pady=5)
            tipo_boleto_entry = Entry(frame_boleto)
            tipo_boleto_entry.grid(row=2, column=1, padx=5, pady=5)

            Label(frame_boleto, text="Fecha Visita (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
            fecha_visita_entry = Entry(frame_boleto)
            fecha_visita_entry.grid(row=3, column=1, padx=5, pady=5)

            entradas_boletos.append({
                "zona_id": zona_id_entry,
                "precio": precio_entry,
                "tipo_boleto": tipo_boleto_entry,
                "fecha_visita": fecha_visita_entry
            })

        def registrar_boletos():
            datos_boletos = []
            for entrada in entradas_boletos:
                zona_id = entrada["zona_id"].get().strip()
                precio = entrada["precio"].get().strip()
                tipo_boleto = entrada["tipo_boleto"].get().strip()
                fecha_visita = entrada["fecha_visita"].get().strip()
                datos_boletos.append((zona_id, precio, tipo_boleto, fecha_visita))

            factura_temporal_id = factura_temporal_entry.get().strip()
            cliente_id = cliente_id_entry.get().strip()
            nit = nit_entry.get().strip()
            cantidad_boletos = len(datos_boletos) # Usar la cantidad real de boletos
            total = total_entry.get().strip()

            try:
                cursor = mydb.cursor()

                for zona_id, precio, tipo_boleto, fecha_visita in datos_boletos:
                    cursor.execute("""
                        INSERT INTO VentasPendientes (FacturaTemporalID, ClienteID, ZonaID, Precio, Tipo_boleto, Fecha_visita)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (factura_temporal_id, cliente_id, zona_id, precio, tipo_boleto, fecha_visita))

                # Insertar en Facturas
                cursor.execute("""
                    INSERT INTO Facturas (Nit, CantidadDeBoletos, Total)
                    VALUES (?, ?, ?)
                """, (nit, cantidad_boletos, total))

                mydb.commit()
                messagebox.showinfo("Éxito", "Venta pendiente y factura registrada.")
                ventana_registro.destroy()
                formulario_boletos.destroy()

            except pyodbc.Error as ex:
                mydb.rollback()
                messagebox.showerror("Error", f"Error al registrar la venta: \n{ex}")
            except Exception as ex:
                mydb.rollback()
                messagebox.showerror("Error", f"Error general: \n{ex}")

        Button(formulario_boletos, text="Registrar Boletos", command=registrar_boletos).pack(pady=10)

    def pedir_cantidad_boletos():
        try:
            num_boletos = int(cantidad_boletos_deseada_entry.get().strip())
            if num_boletos > 0:
                mostrar_formulario_boletos(num_boletos)
                cantidad_boletos_dialog.destroy()
            else:
                messagebox.showerror("Error", "La cantidad de boletos debe ser mayor que cero.")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un número válido de boletos.")

    ventana_registro = Toplevel()
    ventana_registro.title("Registrar Venta (Vendedor)")
    ventana_registro.iconbitmap("codigos/assets/BDICON.ico")

    Label(ventana_registro, text="Factura Temporal ID:").grid(row=0, column=0, padx=5, pady=5)
    factura_temporal_entry = Entry(ventana_registro)
    factura_temporal_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(ventana_registro, text="Cliente ID:").grid(row=1, column=0, padx=5, pady=5)
    cliente_id_entry = Entry(ventana_registro)
    cliente_id_entry.grid(row=1, column=1, padx=5, pady=5)

    # Preguntar la cantidad de boletos
    cantidad_boletos_dialog = Toplevel(ventana_registro)
    cantidad_boletos_dialog.title("Cantidad de Boletos")
    Label(cantidad_boletos_dialog, text="¿Cuántos boletos desea registrar?").pack(padx=10, pady=10)
    cantidad_boletos_deseada_entry = Entry(cantidad_boletos_dialog)
    cantidad_boletos_deseada_entry.pack(padx=10, pady=5)
    Button(cantidad_boletos_dialog, text="Continuar", command=pedir_cantidad_boletos).pack(pady=10)

    Label(ventana_registro, text="--- Factura ---").grid(row=2, column=0, columnspan=2, pady=5)
    Label(ventana_registro, text="NIT:").grid(row=3, column=0, padx=5, pady=5)
    nit_entry = Entry(ventana_registro)
    nit_entry.grid(row=3, column=1, padx=5, pady=5)
    # Ya no preguntamos la cantidad de boletos aquí, se calculará dinámicamente
    Label(ventana_registro, text="Total:").grid(row=4, column=0, padx=5, pady=5)
    total_entry = Entry(ventana_registro)
    total_entry.grid(row=4, column=1, padx=5, pady=5)

    # El botón de registrar venta ahora está en el formulario de boletos
