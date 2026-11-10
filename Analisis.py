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
    rechazados = estados_lotes == "RECHAZADO"

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

    # ---------- Análisis extra ----------
    print("\n---------- Análisis extra ----------")
    print(f"% No conformes por lote → promedio: {np.mean(porcentaje_nc_por_lote):.1f}% | "
          f"mediana: {np.median(porcentaje_nc_por_lote):.1f}% | desvío: {np.std(porcentaje_nc_por_lote):.1f}%")
    print(f"Muestras por lote → mínimo: {np.min(muestras_por_lote)} | máximo: {np.max(muestras_por_lote)} | "
          f"promedio: {np.mean(muestras_por_lote):.1f}")

    rechazados_por_una = np.sum(rechazados & (no_conformes_por_lote == 1))
    print(f"Lotes rechazados por UNA sola muestra No Conforme: {rechazados_por_una} de {np.sum(rechazados)}")

    correlacion = np.corrcoef(muestras_por_lote, porcentaje_nc_por_lote)[0, 1]
    print(f"Correlación entre cantidad de muestras y % No conformes: {correlacion:.2f}")

    limites = np.arange(0, 26)                                  # límites de 0% a 25%
    rechazo_segun_limite = np.array(list(map(lambda limite: np.mean(porcentaje_nc_por_lote > limite) * 100, limites)))
    print(f"Simulación → con límite 5%: {rechazo_segun_limite[5]:.0f}% de lotes rechazados | "
          f"con límite 10%: {rechazo_segun_limite[10]:.0f}%")
   
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


    # ---------- Ventana 2: análisis extra ----------
    figura, (heatmap, scatter, curva) = plt.subplots(1, 3, figsize=(18, 6))
    figura.suptitle("Análisis General de Calidad - Análisis extra", fontsize=14, fontweight="bold")

    # Heatmap: los lotes en una grilla de 10 columnas, coloreados por % No conformes
    filas = int(np.ceil(len(ids_lotes) / 10))
    grilla = np.full(filas * 10, np.nan)                       # celdas vacías si no completa la grilla
    grilla[:len(ids_lotes)] = porcentaje_nc_por_lote
    imagen = heatmap.imshow(grilla.reshape(filas, 10), cmap="Reds")
    heatmap.set_title("Mapa de calor de lotes (% No conformes)")
    heatmap.set_xlabel("Lote (dentro de la fila)")
    heatmap.set_ylabel("Grupo de lotes")
    heatmap.set_xticks(np.arange(10))
    heatmap.set_xticklabels(np.arange(1, 11))
    heatmap.set_yticks(np.arange(filas))
    heatmap.set_yticklabels(list(map(lambda f: f"L{f * 10 + 1}-L{f * 10 + 10}", range(filas))))
    figura.colorbar(imagen, ax=heatmap, label="% No conformes")

    # Scatter: tamaño del lote vs % No conformes
    scatter.scatter(muestras_por_lote[~rechazados], porcentaje_nc_por_lote[~rechazados],
                    color="#4CAF50", label="Aprobados")
    scatter.scatter(muestras_por_lote[rechazados], porcentaje_nc_por_lote[rechazados],
                    color="#E53935", label="Rechazados")
    tamanios = np.arange(5, 21)
    scatter.plot(tamanios, 100 / tamanios, "k--", label="Una sola muestra No conforme")
    scatter.axhline(5, color="gray", linestyle=":", label="Límite 5%")
    scatter.set_title(f"Muestras por lote vs % No conformes (correlación: {correlacion:.2f})")
    scatter.set_xlabel("Cantidad de muestras del lote")
    scatter.set_ylabel("% No conformes")
    scatter.legend()

    # Curva: % de lotes rechazados según el límite elegido
    curva.plot(limites, rechazo_segun_limite, marker="o", color="#1E88E5", label="% lotes rechazados")
    curva.axvline(5, color="#E53935", linestyle="--", label="Límite actual (5%)")
    curva.set_title("Simulación: rechazo según el límite")
    curva.set_xlabel("Límite de No conformes (%)")
    curva.set_ylabel("% de lotes rechazados")
    curva.legend()

    plt.tight_layout()
    plt.show()

# ==========================================
# EJERCICIO 2: DISTRIBUCIÓN DE DEFECTOS
# ==========================================
def distribucion_defectos():
    #1. Obtención de datos
    defectos = cargar("defectos.csv")

    tipos = columna(defectos, "tipo")
    gravedades = columna(defectos, "gravedad").astype(int)
    muestras = columna(defectos, "muestra_id")

    #2. Métricas
    tipos_unicos, cantidades = np.unique(tipos, return_counts=True) #Cantidad de defectos por tipo

    gravedad_promedio = np.mean(gravedades)#Gravedad promedio

    gravedad_maxima = np.max(gravedades)#Gravedad máxima

    porcentaje_criticos = np.mean(gravedades == 5) * 100#Porcentaje de críticos
    pass



# ==========================================
# EJERCICIO 5: DESEMPEÑO DE PROFESIONALES
# ==========================================

def desempeno_profesionales():
    profesionales = cargar("profesionales.csv")
    inspecciones = cargar("inspecciones.csv")
    muestras = cargar("muestras.csv")
    defectos = cargar("defectos.csv")

    # ---------- Organizar los datos ----------

    # Solo considerar inspecciones finalizadas
    finalizadas = list(filter(
        lambda i: i["estado_inspeccion"] == "FINALIZADA",
        inspecciones
    ))

    # Relacionar cada muestra con su estado
    estados_muestras = {
        muestra["id"]: muestra["estado"]
        for muestra in muestras
    }

    # Relacionar cada muestra con sus defectos
    defectos_por_muestra = {}

    for defecto in defectos:
        id_muestra = defecto["muestra_id"]

        if id_muestra not in defectos_por_muestra:
            defectos_por_muestra[id_muestra] = []

        defectos_por_muestra[id_muestra].append(defecto)

    # ---------- Calcular métricas ----------

    nombres = []
    inspeccionadas = []
    reportes = []
    total_defectos = []
    defectos_criticos = []

    for profesional in profesionales:
        id_profesional = profesional["id"]

        propias = list(filter(
            lambda i: i["profesional_id"] == id_profesional,
            finalizadas
        ))

        muestras_propias = list(map(
            lambda i: i["muestra_id"],
            propias
        ))

        defectos_propios = [
            defecto
            for id_muestra in muestras_propias
            for defecto in defectos_por_muestra.get(id_muestra, [])
        ]

        nombres.append(profesional["nombre"])
        inspeccionadas.append(len(muestras_propias))

        # Una muestra no conforme finalizada tiene un reporte
        reportes.append(sum(map(
            lambda id_muestra:
                estados_muestras[id_muestra] == "NO_CONFORME",
            muestras_propias
        )))

        total_defectos.append(len(defectos_propios))

        defectos_criticos.append(sum(map(
            lambda defecto: int(defecto["gravedad"]) == 5,
            defectos_propios
        )))

    # Convertir las listas a arrays NumPy
    nombres = np.array(nombres)
    inspeccionadas = np.array(inspeccionadas)
    reportes = np.array(reportes)
    total_defectos = np.array(total_defectos)
    defectos_criticos = np.array(defectos_criticos)

    if len(nombres) == 0:
        print("No hay profesionales para analizar.")
        return

    # ---------- Resultados ----------

    print("\n========== DESEMPEÑO DE PROFESIONALES ==========")

    print("Total de inspecciones:", np.sum(inspeccionadas))
    print("Total de reportes:", np.sum(reportes))
    print("Total de defectos:", np.sum(total_defectos))
    print("Total de defectos críticos:", np.sum(defectos_criticos))

    print(f"\nPromedio de inspecciones por profesional: "
          f"{np.mean(inspeccionadas):.2f}")

    print(f"Desviación estándar de inspecciones: "
          f"{np.std(inspeccionadas):.2f}")

    # Ranking de profesionales
    orden = np.argsort(inspeccionadas)[::-1]

    print("\n---------- RANKING DE INSPECTORES ----------")

    for i in orden:
        print(f"{nombres[i]}:")
        print(f"  Inspecciones: {inspeccionadas[i]}")
        print(f"  Reportes: {reportes[i]}")
        print(f"  Defectos: {total_defectos[i]}")
        print(f"  Críticos: {defectos_criticos[i]}")

    # Mayor detección de defectos críticos
    indice = np.argmax(defectos_criticos)

    print("\nMayor cantidad de defectos críticos:")
    print(nombres[indice], "-", defectos_criticos[indice])

    # ---------- Gráficos ----------

    # Mostrar los 10 profesionales con más inspecciones
    top = orden[:10]

    plt.figure(figsize=(12, 6))
    plt.bar(nombres[top], inspeccionadas[top],
            color="#1E88E5")
    plt.title("Ranking de profesionales por inspecciones")
    plt.xlabel("Profesionales")
    plt.ylabel("Muestras inspeccionadas")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Comparación de defectos y defectos críticos
    posiciones = np.arange(len(top))
    ancho = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(posiciones - ancho / 2,
            total_defectos[top],
            ancho, label="Defectos totales",
            color="#FF9800")

    plt.bar(posiciones + ancho / 2,
            defectos_criticos[top],
            ancho, label="Defectos críticos",
            color="#E53935")

    plt.xticks(posiciones, nombres[top],
               rotation=45, ha="right")
    plt.title("Defectos detectados por profesional")
    plt.xlabel("Profesionales")
    plt.ylabel("Cantidad de defectos")
    plt.legend()
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



    