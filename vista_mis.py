
import matplotlib.pyplot as plt
import pandas as pd
import solara
import datos


@solara.component
def ReporteMIS(conn, argumento):

    filas = datos.reportar(conn, argumento)

    tabla = pd.DataFrame(
        filas,
        columns=["Marca", "Cantidad", "Precio_Promedio"]
    )

    precio_promedio = round(
        tabla["Precio_Promedio"].mean(),
        2
    )

    solara.Markdown(
        f"## Precio promedio general: ${precio_promedio}"
    )

    solara.DataFrame(tabla)

    fig, ax = plt.subplots()

    ax.bar(
        tabla["Marca"],
        tabla["Precio_Promedio"]
    )

    ax.set_title("Precio promedio por marca")
    ax.set_xlabel("Marca")
    ax.set_ylabel("Precio promedio")

    plt.xticks(rotation=45)

    solara.FigureMatplotlib(fig)
