#Las páginas muestran información.
#funciones.py obtiene o modifica información.
#database.py conecta con SQLite.
#Funicones es como un puente ej:pantalla → función → base de datos
"Operaciones principales del proyecto, escritas con funciones simples."

from datetime import date
from database import conectar
from datos.paises import PAISES

def listar_vuelos(busqueda=""):
    conexion = conectar()
    # Los signos % permiten buscar una palabra aunque esté en medio del texto.
    texto = "%" + busqueda.strip() + "%"
    filas = conexion.execute(
        """SELECT * FROM vuelos
           WHERE codigo LIKE ? OR origen LIKE ? OR destino LIKE ?
           ORDER BY fecha, hora""",
        (texto, texto, texto),
    ).fetchall()
    conexion.close()
    # Convierto cada fila en diccionario para que NiceGUI pueda mostrarla.
    return [dict(fila) for fila in filas]

def listar_pasajeros():
    conexion = conectar()
    filas = conexion.execute("SELECT * FROM pasajeros ORDER BY nombre").fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]

def listar_reservas():
    conexion = conectar()
    filas = conexion.execute(
        """SELECT reservas.id, pasajeros.nombre, vuelos.codigo,
                  vuelos.origen, vuelos.destino, vuelos.fecha,
                  reservas.estado
           FROM reservas
           -- JOIN combina la reserva con el pasajero y el vuelo relacionados.
           JOIN pasajeros ON pasajeros.id = reservas.pasajero_id
           JOIN vuelos ON vuelos.id = reservas.vuelo_id
           ORDER BY vuelos.fecha"""
    ).fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]

def listar_boletos():
    conexion = conectar()
    filas = conexion.execute(
        """SELECT boletos.id, pasajeros.nombre, vuelos.codigo,
                  boletos.asiento, boletos.precio, boletos.fecha_emision
           FROM boletos
           JOIN reservas ON reservas.id = boletos.reserva_id
           JOIN pasajeros ON pasajeros.id = reservas.pasajero_id
           JOIN vuelos ON vuelos.id = reservas.vuelo_id
           ORDER BY boletos.id DESC"""
    ).fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]

def crear_reserva(pasajero_id, vuelo_id):
    "Guarda una reserva y devuelve un mensaje que la pantalla puede mostrar."
    conexion = conectar()
    try:
        # Uso ? para enviar valores de forma segura a SQLite.
        conexion.execute(
            "INSERT INTO reservas (pasajero_id, vuelo_id, fecha_reserva, estado) VALUES (?, ?, ?, ?)",
            (pasajero_id, vuelo_id, date.today().isoformat(), "Confirmada"),
        )
        conexion.commit()
        return True, "Reserva creada correctamente."
    except Exception:
        return False, "No se pudo crear: el pasajero quizá ya tiene esa reserva."
    finally:
        # Cierro la conexión aunque ocurra un error.
        conexion.close()

def crear_pasajero(nombre, documento, nacionalidad, correo):
    "Valida y guarda un pasajero nuevo en la base de datos."
    nombre = (nombre or "").strip()
    documento = (documento or "").strip().upper()
    nacionalidad = (nacionalidad or "").strip()
    correo = (correo or "").strip().lower()

    prefijo = obtener_prefijo(nacionalidad)

    if nombre == "" or documento == "" or nacionalidad == "" or correo == "":
        return False, "Completa todos los campos."

    if len(nombre) < 3:
        return False, "El nombre es demasiado corto."

    # El nombre puede tener letras y espacios, pero no números.
    nombre_sin_espacios = nombre.replace(" ", "")
    if not nombre_sin_espacios.isalpha():
        return False, "El nombre solo puede contener letras y espacios."

    if prefijo == "":
        return False, "Selecciona un país válido de la lista."

    # Permite escribir solamente números o el documento con su prefijo.
    documento = documento.replace(prefijo + "-", "")

    if not documento.isdigit():
        return False, "El documento debe contener solamente números."

    documento = prefijo + "-" + documento

    # Si la persona escribe solamente el usuario, completamos Gmail.
    if "@" not in correo:
        correo = correo + "@gmail.com"

    if correo.count("@") != 1 or not correo.endswith("@gmail.com"):
        return False, "El correo debe terminar en @gmail.com."

    usuario_correo = correo.split("@")[0]
    if usuario_correo == "" or " " in usuario_correo:
        return False, "Escribe correctamente el usuario del correo."

    conexion = conectar()

    try:
        conexion.execute(
            """INSERT INTO pasajeros
               (nombre, documento, nacionalidad, correo)
               VALUES (?, ?, ?, ?)""",
            (nombre, documento, nacionalidad, correo),
        )

        conexion.commit()
        return True, "Pasajero registrado correctamente."

    except Exception:
        return False, "No se pudo registrar. El documento quizá ya existe."

    finally:
        # La conexión siempre se cierra para no dejar recursos abiertos.
        conexion.close()


def obtener_pasajero(id_pasajero):
    "Busca un pasajero por su número de identificación."
    conexion = conectar()
    fila = conexion.execute(
        "SELECT * FROM pasajeros WHERE id = ?", (id_pasajero,)
    ).fetchone()
    conexion.close()

    if fila:
        return dict(fila)
    return None


def actualizar_pasajero(id_pasajero, nombre, documento, nacionalidad, correo):
    "Actualiza los datos de un pasajero existente."
    nombre = (nombre or "").strip()
    documento = (documento or "").strip().upper()
    nacionalidad = (nacionalidad or "").strip()
    correo = (correo or "").strip().lower()
    prefijo = obtener_prefijo(nacionalidad)

    if nombre == "" or documento == "" or nacionalidad == "" or correo == "":
        return False, "Completa todos los campos."

    if len(nombre) < 3 or not nombre.replace(" ", "").isalpha():
        return False, "El nombre solo puede contener letras y espacios."

    if prefijo == "":
        return False, "Selecciona un país válido de la lista."

    documento = documento.replace(prefijo + "-", "")
    if not documento.isdigit():
        return False, "El documento debe contener solamente números."
    documento = prefijo + "-" + documento

    if "@" not in correo:
        correo = correo + "@gmail.com"
    if correo.count("@") != 1 or not correo.endswith("@gmail.com"):
        return False, "El correo debe terminar en @gmail.com."

    conexion = conectar()
    try:
        conexion.execute(
            """UPDATE pasajeros
               SET nombre = ?, documento = ?, nacionalidad = ?, correo = ?
               WHERE id = ?""",
            (nombre, documento, nacionalidad, correo, id_pasajero),
        )
        conexion.commit()
        return True, "Pasajero actualizado correctamente."
    except Exception:
        return False, "No se pudo actualizar. El documento quizá ya existe."
    finally:
        conexion.close()


def eliminar_pasajero(id_pasajero):
    "Elimina un pasajero y sus reservas relacionadas."
    conexion = conectar()
    try:
        conexion.execute(
            """DELETE FROM boletos
               WHERE reserva_id IN
               (SELECT id FROM reservas WHERE pasajero_id = ?)""",
            (id_pasajero,),
        )
        conexion.execute(
            "DELETE FROM reservas WHERE pasajero_id = ?", (id_pasajero,)
        )
        resultado = conexion.execute(
            "DELETE FROM pasajeros WHERE id = ?", (id_pasajero,)
        )
        conexion.commit()

        if resultado.rowcount == 0:
            return False, "No se encontró el pasajero."
        return True, "Pasajero eliminado correctamente."
    except Exception:
        conexion.rollback()
        return False, "No se pudo eliminar el pasajero."
    finally:
        conexion.close()


def obtener_prefijo(nacionalidad):
    "Devuelve el prefijo del documento según la nacionalidad."
    nacionalidad = (nacionalidad or "").strip().lower()

    # Recorro el diccionario para aceptar el nombre del país o su código.
    for pais, prefijo in PAISES.items():
        if pais.lower() == nacionalidad or prefijo.lower() == nacionalidad:
            return prefijo

    return ""
        
def opciones_pasajeros():
    return {str(p["id"]): p["nombre"] for p in listar_pasajeros()}

def opciones_vuelos():
    vuelos = listar_vuelos()
    return {str(v["id"]): v["codigo"] + " - " + v["destino"] for v in vuelos}
