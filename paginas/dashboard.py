from nicegui import ui
from database import contar
from paginas.comun import marco


@ui.page("/")
def dashboard():
    marco("Centro de operaciones", "Resumen del aeropuerto simulado SJO")
    with ui.row().classes("w-full gap-4 mt-6"):
        #ui.row(): Coloca los elementos en una fila horizontal. gap-4: Deja espacio entre las tarjetas. mt-6:Deja espacio arriba de la fila
        for titulo, tabla, color in [("Vuelos", "vuelos", "blue"), ("Pasajeros", "pasajeros", "green"), ("Reservas", "reservas", "orange"), ("Boletos", "boletos", "purple")]:
            with ui.card().classes("w-56"):
                ui.label(titulo).classes("text-gray-600")
                ui.label(str(contar(tabla))).classes("text-4xl font-bold text-" + color + "-700")
                        #str Convierte el número a texto
        # Usamos for porque recorremos una lista conocida de cuatro tarjetas.
        # El ciclo se repite una vez por cada elemento de la lista.
        # Un while sería más largo porque tendríamos que controlar una posición manualmente.
    with ui.row().classes("w-full gap-4 mt-6 items-stretch"):
        with ui.card().classes("bg-slate-800 border border-slate-700 w-full"):
            ui.label("ESTADO OPERATIVO").classes("text-lg font-bold text-white")
            ui.label("Todos los datos son simulados para la presentación.").classes("text-slate-400")
            with ui.row().classes("gap-3 mt-4"):
                ui.badge("PROGRAMADO", color="blue")
                ui.badge("A TIEMPO", color="green")
                ui.badge("REVISIÓN", color="orange")

        with ui.card().classes("bg-slate-800 border border-slate-700 w-full"):
            ui.label("RUTAS PRINCIPALES").classes("text-lg font-bold text-white")
            ui.label("SJO → GUA   |   SJO → PTY   |   SJO → MEX   |   SJO → MIA").classes("text-blue-300 mt-3")

    with ui.card().classes("mt-6 w-full bg-slate-800 border border-slate-700"):
        ui.label("Nota del proyecto").classes("text-xl font-bold text-white")
        ui.label("Los datos son sintéticos y sirven para practicar el flujo de vuelos, pasajeros, reservas y boletos.").classes("text-slate-400")

