import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap
from GestorArchivos import GestorArchivos

# ==========================================
# PALETA DE COLORES
# ==========================================
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from GestorArchivos import GestorArchivos

# ---------- Paleta de colores ----------
AZULES = ["#DCEAF7", "#B8D3EE", "#86B4DD", "#4F8FC6", "#2E6FAE"]
AMARILLOS = ["#F8E5A4", "#F4D37A", "#F2C14E", "#EAAF3D", "#D99A30"]
AZUL = AZULES[3]
AMARILLO = AMARILLOS[2]
GRIS_OSCURO = "#606D7A"
GRIS_CLARO = "#E3E8ED"
MAPA_AMARILLO_AZUL = LinearSegmentedColormap.from_list("amarillo_a_azul", ["#FFF2CF", "#F2D276", "#C2D8EB", "#7BA9D1", "#2E6FAE"])
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
    valores, repeticiones = np.unique(porcentaje_nc_por_lote, return_counts=True)
    moda = valores[np.argmax(repeticiones)]
    print(f"Moda de % NC por lote: {moda:.1f}% ({np.max(repeticiones)} lotes)")
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
    
    # np.full(...) crea un array de tamaño filas*10 lleno de np.nan (celdas vacías)
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
    scatter.set_title(f"Muestras por lote vs % No conformes")
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
    # 1. Obtención y validación de datos
    defectos = cargar("defectos.csv")
    datos_muestras = cargar("muestras.csv")
    inspecciones = cargar("inspecciones.csv")
    procedimientos = cargar("procedimientos.csv")

    if any(datos is None for datos in (defectos, datos_muestras, inspecciones, procedimientos)):
        print("Faltan archivos CSV para realizar el análisis de defectos.")
        return
    if not defectos:
        print("No hay defectos registrados para analizar.")
        return

    tipos = columna(defectos, "tipo")
    gravedades = columna(defectos, "gravedad").astype(int)
    ids_muestras_defecto = columna(defectos, "muestra_id")

    son_visuales = np.char.startswith(tipos, "Anomalía Visual")
    son_dimensionales = np.char.startswith(tipos, "Desviación ")
    if not np.all(son_visuales | son_dimensionales):
        raise ValueError("Hay defectos con tipos no clasificados como visuales o dimensionales.")

    # 2. Métricas generales y por tipo
    tipos_unicos, cantidades = np.unique(tipos, return_counts=True)
    gravedad_promedio = np.mean(gravedades)
    gravedad_maxima = np.max(gravedades)
    porcentaje_criticos = np.mean(gravedades == 5) * 100

    # 3. Resultados generales
    print("\n========== DISTRIBUCIÓN DE DEFECTOS ==========")
    print("Cantidad total de defectos:", len(defectos))
    print("\n---------- Cantidad por tipo ----------")
    print("\n".join(map(
        lambda tipo, cantidad: f"  {tipo}: {cantidad}",
        tipos_unicos, cantidades
    )))
    print(f"\nGravedad promedio: {gravedad_promedio:.2f}")
    print(f"Gravedad máxima: {gravedad_maxima}")
    print(f"Porcentaje de defectos críticos: {porcentaje_criticos:.2f}%")

    # 4. Riesgo por tipo
    gravedad_por_tipo = np.array([
        np.mean(gravedades[tipos == tipo]) for tipo in tipos_unicos
    ])
    criticos_por_tipo = np.array([
        np.sum(gravedades[tipos == tipo] == 5) for tipo in tipos_unicos
    ])
    print("\n---------- Riesgo por tipo de defecto ----------")
    print("\n".join(map(
        lambda tipo, promedio, criticos:
            f"  {tipo}: gravedad promedio {promedio:.2f} | críticos: {criticos}",
        tipos_unicos, gravedad_por_tipo, criticos_por_tipo
    )))

    # Muestras cerradas e inspecciones correspondientes
    muestras_cerradas = [
        m for m in datos_muestras if m["estado"] in ("CONFORME", "NO_CONFORME")
    ]
    if not muestras_cerradas:
        print("No hay muestras cerradas para los análisis por inspección.")
        return
    ids_cerradas = {m["id"] for m in muestras_cerradas}
    inspecciones_cerradas = [
        i for i in inspecciones if i["muestra_id"] in ids_cerradas
    ]
    procedimiento_por_muestra = {
        i["muestra_id"]: i["procedimiento_id"] for i in inspecciones_cerradas
    }
    ids_procedimientos = columna(procedimientos, "id")
    nombres_procedimientos = columna(procedimientos, "nombre")
    categorias_procedimientos = columna(procedimientos, "tipo")

    inspecciones_por_procedimiento = np.array([
        sum(i["procedimiento_id"] == id_proc for i in inspecciones_cerradas)
        for id_proc in ids_procedimientos
    ])
    defectos_por_procedimiento = np.array([
        sum(procedimiento_por_muestra.get(d["muestra_id"]) == id_proc for d in defectos)
        for id_proc in ids_procedimientos
    ])
    tasa_defectos = np.divide(
        defectos_por_procedimiento, inspecciones_por_procedimiento,
        out=np.zeros(len(procedimientos), dtype=float),
        where=inspecciones_por_procedimiento != 0
    )

    # 5. Frecuencia de defectos por procedimiento (tonos alternados dentro de cada categoría)
    orden = np.argsort(tasa_defectos)[::-1]
    etiquetas = [
        f"{nombres_procedimientos[i]} (n={inspecciones_por_procedimiento[i]})"
        for i in orden
    ]
    color_por_procedimiento = {}
    for categoria, paleta in (("dimensional", AZULES), ("visual", AMARILLOS)):
        indices = [i for i in orden if categorias_procedimientos[i].lower() == categoria]
        for posicion, i in enumerate(indices):
            color_por_procedimiento[i] = paleta[posicion % len(paleta)]
    colores = [color_por_procedimiento[i] for i in orden]

    print("\n---------- Defectos por procedimiento ----------")
    for i in orden:
        print(
            f"{nombres_procedimientos[i]}: {defectos_por_procedimiento[i]} defectos "
            f"en {inspecciones_por_procedimiento[i]} inspecciones "
            f"({tasa_defectos[i]:.2f} defectos/inspección)"
        )

    figura, grafico = plt.subplots(figsize=(14, 8), layout="constrained")
    barras = grafico.barh(etiquetas, tasa_defectos[orden], color=colores, edgecolor=GRIS_OSCURO, linewidth=0.6)
    grafico.invert_yaxis()
    grafico.bar_label(barras, labels=[
        f"{tasa_defectos[i]:.2f} ({defectos_por_procedimiento[i]} defectos)" for i in orden
    ], padding=4, fontsize=9)
    grafico.set_xlim(0, max(tasa_defectos.max(), 0.1) * 1.45)
    grafico.set_title(
        "Defectos detectados por procedimiento\n"
        f"{len(inspecciones_cerradas)} inspecciones de muestras cerradas · {len(defectos)} defectos"
    )
    grafico.set_xlabel("Defectos por inspección")
    grafico.set_ylabel("Procedimiento (n = inspecciones)")
    grafico.legend(handles=[
        Patch(color=AZUL, label="Dimensionales"),
        Patch(color=AMARILLO, label="Visuales")
    ], loc="lower right")
    plt.show()

    # 6. Gravedad de los defectos (dimensionales en escala azul; visuales amarillo)
    niveles = np.arange(1, 6)
    dimensionales_gravedad = np.array([
        np.sum(gravedades[son_dimensionales] == nivel) for nivel in niveles
    ])
    visuales_gravedad = np.array([
        np.sum(gravedades[son_visuales] == nivel) for nivel in niveles
    ])
    totales_gravedad = dimensionales_gravedad + visuales_gravedad

    figura, grafico = plt.subplots(figsize=(11, 6), layout="constrained")
    grafico.bar(niveles, dimensionales_gravedad, color=AZULES,
                edgecolor=GRIS_OSCURO, linewidth=0.6)
    grafico.bar(niveles, visuales_gravedad, bottom=dimensionales_gravedad,
                color=AMARILLO, edgecolor=GRIS_OSCURO, linewidth=0.6)
    for x, total in zip(niveles, totales_gravedad):
        grafico.text(x, total + max(totales_gravedad) * 0.015,
                     str(total), ha="center", va="bottom", fontsize=10)
    grafico.set_ylim(0, max(totales_gravedad) * 1.13)
    grafico.set_title(f"Distribución de gravedad · {len(defectos)} defectos")
    grafico.set_xlabel("Gravedad (1 = leve, 5 = crítica)")
    grafico.set_ylabel("Cantidad de defectos")
    grafico.set_xticks(niveles)
    grafico.legend(handles=[
        Patch(color=AZUL, label="Dimensionales"), Patch(color=AMARILLO, label="Visuales")
    ])
    # Aclarar el desglose del último nivel sin ocultar el aporte dimensional
    grafico.annotate(f"5 dimensionales + {visuales_gravedad[-1]} visuales",
                     xy=(5, totales_gravedad[-1]), xytext=(4.0, max(totales_gravedad) * 0.38),
                     arrowprops={"arrowstyle": "->", "color": GRIS_OSCURO}, fontsize=9)
    plt.show()

    # 7. Pareto agrupado: cinco gravedades dimensionales + todos los visuales
    nombres_pareto = np.array(["Leve", "Moderada", "Seria", "Severa", "Crítica", "Visuales"])
    cantidades_pareto = np.append(dimensionales_gravedad, np.sum(son_visuales))

    # Orden ascendente, como en la versión que venías usando. Para Pareto convencional, añadir [::-1].
    orden_pareto = np.argsort(cantidades_pareto)
    nombres_pareto = nombres_pareto[orden_pareto]
    cantidades_pareto = cantidades_pareto[orden_pareto]
    porcentaje_acumulado = np.cumsum(cantidades_pareto) / np.sum(cantidades_pareto) * 100
    colores_pareto = {
        "Leve": AZULES[0], "Moderada": AZULES[1], "Seria": AZULES[2],
        "Severa": AZULES[3], "Crítica": AZULES[4], "Visuales": AMARILLO
    }
    posiciones = np.arange(len(nombres_pareto))
    figura, grafico = plt.subplots(figsize=(12, 7), layout="constrained")
    barras = grafico.bar(posiciones, cantidades_pareto,
                         color=[colores_pareto[n] for n in nombres_pareto],
                         edgecolor=GRIS_OSCURO, linewidth=0.6)
    grafico.bar_label(barras, padding=3)
    grafico.set_title(f"Frecuencia acumulada por tipo · {len(defectos)} defectos")
    grafico.set_xlabel("Dimensionales por gravedad y visuales agrupados")
    grafico.set_ylabel("Cantidad de defectos")
    grafico.set_xticks(posiciones)
    grafico.set_xticklabels(nombres_pareto)
    grafico.set_ylim(0, max(cantidades_pareto) * 1.17)
    linea = grafico.twinx()
    linea.plot(posiciones, porcentaje_acumulado, color=GRIS_OSCURO,
               marker="o", linewidth=2, label="Porcentaje acumulado")
    linea.set_ylim(0, 105)
    linea.set_ylabel("Porcentaje acumulado (%)")
    linea.axhline(80, color=AMARILLOS[3], linestyle="--", label="Referencia 80 %")
    linea.legend(loc="upper left")
    plt.show()

    # 8. Heatmap: gravedades por procedimiento, por cada 100 inspecciones
    matriz = np.zeros((len(procedimientos), 5), dtype=int)
    for i, id_proc in enumerate(ids_procedimientos):
        for gravedad in niveles:
            matriz[i, gravedad - 1] = sum(
                procedimiento_por_muestra.get(d["muestra_id"]) == id_proc
                and int(d["gravedad"]) == gravedad for d in defectos
            )
    matriz_normalizada = np.divide(
        matriz, inspecciones_por_procedimiento[:, None],
        out=np.zeros_like(matriz, dtype=float),
        where=inspecciones_por_procedimiento[:, None] != 0
    ) * 100
    etiquetas = [
        f"{nombres_procedimientos[i]} (n={inspecciones_por_procedimiento[i]})"
        for i in range(len(procedimientos))
    ]
    figura, heatmap = plt.subplots(figsize=(13, 8), layout="constrained")
    imagen = heatmap.imshow(matriz_normalizada, cmap=MAPA_AMARILLO_AZUL, aspect="auto")
    heatmap.set_title("Gravedad por procedimiento · Defectos por 100 inspecciones")
    heatmap.set_xlabel("Gravedad del defecto")
    heatmap.set_ylabel("Procedimiento (n = inspecciones cerradas)")
    heatmap.set_xticks(np.arange(5), labels=[1, 2, 3, 4, 5])
    heatmap.set_yticks(np.arange(len(procedimientos)), labels=etiquetas)
    maximo_celda = matriz_normalizada.max()
    for i in range(len(procedimientos)):
        for j in range(5):
            valor = matriz_normalizada[i, j]
            heatmap.text(j, i, f"{valor:.1f}", ha="center", va="center",
                         color="white" if valor > maximo_celda * 0.65 else "#263747", fontsize=9)
    figura.colorbar(imagen, ax=heatmap, label="Defectos por 100 inspecciones")
    plt.show()

    # 9. Concentración de gravedad: comparar categorías con colores fijos
    gravedad_visual = np.sum(gravedades[son_visuales])
    gravedad_dimensional = np.sum(gravedades[son_dimensionales])
    gravedad_acumulada = np.array([gravedad_visual, gravedad_dimensional])
    porcentaje_gravedad = gravedad_acumulada / gravedad_acumulada.sum() * 100
    print("\n---------- Concentración de gravedad ----------")
    print(f"Gravedad acumulada visual: {gravedad_visual} ({porcentaje_gravedad[0]:.2f} %)")
    print(f"Gravedad acumulada dimensional: {gravedad_dimensional} ({porcentaje_gravedad[1]:.2f} %)")
    figura, grafico = plt.subplots(figsize=(9, 6), layout="constrained")
    barras = grafico.bar(["Visuales", "Dimensionales"], gravedad_acumulada,
                         color=[AMARILLO, AZUL], edgecolor=GRIS_OSCURO, linewidth=0.6)
    grafico.bar_label(barras, padding=4)
    grafico.set_title("Gravedad acumulada por categoría")
    grafico.set_xlabel("Categoría")
    grafico.set_ylabel("Suma de gravedades (indicador descriptivo)")
    grafico.set_ylim(0, max(gravedad_acumulada) * 1.13)
    plt.show()

    # 10. Defectos por muestra; colores graduados por número de defectos

    # Cargar muestras y considerar solo las cerradas
    datos_muestras = cargar("muestras.csv")

    muestras_cerradas = list(filter(
        lambda m: m["estado"] in ("CONFORME", "NO_CONFORME"),
        datos_muestras
    ))

    # Obtener IDs y estados
    ids_muestras = columna(muestras_cerradas, "id")
    estados_muestras = columna(muestras_cerradas, "estado")

    # Contar cuántos defectos tiene cada muestra
    # ids_muestras_defecto viene del paso 1
    ids_con_defectos, conteos = np.unique(
        ids_muestras_defecto,
        return_counts=True
    )

    defectos_por_muestra = dict(zip(ids_con_defectos, conteos))

    # Incluir también las muestras que tienen cero defectos
    cantidades_por_muestra = np.array([
        defectos_por_muestra.get(id_muestra, 0)
        for id_muestra in ids_muestras
    ])

    # ---------- Métricas ----------

    promedio_muestra = np.mean(cantidades_por_muestra)
    mediana_muestra = np.median(cantidades_por_muestra)
    maximo_muestra = int(np.max(cantidades_por_muestra))

    muestras_sin_defectos = np.sum(cantidades_por_muestra == 0)
    muestras_con_defectos = np.sum(cantidades_por_muestra > 0)

    print("\n---------- Defectos por muestra ----------")
    print("Muestras inspeccionadas:", len(ids_muestras))
    print("Muestras sin defectos:", muestras_sin_defectos)
    print("Muestras con defectos:", muestras_con_defectos)
    print(f"Promedio de defectos por muestra: {promedio_muestra:.2f}")
    print(f"Mediana de defectos por muestra: {mediana_muestra:.2f}")
    print("Máximo de defectos en una muestra:", maximo_muestra)

    # ---------- Preparar los gráficos ----------

    # Excluir del gráfico las muestras sin defectos
    niveles = np.arange(1, maximo_muestra + 1)

    # Cantidad de muestras conformes y no conformes por nivel
    conformes = np.array([
        np.sum(
            (cantidades_por_muestra == n) &
            (estados_muestras == "CONFORME")
        )
        for n in niveles
    ])

    no_conformes = np.array([
        np.sum(
            (cantidades_por_muestra == n) &
            (estados_muestras == "NO_CONFORME")
        )
        for n in niveles
    ])

    totales = conformes + no_conformes

    # Porcentaje no conforme para cada cantidad de defectos
    porcentajes_nc = np.divide(
        no_conformes,
        totales,
        out=np.zeros(len(niveles), dtype=float),
        where=totales != 0
    ) * 100

    # ---------- Crear los dos gráficos ----------

    figura, (barras, porcentajes) = plt.subplots(
        1, 2,
        figsize=(16, 6),
        layout="constrained"
    )

    figura.suptitle(
        "Defectos por muestra y conformidad\n"
        f"{muestras_con_defectos} muestras con defectos de "
        f"{len(ids_muestras)} inspeccionadas",
        fontsize=14,
        fontweight="bold"
    )

    # ---------- Gráfico A: Cantidad de muestras ----------

    barras.bar(
        niveles,
        conformes,
        color="#B8C8D7",
        label="Conformes",
        edgecolor=GRIS_OSCURO
    )

    barras.bar(
        niveles,
        no_conformes,
        bottom=conformes,
        color=AZULES[4],
        label="No conformes",
        edgecolor=GRIS_OSCURO
    )

    barras.set_title("Muestras según cantidad de defectos")
    barras.set_xlabel("Defectos por muestra")
    barras.set_ylabel("Cantidad de muestras")
    barras.set_xticks(niveles)
    barras.legend()

    # ---------- Gráfico B: Porcentaje no conforme ----------

# Degradé según cantidad de defectos, no según porcentaje
    colores_porcentaje = [
        AMARILLOS[min(
            int((n - 1) * len(AMARILLOS) / len(niveles)),
            len(AMARILLOS) - 1
        )]
        for n in niveles
    ]

    columnas = porcentajes.bar(
        niveles,
        porcentajes_nc,
        color=colores_porcentaje,
        edgecolor=GRIS_OSCURO
    )

    porcentajes.bar_label(
        columnas,
        labels=[
            f"{porcentajes_nc[i]:.1f}%\n(n={totales[i]})"
            for i in range(len(niveles))
        ],
        padding=3,
        fontsize=9
    )

    porcentajes.set_title("No conformidad según cantidad de defectos")
    porcentajes.set_xlabel("Defectos por muestra")
    porcentajes.set_ylabel("Muestras no conformes (%)")
    porcentajes.set_xticks(niveles)
    porcentajes.set_ylim(0, 115)

    plt.show()





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
    if np.sum(inspeccionadas) == 0:
        print("No hay inspecciones finalizadas para analizar.")
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

    # ---------- Análisis extra ----------

    print("\n---------- ANÁLISIS EXTRA ----------")

    # Promedio de defectos críticos por inspección
    criticos_por_inspeccion = np.divide(
        defectos_criticos,
        inspeccionadas,
        out=np.zeros(len(inspeccionadas), dtype=float),
        where=inspeccionadas != 0
    )

    print(f"Promedio global de defectos por inspección: "
        f"{np.sum(total_defectos) / np.sum(inspeccionadas):.3f}")

    print(f"Promedio global de críticos por inspección: "
        f"{np.sum(defectos_criticos) / np.sum(inspeccionadas):.3f}")

    print(f"Mediana de inspecciones por profesional: "
        f"{np.median(inspeccionadas):.1f}")

    print(f"Mínimo de inspecciones: {np.min(inspeccionadas)}")
    print(f"Máximo de inspecciones: {np.max(inspeccionadas)}")

    # Ranking normalizado de defectos críticos
    orden_criticos = np.argsort(criticos_por_inspeccion)[::-1][:5]

    print("\nProfesionales con más críticos por inspección:")

    for i in orden_criticos:
        print(
            f"{nombres[i]}: {criticos_por_inspeccion[i]:.3f} "
            f"({defectos_criticos[i]} críticos en "
            f"{inspeccionadas[i]} inspecciones)"
        )

    # Interpretación automática
    print("\n---------- INTERPRETACIÓN ----------")

    print(
        "La cantidad de inspecciones realizadas presenta una "
        f"desviación estándar de {np.std(inspeccionadas):.2f}, "
        "lo que permite observar la dispersión de la carga "
        "de trabajo entre profesionales."
    )

    print(
        "Para comparar la detección de defectos críticos, "
        "se considera también su frecuencia por inspección, "
        "ya que los profesionales no necesariamente realizaron "
        "la misma cantidad de inspecciones."
    )

    # Ranking de profesionales
    orden = np.argsort(inspeccionadas)[::-1]

    print("\n---------- TOP 10 INSPECTORES ----------")

    for i in orden[:10]:
        print(f"{nombres[i]}:")
        print(f"  Inspecciones: {inspeccionadas[i]}")
        print(f"  Reportes: {reportes[i]}")
        print(f"  Defectos: {total_defectos[i]}")
        print(f"  Críticos: {defectos_criticos[i]}")

    # Mayor detección de defectos críticos
    maximo_criticos = np.max(defectos_criticos)
    indices = np.where(defectos_criticos == maximo_criticos)[0]

    print("\nProfesionales con más defectos críticos:")

    for i in indices:
        print(nombres[i], "-", defectos_criticos[i])

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
 
    top_criticos = np.argsort(defectos_criticos)[::-1][:10]

    posiciones = np.arange(len(top_criticos))
    ancho = 0.35

    plt.figure(figsize=(12, 6))
    plt.bar(posiciones - ancho / 2,
            total_defectos[top_criticos],
            ancho, label="Defectos totales",
            color="#FF9800")

    plt.bar(posiciones + ancho / 2,
            defectos_criticos[top_criticos],
            ancho, label="Defectos críticos",
            color="#E53935")

    plt.xticks(posiciones, nombres[top_criticos],
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



    