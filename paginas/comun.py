from nicegui import ui


def encabezado(titulo, subtitulo=""):
    ui.label(titulo).classes("text-3xl font-bold text-white")
    if subtitulo:
        ui.label(subtitulo).classes("text-slate-400")


def menu():  # Esto es la barra lateral.
    with ui.left_drawer(value=True).classes("bg-slate-950 border-r border-slate-800"):
    #El with indica que los elementos escritos debajo pertenecen al panel lateral.
        ui.label("✈ AEROPORT\nCONTROL").classes("text-2xl font-bold text-blue-400 whitespace-pre-line p-4")
        ui.label("CENTRO DE OPERACIONES").classes("text-xs text-slate-500 px-4")
        ui.link("⌂  Dashboard", "/").classes("text-slate-200 p-3 w-full hover:bg-slate-800")
        ui.link("✈  Vuelos", "/vuelos").classes("text-slate-200 p-3 w-full hover:bg-slate-800")
        ui.link("♙  Pasajeros", "/pasajeros").classes("text-slate-200 p-3 w-full hover:bg-slate-800")
        ui.link("▣  Reservas", "/reservas").classes("text-slate-200 p-3 w-full hover:bg-slate-800")
        ui.link("▤  Boletos", "/boletos").classes("text-slate-200 p-3 w-full hover:bg-slate-800")
        ui.link("▥  Reportes", "/reportes").classes("text-slate-200 p-3 w-full hover:bg-slate-800")


def marco(titulo, subtitulo=""):
    ui.dark_mode().enable()
    menu()
    with ui.header().classes("bg-slate-950 border-b border-slate-800 px-8"):
        ui.label("AEROPORT CONTROL").classes("text-xl font-bold text-white")
        ui.space()
        ui.label("SJO  |  DATOS SIMULADOS").classes("text-sm text-slate-400")
    with ui.column().classes("w-full bg-slate-900 p-8 gap-2"):
        encabezado(titulo, subtitulo)

