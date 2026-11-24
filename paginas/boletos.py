from nicegui import ui
from funciones import listar_boletos
from paginas.comun import marco


@ui.page("/boletos")
def boletos():
    marco("Boletos", "Boletos emitidos para reservas confirmadas")
#Diccionarios
    ui.table(columns=[
        {"name": "nombre", "label": "Pasajero", "field": "nombre"},
        {"name": "codigo", "label": "Vuelo", "field": "codigo"},
        #Busca el código del vuelo.
        {"name": "asiento", "label": "Asiento", "field": "asiento"},
        #Busca el asiento.
        {"name": "precio", "label": "Precio", "field": "precio"},
        #Busca el precio.
        {"name": "fecha_emision", "label": "Emitido", "field": "fecha_emision"},
        #Busca la fecha en que se emitió el boleto.
    ], rows=listar_boletos()).classes("w-full mt-4")
    #La w viene de width, que significa ancho. Y mt-4: margin-top

