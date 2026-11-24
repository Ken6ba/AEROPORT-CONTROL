from nicegui import ui
from funciones import crear_reserva, listar_reservas, opciones_pasajeros, opciones_vuelos
from paginas.comun import marco


@ui.page("/reservas")
def reservas():
    marco("Reservas", "Crea una reserva seleccionando un pasajero y un vuelo")
    pasajero = ui.select(opciones_pasajeros(), label="Pasajero").classes("w-80")
    vuelo = ui.select(opciones_vuelos(), label="Vuelo").classes("w-80")
    mensaje = ui.label().classes("text-green-700")
    tabla = ui.table(columns=[
        {"name": "nombre", "label": "Pasajero", "field": "nombre"},
        {"name": "codigo", "label": "Vuelo", "field": "codigo"},
        {"name": "destino", "label": "Destino", "field": "destino"},
        {"name": "fecha", "label": "Fecha", "field": "fecha"},
        {"name": "estado", "label": "Estado", "field": "estado"},
    ], rows=listar_reservas()).classes("w-full mt-4")
# Función anidada (def dentro de otro def): se define aquí dentro para que tenga acceso
    # directo a los componentes de esta página (pasajero, vuelo, mensaje y tabla) sin tener
    # que pasarlos como parámetros, y porque esta acción solo pertenece a la vista /reservas.
    def guardar():
        if pasajero.value and vuelo.value:
            correcto, texto = crear_reserva(int(pasajero.value), int(vuelo.value))
            mensaje.text = texto
            if correcto:
                tabla.update_rows(listar_reservas())
        else:
            mensaje.text = "Selecciona un pasajero y un vuelo."

    ui.button("Guardar reserva", on_click=guardar).classes("bg-blue-700 text-white")

