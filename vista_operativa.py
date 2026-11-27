import pandas as pd
import solara
import datos

ram_filtro_texto = solara.reactive("8")


def obtener_ram_entero(valor=None):
    raw = ram_filtro_texto.value if valor is None else valor
    try:
        ram_num = int(str(raw).strip())
        return ram_num if ram_num > 0 else 8
    except (ValueError, TypeError):
        return 8


@solara.component
def VistaOperativa(conn, ram_reactiva=None):
    estado_ram = ram_reactiva if ram_reactiva is not None else ram_filtro_texto

    solara.Markdown("## Consulta de Laptops")

    solara.InputText(
        label="RAM (GB)",
        value=estado_ram
    )

    ram_num = obtener_ram_entero(estado_ram.value)
    filas = datos.consultar(conn, ram_num)

    if filas:
        df = pd.DataFrame(
            filas,
            columns=["ID", "Modelo", "Precio", "RAM", "SSD", "Procesador", "SO", "ID_Marca"]
        )
        solara.DataFrame(df)
    else:
        solara.Info(f"No hay laptops registradas con {ram_num} GB de RAM.")
