import random
from datetime import date
import numpy as np
from Empresa import Empresa

# Semilla fija: cada vez que se corre, sale el mismo dataset
rng = np.random.default_rng(42)
random.seed(42)

# 1. Cargar lo que ya existe en los CSV (admins, profesionales, equipos, procedimientos)
empresa = Empresa("QuantumTech Precision")
empresa.cargar_estado_total()
admin = empresa.getter_administradores()[0]
equipos = empresa.getter_equipos()
procedimientos = empresa.getter_procedimientos()

# 2. Contratar 40 profesionales más (quedan 50 en total)
nombres_nuevos = [
    "Lucia Moreno", "Diego Acosta", "Julieta Paz", "Andres Molina", "Carolina Suarez",
    "Bruno Castillo", "Agustina Ramos", "Facundo Ibarra", "Micaela Rojas", "Santiago Luna",
    "Florencia Vidal", "Gonzalo Peralta", "Rocio Navarro", "Matias Ferreyra", "Antonella Sosa",
    "Joaquin Aguirre", "Milagros Cabrera", "Lautaro Godoy", "Delfina Ponce", "Emiliano Quiroga",
    "Brenda Villalba", "Franco Ledesma", "Abril Correa", "Ignacio Figueroa", "Martina Rivero",
    "Leandro Ojeda", "Candela Mendez", "Ezequiel Rios", "Victoria Luna", "Maximiliano Vera",
    "Celeste Arias", "Federico Paez", "Josefina Blanco", "Gaston Ruiz", "Pilar Dominguez",
    "Nahuel Campos", "Morena Salinas", "Hernan Bustos", "Daniela Olmos", "Cristian Lopez"
]
certificaciones_posibles = [["Metrologia dimensional"], ["Inspeccion visual"],
                            ["Metrologia dimensional", "Inspeccion visual"]]

for nombre in nombres_nuevos:
    profesional = admin.crear_profesional(nombre)
    for certificacion in certificaciones_posibles[int(rng.integers(0, 3))]:
        profesional.agregar_certificacion(certificacion, date(2026, 1, 1), date(2027, 12, 31))

profesionales = empresa.getter_profesionales()

# 3. Para cada procedimiento: qué profesionales y equipos pueden usarse (se calcula una sola vez)
habilitados = {proc.getter_id(): list(filter(lambda p: not p.certificaciones_faltantes(proc.getter_certificaciones_requeridas(), date.today()), profesionales))
               for proc in procedimientos}
compatibles = {proc.getter_id(): list(filter(lambda e: e.getter_categoria() == proc.getter_categoria_equipo(), equipos))
               for proc in procedimientos}

# 4. Crear 100 lotes, cada uno con 5 a 20 muestras
for _ in range(100):
    lote = admin.crear_lote(int(rng.integers(500, 2001)))

    for _ in range(int(rng.integers(5, 21))):
        procedimiento = rng.choice(procedimientos)
        admin.crear_muestra(lote.getter_id(), int(rng.integers(8, 16)),
                            rng.choice(habilitados[procedimiento.getter_id()]).getter_id(),
                            rng.choice(compatibles[procedimiento.getter_id()]).getter_id(),
                            procedimiento.getter_id())

# 5. Los profesionales ejecutan sus inspecciones y el admin evalúa los lotes
for profesional in profesionales:
    while not profesional.getter_cola_vacia():
        profesional.ejecutar_siguiente_inspeccion()

for lote in empresa.getter_lotes():
    admin.evaluar_lote(lote.getter_id())

# 6. Guardar todo en los CSV
empresa.guardar_estado_total()
print("Listo:", len(empresa.getter_profesionales()), "profesionales y", len(empresa.getter_lotes()), "lotes")