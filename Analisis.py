import numpy as np
import matplotlib.pyplot as plt
from GestorArchivos import GestorArchivos


# ==========================================
# OBTENER LOS DATOS
# ==========================================

def cargar(archivo):
    return GestorArchivos.leer_csv_dict(GestorArchivos.CARPETA_DATOS / archivo)

def columna(filas, nombre):
    return np.array(list(map(lambda fila: fila[nombre], filas)))


# ==========================================
# EJERCICIO 1: ANÁLISIS GENERAL DE CALIDAD
# ==========================================

def analisis_general():
    muestras = cargar("muestras.csv")
    lotes = cargar("lotes.csv")

    estados = columna(muestras, "estado")
    lote_de_muestra = columna(muestras, "lote_id")
    estados_lotes = columna(lotes, "estado")

    # ---------- Métricas ----------

    # Comparar un array con un valor compara cada elemento y devuelve True/False para cada uno
    inspeccionadas = estados != "PENDIENTE"
    no_conformes = estados == "NO_CONFORME"

    cantidad_inspeccionadas = np.sum(inspeccionadas)
    porcentaje_conformes = np.sum(estados == "CONFORME") / cantidad_inspeccionadas * 100
    porcentaje_no_conformes = np.sum(no_conformes) / cantidad_inspeccionadas * 100
    cantidad_reportes = np.sum(no_conformes)          # cada muestra No Conforme genera un reporte
    # np.mean (el promedio) de True/False es la proporción de True.
    tasa_rechazo_lotes = np.mean(estados_lotes == "RECHAZADO") * 100

    print("\n========== ANÁLISIS GENERAL DE CALIDAD ==========")
    print("Muestras inspeccionadas:", cantidad_inspeccionadas)
    print(f"Conformes: {porcentaje_conformes:.1f}%")
    print(f"No conformes: {porcentaje_no_conformes:.1f}%")
    print("Reportes generados:", cantidad_reportes)
    print(f"Tasa global de rechazo de lotes: {tasa_rechazo_lotes:.1f}% "
          f"({np.sum(estados_lotes == 'RECHAZADO')} de {len(lotes)} lotes)")

    # ---------- Conformidad por lote ----------
    ids_lotes = columna(lotes, "id")
    muestras_por_lote = np.array(list(map(lambda lote: np.sum(lote_de_muestra == lote), ids_lotes)))
    # mascara
    no_conformes_por_lote = np.array(list(map(lambda lote: np.sum(no_conformes[lote_de_muestra == lote]), ids_lotes)))
    conformes_por_lote = muestras_por_lote - no_conformes_por_lote
    porcentaje_nc_por_lote = no_conformes_por_lote / muestras_por_lote * 100

    # Lotes problemáticos: los de mayor porcentaje de muestras No Conformes
    # np.argsort(...) devuelve las POSICIONES ordenadas de menor a mayor valor
    # [::-1] da vuelta la lista: de mayor a menor
    # [:5] se queda con los primeros 5
    orden = np.argsort(porcentaje_nc_por_lote)[::-1][:5]
    print("\nLotes más problemáticos (mayor % de muestras No Conformes):")
    print("\n".join(map(lambda i: f"  {ids_lotes[i]}: {no_conformes_por_lote[i]} de {muestras_por_lote[i]} "
                                  f"muestras ({porcentaje_nc_por_lote[i]:.1f}%) - {estados_lotes[i]}", orden)))

    # ---------- Gráficos ----------
    figura, (torta, barras) = plt.subplots(1, 2, figsize=(16, 6), gridspec_kw={"width_ratios": [1, 3]})
    figura.suptitle("Análisis General de Calidad", fontsize=14, fontweight="bold")

    # Torta: conformes vs no conformes
    torta.pie([np.sum(estados == "CONFORME"), np.sum(no_conformes)],
              labels=["Conformes", "No conformes"], colors=["#4CAF50", "#E53935"],
              autopct="%1.1f%%", startangle=90)
    torta.set_title("Muestras inspeccionadas")

    # Barras apiladas: conformidad por lote
    posiciones = np.arange(len(ids_lotes))
    barras.bar(posiciones, conformes_por_lote, color="#4CAF50", label="Conformes")
    barras.bar(posiciones, no_conformes_por_lote, bottom=conformes_por_lote, color="#E53935", label="No conformes")
    barras.set_title("Conformidad por lote")
    barras.set_xlabel("Lote")
    barras.set_ylabel("Cantidad de muestras")
    barras.set_xticks(posiciones[::5])
    barras.set_xticklabels(ids_lotes[::5], rotation=90)
    barras.legend()

    plt.tight_layout()
    plt.show()


# ==========================================
# MENÚ DE ANÁLISIS
# ==========================================

def menu():
    opcion = ""
    while opcion != "0":
        print("\n========== ANÁLISIS DE DATOS ==========")
        print("   1. Análisis general de calidad")
        print("   2. Distribución de imperfecciones")
        print("   3. Desempeño de profesionales")
        print("   0. Salir")
        opcion = input("\nOpción: ")

        if opcion == "1":
            analisis_general()
        elif opcion == "2":
            distribucion_defectos()
        elif opcion == "3":
            desempeno_profesionales()
        elif opcion != "0":
            print("Opción incorrecta.")


if __name__ == "__main__":
    menu()