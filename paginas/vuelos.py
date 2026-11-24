from nicegui import ui
from funciones import listar_vuelos
from paginas.comun import marco


@ui.page("/vuelos")
def vuelos():
    marco("Vuelos", "Programación de vuelos desde el aeropuerto SJO")
    buscador = ui.input("Buscar por código, origen o destino").classes("w-96")
    tabla = ui.table(columns=[
        {"name": "codigo", "label": "Código", "field": "codigo"},
        {"name": "origen", "label": "Origen", "field": "origen"},
        {"name": "destino", "label": "Destino", "field": "destino"},
        {"name": "fecha", "label": "Fecha", "field": "fecha"},
        {"name": "hora", "label": "Hora", "field": "hora"},
        {"name": "estado", "label": "Estado", "field": "estado"},
    ], rows=listar_vuelos()).classes("w-full mt-4")
    buscador.on("update:model-value", lambda: tabla.update_rows(listar_vuelos(buscador.value or "")))

