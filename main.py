"Punto de entrada de AEROPORT CONTROL."

from nicegui import ui
from database import crear_tablas
from datos.generar_datos import generar_datos

# Importar las páginas hace que NiceGUI registre sus rutas.
# Cada página tiene una dirección, por ejemplo /vuelos o /pasajeros.
import paginas.dashboard
import paginas.vuelos
import paginas.pasajeros
import paginas.reservas
import paginas.boletos
import paginas.reportes


# Primero preparo la base de datos y después cargo los datos simulados.
# Este orden evita intentar insertar datos antes de crear las tablas.
crear_tablas()
generar_datos()

ui.run(title="AEROPORT CONTROL", port=8080, reload=False)

