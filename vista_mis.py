import matplotlib.pyplot as plt
import pandas as pd
import solara
import datos


def _obtener_promedio_global_usd(conn):
    fila = conn.execute("SELECT AVG(precio) FROM laptops").fetchone()
    if fila and fila[0] is not None:
        return round(float(fila[0]), 2)
    return 1000.0


def _obtener_resumen_general_por_marca(conn):
    filas = conn.execute(
        """
        SELECT m.nombre, COUNT(l.id_laptop), AVG(l.precio)
        FROM marcas m
        LEFT JOIN laptops l ON l.id_marca = m.id_marca
        GROUP BY m.id_marca, m.nombre
        ORDER BY m.nombre
        """
    ).fetchall()
    resumen = {}
    for marca, cant_total, prom_total in filas:
        resumen[marca] = {
            "cantidad_total": int(cant_total or 0),
            "precio_general": round(float(prom_total), 2) if prom_total is not None else 0.0,
        }
    return resumen


def _parse_ram_independiente(valor, fallback):
    try:
        ram = int(str(valor).strip())
        return ram if ram > 0 else fallback
    except (ValueError, TypeError):
        return fallback


def _parse_presupuesto_independiente(valor, fallback):
    try:
        pres = float(str(valor).strip())
        return pres if pres > 0 else fallback
    except (ValueError, TypeError):
        return fallback


@solara.component
def GraficoStockDSS(conn, argumento):
    filas = datos.reportar(conn, argumento)
    if not filas:
        return

    df_stock = pd.DataFrame(filas, columns=["Marca", "Cantidad", "Precio_Promedio_USD"])
    df_stock["Cantidad"] = df_stock["Cantidad"].astype(int)
    df_stock = df_stock.sort_values("Cantidad", ascending=False).reset_index(drop=True)

    solara.Markdown(f"#### Disponibilidad de equipos por marca ({argumento} GB RAM)")
    fig3, ax_g3 = plt.subplots(figsize=(7.5, 3.8))
    barras_s = ax_g3.bar(df_stock["Marca"], df_stock["Cantidad"], color="#1976d2", width=0.55)
    ax_g3.set_title(f"Cantidad de laptops disponibles por marca ({argumento} GB RAM)")
    ax_g3.set_xlabel("Marca")
    ax_g3.set_ylabel("Cantidad de equipos")
    plt.xticks(rotation=35, ha="right")

    for rect, cant in zip(barras_s, df_stock["Cantidad"]):
        ax_g3.text(
            rect.get_x() + rect.get_width() / 2.0,
            rect.get_height(),
            f"{int(cant)}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.tight_layout()
    solara.FigureMatplotlib(fig3)
    plt.close(fig3)


@solara.component
def ReporteMIS(conn, argumento):
    resumen_general = _obtener_resumen_general_por_marca(conn)
    promedio_global = _obtener_promedio_global_usd(conn)

    if not resumen_general:
        solara.Info("No hay marcas registradas en la base de datos.")
        return

    # Estado independiente exclusivo para el primer gráfico
    ram_graf1_texto = solara.use_reactive(str(argumento))
    pres_graf1_texto = solara.use_reactive(str(promedio_global))

    ram_graf1 = _parse_ram_independiente(ram_graf1_texto.value, int(argumento))
    pres_graf1 = _parse_presupuesto_independiente(pres_graf1_texto.value, promedio_global)

    filas_graf1 = datos.reportar(conn, ram_graf1)

    solara.Markdown(f"### Reporte y DSS — Base filtro: {argumento} GB RAM (Precios en USD)")

    if filas_graf1:
        df_ram = pd.DataFrame(filas_graf1, columns=["Marca", "Cantidad", "Precio_Promedio_USD"])
        df_ram["Cantidad"] = df_ram["Cantidad"].astype(int)
        df_ram["Precio_Promedio_USD"] = df_ram["Precio_Promedio_USD"].round(2)
        df_ram["Brecha_USD"] = (df_ram["Precio_Promedio_USD"] - pres_graf1).round(2)
        df_ram["Estado_DSS"] = df_ram["Precio_Promedio_USD"].apply(
            lambda p: "Dentro de presupuesto" if p <= pres_graf1
            else ("Cerca del límite (<=15%)" if p <= pres_graf1 * 1.15 else "Sobre presupuesto")
        )
        df_ram = df_ram.sort_values("Precio_Promedio_USD", ascending=True).reset_index(drop=True)
        solara.DataFrame(df_ram)
    else:
        df_ram = pd.DataFrame(columns=["Marca", "Cantidad", "Precio_Promedio_USD", "Brecha_USD", "Estado_DSS"])
        solara.Info(f"No hay laptops registradas con {ram_graf1} GB de RAM para el primer gráfico.")

    # --- PRIMER GRÁFICO (INDEPENDIENTE): Ranking por marca — Precio USD ---
    solara.Markdown("#### Gráfico 1 (Independiente): Ranking por marca — Precio USD")
    with solara.Columns([1, 1]):
        solara.InputText(label="RAM Gráfico 1 (GB)", value=ram_graf1_texto)
        solara.InputText(label="Presupuesto Gráfico 1 (USD)", value=pres_graf1_texto)

    precios_ram = dict(zip(df_ram["Marca"], df_ram["Precio_Promedio_USD"])) if not df_ram.empty else {}

    registros_grafico = []
    for marca, info in resumen_general.items():
        tiene_ram = marca in precios_ram
        precio_barra = precios_ram[marca] if tiene_ram else info["precio_general"]

        if not tiene_ram:
            color = "#b0bec5"
        elif precio_barra <= pres_graf1:
            color = "#2e7d32"
        elif precio_barra <= pres_graf1 * 1.15:
            color = "#ed6c02"
        else:
            color = "#c62828"

        registros_grafico.append({
            "marca": marca,
            "precio": precio_barra,
            "color": color,
        })

    registros_grafico.sort(key=lambda x: x["precio"])

    marcas_ord = [r["marca"] for r in registros_grafico]
    precios_ord = [r["precio"] for r in registros_grafico]
    colores_ord = [r["color"] for r in registros_grafico]

    fig1, ax1 = plt.subplots(figsize=(8, 4.5))
    x_pos = range(len(marcas_ord))

    barras = ax1.bar(x_pos, precios_ord, color=colores_ord, width=0.58, label="Precio promedio (USD)")
    ax1.axhline(
        pres_graf1,
        color="#1565c0",
        linestyle="--",
        linewidth=1.8,
        label=f"Presupuesto (${pres_graf1} USD)"
    )
    ax1.set_title(f"Ranking DSS por marca ({ram_graf1} GB RAM) — Precio USD")
    ax1.set_xticks(list(x_pos))
    ax1.set_xticklabels(marcas_ord, rotation=35, ha="right")
    ax1.set_ylabel("Precio promedio (USD)")

    for rect, precio in zip(barras, precios_ord):
        ax1.text(
            rect.get_x() + rect.get_width() / 2.0,
            rect.get_height(),
            f"${precio:.0f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    ax1.legend(loc="upper left", fontsize=8)
    plt.tight_layout()
    solara.FigureMatplotlib(fig1)
    plt.close(fig1)

    # --- SEGUNDO GRÁFICO (INTACTO): Precio promedio por marca ---
    filas_graf2 = datos.reportar(conn, argumento)
    if filas_graf2:
        df_graf2 = pd.DataFrame(filas_graf2, columns=["Marca", "Cantidad", "Precio_Promedio_USD"])
        df_graf2["Precio_Promedio_USD"] = df_graf2["Precio_Promedio_USD"].round(2)

        solara.Markdown(f"#### Gráfico 2: Precio promedio por marca ({argumento} GB RAM — USD)")
        fig2, ax_g2 = plt.subplots(figsize=(8, 3.8))
        ax_g2.bar(df_graf2["Marca"], df_graf2["Precio_Promedio_USD"])
        ax_g2.set_title(f"Precio promedio por marca ({argumento} GB RAM)")
        ax_g2.set_xlabel("Marca")
        ax_g2.set_ylabel("Precio promedio (USD)")
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()

        solara.FigureMatplotlib(fig2)
        plt.close(fig2)
