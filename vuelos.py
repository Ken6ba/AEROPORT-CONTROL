from datos import vuelos
from datetime import datetime

def registrar_vuelo(origen, destino, fecha, hora, capacidad):
    # Verificar que los datos no esten vacíos
    if not origen.strip() or not destino.strip():
        return "Error: origen y destino son obligatorios."

    # Validar la capacidad
    try:
        capacidad = int(capacidad)
    except ValueError:
        return "Error: la capacidad debe ser un número entero."

    if capacidad <= 0:
        return "Error: la capacidad debe ser mayor que cero."
    
    # Generar código único para cada vuelo
    codigo = f"AC{len(vuelos) + 1:03d}"
        # Validar fecha
    try:
        datetime.strptime(fecha, "%d-%m-%Y")
    except ValueError:
        return "Error: la fecha debe tener el formato DD-MM-YYYY."

    # Validar hora
    try:
        datetime.strptime(hora, "%H:%M")
    except ValueError:
        return "Error: la hora debe tener el formato HH:MM."
    # Crear un diccionario con los datos
    vuelo = {
        "codigo": codigo,
        "origen": origen.strip(),#Strip Elimina los espacios en blanco sobrantes al principio y al final de un texto
        "destino": destino.strip(),
        "fecha": fecha,
        "hora": hora,
        "capacidad": capacidad
    }
    # Guardar el vuelo en la lista
    vuelos.append(vuelo)
    return "Vuelo registrado exitosamente."

def buscar_vuelo(codigo):
    for vuelo in vuelos:
        if vuelo["codigo"] == codigo.strip().upper():#Strip Elimina los espacios en blanco sobrantes al principio y al final de un texto
            return vuelo                             #Upper Hace lo contrario que lower osea todo lo vuelve todas las letras a mayusculas.

#Esto es para editar el vuelo osea el destino al que se dirige
def editar_vuelo(codigo, nuevo_destino):
    vuelo = buscar_vuelo(codigo)

    if vuelo is None:
        return "Error: vuelo no encontrado."

    if not nuevo_destino.strip():
        return "Error: el destino no puede estar vacío."

    if nuevo_destino.strip().lower() == vuelo["origen"].lower():#Strip Elimina los espacios en blanco sobrantes al principio y al final de un texto
        return "Error: el destino no puede ser igual al origen."#Lower Convierte todas las letras del texto a minúsculas.

    vuelo["destino"] = nuevo_destino.strip()

    return "Vuelo actualizado exitosamente."

    return None