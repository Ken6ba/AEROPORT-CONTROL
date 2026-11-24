# AEROPORT CONTROL

Sistema sencillo para administrar información básica de un aeropuerto.

## ¿Qué hace?

- Muestra vuelos, pasajeros, reservas y boletos.
- Permite registrar pasajeros.
- Valida nombres, documentos, países y correos Gmail.
- Permite crear reservas.
- Muestra un dashboard y reportes básicos.
- Guarda la información en una base de datos SQLite.

## Tecnologías

- Python 3.12
- NiceGUI
- SQLite con la biblioteca `sqlite3`

## Instalación

Desde la carpeta principal del proyectoe jecutamos:

```powershell
python -m pip install -r requirements.txt
eso es para instalar las librerias que ocupa el programa
```

## Ejecución

```powershell
python main.py
```

Después abrir en el navegador:

```text
http://localhost:8080
```

## Carpetas principales

- `main.py`: inicia el programa.
- `database.py`: crea y conecta la base de datos.
- `funciones.py`: contiene las funciones que consultan o guardan información.
- `datos/`: contiene los países y los datos simulados.
- `paginas/`: contiene las pantallas del sistema.
- `aeroport.db`: base de datos SQLite.

Los datos del proyecto son simulados y se utilizan solamente con fines educativos.
