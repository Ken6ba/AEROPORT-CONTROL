from nicegui import ui
from database import conectar
from paginas.comun import marco


@ui.page("/reportes")
def reportes():
    marco("Reportes", "Consultas simples para revisar la operación")
    conexion = conectar()
    destinos = conexion.execute("SELECT destino, COUNT(*) AS total FROM vuelos GROUP BY destino ORDER BY total DESC").fetchall()
    conexion.close()
    ui.label("Vuelos por destino").classes("text-xl font-bold mt-6")
    ui.table(columns=[
        {"name": "destino", "label": "Destino", "field": "destino"},
        {"name": "total", "label": "Cantidad de vuelos", "field": "total"},
    ], rows=[dict(fila) for fila in destinos]).classes("w-96 mt-2")
            #dict convierte cada fila de la base de datos a un diccionario estándar para que ui.table pueda leerlo
