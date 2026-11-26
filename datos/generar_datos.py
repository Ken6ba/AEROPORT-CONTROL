"Genera datos de demostración claramente simulados para SJO."

from datetime import date, timedelta
import random
from database import conectar, crear_tablas


def generar_datos():
    crear_tablas()
    conexion = conectar()
    # Si ya hay vuelos, no vuelvo a insertar los datos cada vez que inicio.
    total = conexion.execute("SELECT COUNT(*) AS total FROM vuelos").fetchone()["total"]
    if total > 0:
        conexion.close()
        return

    # La semilla hace que los datos simulados sean repetibles.
    random.seed(10)
    nombres = [
        ("Ana López", "CR-1001", "Costa Rica", "ana@gmail.com"),
        ("Carlos Méndez", "GT-1002", "Guatemala", "carlos@gmail.com"),
        ("María Solís", "NI-1003", "Nicaragua", "maria@gmail.com"),
        ("Diego Herrera", "PA-1004", "Panamá", "diego@gmail.com"),
        ("Laura Vargas", "SV-1005", "El Salvador", "laura@gmail.com"),
        ("José Ramírez", "HN-1006", "Honduras", "jose@gmail.com"),
    ]
    for pasajero in nombres:
        conexion.execute(
            "INSERT INTO pasajeros (nombre, documento, nacionalidad, correo) VALUES (?, ?, ?, ?)",
            pasajero,
        )

    destinos = [("GUA", "Ciudad de Guatemala"), ("PTY", "Ciudad de Panamá"), ("MEX", "Ciudad de México"), ("MIA", "Miami")]
    estados = ["Programado", "A tiempo", "Completado"]
    inicio = date(2026, 11, 1)
    # Uso un for porque conozco la cantidad exacta de 60 vuelos.
    for numero in range(60):
        dia = inicio + timedelta(days=numero)
        codigo_destino, destino = destinos[numero % len(destinos)]
        codigo = "AV" + str(100 + numero)
        hora = str(6 + (numero % 12)).zfill(2) + ":30"
        estado = estados[numero % len(estados)]
        conexion.execute(
            """INSERT INTO vuelos (codigo, origen, destino, fecha, hora, estado, capacidad)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (codigo, "SJO", destino, dia.isoformat(), hora, estado, 180),
        )

    vuelos = conexion.execute("SELECT id FROM vuelos LIMIT 6").fetchall()
    pasajeros = conexion.execute("SELECT id FROM pasajeros").fetchall()
    for posicion in range(6):
        conexion.execute(
            "INSERT INTO reservas (pasajero_id, vuelo_id, fecha_reserva, estado) VALUES (?, ?, ?, ?)",
            (pasajeros[posicion]["id"], vuelos[posicion]["id"], "2026-10-25", "Confirmada"),
        )
    reservas = conexion.execute("SELECT id FROM reservas").fetchall()
    for posicion, reserva in enumerate(reservas):
        conexion.execute(
            "INSERT INTO boletos (reserva_id, asiento, precio, fecha_emision) VALUES (?, ?, ?, ?)",
            (reserva["id"], str(10 + posicion) + "A", 145.00 + posicion * 20, "2026-10-25"),
        )
    conexion.commit()
    conexion.close()

