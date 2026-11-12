import tkinter as tk

from vuelos import registrar_vuelo, buscar_vuelo, editar_vuelo
from tkinter import messagebox
from tkinter import ttk
from datos import vuelos

ventana = tk.Tk()

import random#Eso es de prueba para que el proceso sea mas rapido y no llenar todo manual jaja

ventana.title("AEROPORT CONTROL")
ventana.geometry("1200x700")
ventana.configure(bg="#0B1728")

# Crear menú lateral
menu = tk.Frame(ventana, bg="#14263D", width=225)
menu.pack(side="left", fill="y")
menu.pack_propagate(False)

# Título del menú
titulo = tk.Label(
    menu,
    text="✈ AEROPORT CONTROL",
    bg="#14263D",
    fg="white",
    font=("Arial", 16, "bold")
)
titulo.pack(pady=40)

# Opciones del menú
opciones = [
    "Dashboard",
    "Vuelos",
    "Pasajeros",
    "Reservas",
    "Boletos",
    "Reportes"
]
#Cambio de pantalla 

def mostrar_pantalla(nombre):
    # Borrar el contenido anterior
    for widget in contenido.winfo_children():
        widget.destroy()



    # Mostrar el título
    titulo = tk.Label(
        contenido,
        text=nombre,
        bg="#0B1728",
        fg="white",
        font=("Arial", 24, "bold")
    )
    titulo.pack(pady=30)

# Mostrar formulario únicamente en Vuelos
    if nombre == "Vuelos":
        entradas = {}
        campos = [
            "Origen",
            "Destino",
            "Fecha",
            "Hora",
            "Capacidad"
        ]

        for campo in campos:
            etiqueta = tk.Label(
                contenido,
                text=campo,
                bg="#0B1728",
                fg="white",
                font=("Arial", 12)
            )
            etiqueta.pack(pady=(10, 2))

            entrada = tk.Entry(
                contenido,
                font=("Arial", 12),
                width=35
            )
            entrada.pack(pady=5)
            entradas[campo] = entrada
        
        # Generar datos aleatorios para pruebas
        def generar_datos():

            ciudades = [
                "San José",
                "Panamá",
                "Bogotá",
                "Ciudad de México",
                "Miami",
                "Madrid",
                "Nueva York",
                "Lima"
                "Vice City"
                "Leonida"
                "Liberty City"
                "Los Santos"
                "San Fierro"

            ]

            origen, destino = random.sample(ciudades, 2)

            dia = random.randint(1, 28)
            mes = random.randint(1, 12)
            fecha = f"{dia:02d}-{mes:02d}-2027"

            hora = random.randint(0, 23)
            minuto = random.choice([0, 15, 30, 45])
            hora_vuelo = f"{hora:02d}:{minuto:02d}"

            capacidad = random.randint(0, 900)

            datos = {
                "Origen": origen,
                "Destino": destino,
                "Fecha": fecha,
                "Hora": hora_vuelo,
                "Capacidad": capacidad
            }

            for campo, valor in datos.items():
                entradas[campo].delete(0, tk.END)    
                entradas[campo].insert(0, str(valor))
            #Esas dos limpian el campo de entrada desde el inicio hasta el final e inserta el nuevo valor
            

        # Botón de datos aleatorios
        boton_aleatorio = tk.Button(
            contenido,
            text="🎲 Generar datos aleatorios",
            bg="#7C3AED",
            fg="white",
            font=("Arial", 11, "bold"),
            command=generar_datos
        )
        boton_aleatorio.pack(pady=10)


        def guardar_vuelo():
                    origen = entradas["Origen"].get()
                    destino = entradas["Destino"].get()
                    fecha = entradas["Fecha"].get()
                    hora = entradas["Hora"].get()
                    capacidad = entradas["Capacidad"].get()
                    resultado = registrar_vuelo(
                        origen, destino, fecha, hora, capacidad
                    )
                    if resultado.startswith("Error"):
                        messagebox.showerror("Error", resultado)
                    else:
                        messagebox.showinfo("AEROPORT CONTROL", resultado)
                        mostrar_pantalla("Vuelos")

        boton_guardar = tk.Button(
            contenido,
            text="Guardar Vuelo",
            bg="#00BFFF",
            fg="white",
            font=("Arial", 12, "bold"),
            command=guardar_vuelo
        )
        boton_guardar.pack(pady=25)
        #Buscador de vuelos
        etiqueta_buscar = tk.Label(
            contenido,
            text="Buscar vuelo por código",
            bg="#0B1728",
            fg="white",
            font=("Arial", 12)
        )
        etiqueta_buscar.pack(pady=5)

        entrada_buscar = tk.Entry(
            contenido,
            font=("Arial", 12),
            width=25
        )
        entrada_buscar.pack(pady=5)
        # Función para buscar vuelos
        def realizar_busqueda():
            codigo = entrada_buscar.get()
            vuelo = buscar_vuelo(codigo)
            if vuelo is None:
                messagebox.showerror(
                    "Vuelo no encontrado",
                    "No existe un vuelo con ese código."
                )
            else:
                mensaje = (
                    f"Código: {vuelo['codigo']}\n"
                    f"Origen: {vuelo['origen']}\n"
                    f"Destino: {vuelo['destino']}\n"
                    f"Fecha: {vuelo['fecha']}\n"
                    f"Hora: {vuelo['hora']}\n"
                    f"Capacidad: {vuelo['capacidad']}"
                )
                messagebox.showinfo(
                    "Información del vuelo",
                    mensaje
                )
        # Botón para buscar
        boton_buscar = tk.Button(
            contenido,
            text="Buscar vuelo",
            bg="#00BFFF",
            fg="white",
            font=("Arial", 12, "bold"),
            command=realizar_busqueda
        )
        boton_buscar.pack(pady=10)
        # Vuelos registrados
        columnas = ("Codigo", "Origen", "Destino", "Fecha", "Hora", "Capacidad")

        tabla_vuelos = ttk.Treeview(
            contenido,
            columns=columnas,
            show="headings",
            height=6
        )

        # Configurar columnas
        for columna in columnas:
            tabla_vuelos.heading(columna, text=columna)
            tabla_vuelos.column(columna, width=130, anchor="center")

        tabla_vuelos.pack(pady=15, padx=20, fill="x")

        # Mostrar los vuelos registrados
        for vuelo in vuelos:
            tabla_vuelos.insert(
                "",
                "end",
                values=(
                    vuelo["codigo"],
                    vuelo["origen"],
                    vuelo["destino"],
                    vuelo["fecha"],
                    vuelo["hora"],
                    vuelo["capacidad"]
                )
            )

        

# Crear botones
for opcion in opciones:
    boton = tk.Button(
        menu,
        text=opcion,
        bg="#14263D",
        fg="white",
        font=("Arial", 12),
        relief="flat",
        anchor="w",
        padx=20,
        command=lambda nombre=opcion: mostrar_pantalla(nombre)
    )
    boton.pack(fill="x", pady=5)

# Área principal
contenido = tk.Frame(ventana, bg="#0B1728")
contenido.pack(side="right", fill="both", expand=True)

# Mostrar pantalla inicial
mostrar_pantalla("Dashboard")

# Mantener la ventana abierta
ventana.mainloop()