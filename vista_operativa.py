
import pandas as pd
import solara
import datos

parametro = solara.reactive(8)

@solara.component
def VistaOperativa(conn):

    solara.Markdown("## Consulta de Laptops")

    solara.InputText(
        label="RAM",
        value=parametro
    )

    filas = datos.consultar(conn, parametro.value)

    df = pd.DataFrame(filas)

    solara.DataFrame(df)
