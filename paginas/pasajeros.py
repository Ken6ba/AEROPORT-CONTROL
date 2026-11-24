from nicegui import ui
from funciones import (
    actualizar_pasajero,
    crear_pasajero,
    eliminar_pasajero,
    listar_pasajeros,
    obtener_pasajero,
    obtener_prefijo,
    opciones_pasajeros,
)
from datos.paises import PAISES
from paginas.comun import marco


@ui.page("/pasajeros")
def pasajeros():
    marco("Pasajeros", "Registro y administración de personas")

    selector = ui.select(
        opciones_pasajeros(),
        label="Pasajero para editar o eliminar",
    ).classes("w-96")

    nombre = ui.input("Nombre completo").classes("w-96")
    documento = ui.input(
        "Número del documento",
        placeholder="Ejemplo: 123456",
    ).classes("w-96")

    letras = sorted(set(pais[0].upper() for pais in PAISES))
    letra = ui.select(letras, label="Primera letra del país").classes("w-96")
    nacionalidad = ui.select([], label="Nacionalidad").classes("w-96")

    correo = ui.input(
        "Usuario de Gmail",
        placeholder="Ejemplo: juan12",
    ).classes("w-96")

    mensaje = ui.label().classes("text-blue-300")

    def actualizar_lista_paises(valor_letra):
        if not valor_letra:
            nacionalidad.options = []
            nacionalidad.value = None
            nacionalidad.update()
            return

        nacionalidad.options = [
            pais for pais in PAISES if pais.startswith(valor_letra)
        ]
        nacionalidad.update()

    def cambiar_letra(evento):
        actualizar_lista_paises(evento.value)
        nacionalidad.value = None
        nacionalidad.update()

    def colocar_prefijo(evento):
        prefijo = obtener_prefijo(evento.value)
        documento.value = prefijo + "-" if prefijo else ""

    def completar_correo(evento):
        texto = (evento.value or "").strip().lower()
        if texto and "@" not in texto:
            correo.value = texto + "@gmail.com"

    letra.on_value_change(cambiar_letra)
    nacionalidad.on_value_change(colocar_prefijo)
    correo.on("blur", completar_correo)

    tabla = ui.table(
        columns=[
            {"name": "nombre", "label": "Nombre", "field": "nombre"},
            {"name": "documento", "label": "Documento", "field": "documento"},
            {"name": "nacionalidad", "label": "Nacionalidad", "field": "nacionalidad"},
            {"name": "correo", "label": "Correo", "field": "correo"},
        ],
        rows=listar_pasajeros(),
    ).classes("w-full mt-4")

    def refrescar():
        tabla.update_rows(listar_pasajeros())
        selector.options = opciones_pasajeros()
        selector.update()

    def limpiar_formulario():
        nombre.value = ""
        documento.value = ""
        letra.value = None
        letra.update()
        nacionalidad.options = []
        nacionalidad.value = None
        nacionalidad.update()
        correo.value = ""

    def cargar_pasajero(evento):
        if not evento.value:
            limpiar_formulario()
            return

        pasajero = obtener_pasajero(int(evento.value))
        if not pasajero:
            return

        nombre.value = pasajero["nombre"]
        correo.value = pasajero["correo"]

        pais = pasajero["nacionalidad"]
        letra.value = pais[0].upper()
        letra.update()
        actualizar_lista_paises(letra.value)
        nacionalidad.value = pais
        nacionalidad.update()
        documento.value = pasajero["documento"]

    def guardar():
        correcto, texto = crear_pasajero(
            nombre.value,
            documento.value,
            nacionalidad.value,
            correo.value,
        )
        mensaje.text = texto
        if correcto:
            refrescar()
            limpiar_formulario()

    def editar():
        if not selector.value:
            mensaje.text = "Selecciona un pasajero para editar."
            return

        correcto, texto = actualizar_pasajero(
            int(selector.value),
            nombre.value,
            documento.value,
            nacionalidad.value,
            correo.value,
        )
        mensaje.text = texto
        if correcto:
            refrescar()

    def borrar():
        if not selector.value:
            mensaje.text = "Selecciona un pasajero para eliminar."
            return

        correcto, texto = eliminar_pasajero(int(selector.value))
        mensaje.text = texto
        if correcto:
            selector.value = None
            limpiar_formulario()
            refrescar()

    selector.on_value_change(cargar_pasajero)

    with ui.row().classes("gap-3 mt-4"):
        ui.button("Guardar pasajero", on_click=guardar).classes("bg-blue-700 text-white")
        ui.button("Editar pasajero", on_click=editar).classes("bg-orange-700 text-white")
        ui.button("Eliminar pasajero", on_click=borrar).classes("bg-red-700 text-white")
