import sqlite3
from pathlib import Path


RUTA_BASE = Path(__file__).parent / "aeroport.db"


def conectar():
    "Abre la base de datos y permite acceder a las columnas por nombre."
    conexion = sqlite3.connect(RUTA_BASE)
    # Así puedo usar fila["nombre"] en vez de recordar posiciones numéricas.
    conexion.row_factory = sqlite3.Row
    # Activo las relaciones entre tablas para proteger reservas y boletos.
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_tablas():
    "Crea las tablas si todavía no existen."
    conexion = conectar()
    conexion.executescript(
        """
        CREATE TABLE IF NOT EXISTS vuelos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            origen TEXT NOT NULL,
            destino TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            estado TEXT NOT NULL,
            capacidad INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pasajeros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT NOT NULL UNIQUE,
            nacionalidad TEXT NOT NULL,
            correo TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pasajero_id INTEGER NOT NULL,
            vuelo_id INTEGER NOT NULL,
            fecha_reserva TEXT NOT NULL,
            estado TEXT NOT NULL,
            -- Evita que un pasajero reserve dos veces el mismo vuelo.
            UNIQUE(pasajero_id, vuelo_id),
            FOREIGN KEY (pasajero_id) REFERENCES pasajeros(id),
            FOREIGN KEY (vuelo_id) REFERENCES vuelos(id)
        );

        CREATE TABLE IF NOT EXISTS boletos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reserva_id INTEGER NOT NULL UNIQUE,
            asiento TEXT NOT NULL,
            precio REAL NOT NULL,
            fecha_emision TEXT NOT NULL,
            FOREIGN KEY (reserva_id) REFERENCES reservas(id)
        );
        """
    )
    conexion.commit()
    conexion.close()


def contar(tabla):
    "Devuelve cuántos registros existen en una tabla conocida."
    tablas_permitidas = ["vuelos", "pasajeros", "reservas", "boletos"]
    if tabla not in tablas_permitidas:
        return 0
    # Solo permito nombres de tablas conocidos antes de formar la consulta.
    conexion = conectar()
    resultado = conexion.execute("SELECT COUNT(*) AS total FROM " + tabla).fetchone()
    conexion.close()
    return resultado["total"]

