import json
from pathlib import Path

import solara
import datos
from vista_encabezado import Encabezado
from vista_mis import GraficoStockDSS, ReporteMIS
from vista_operativa import VistaOperativa, obtener_ram_entero
from vista_registro import Registro

conn = datos.conectar()
EJEMPLOS = json.loads((Path(__file__).parent / "ejemplos.json").read_text(encoding="utf-8"))
ram_seleccionada = solara.reactive("8")


@solara.component
def Page():
    solara.Title("Sistema de Información - Catálogo de Laptops")
    Encabezado()

    ram_actual = obtener_ram_entero(ram_seleccionada.value)

    with solara.Columns([1, 1]):
        with solara.Card("Consulta"):
            VistaOperativa(conn, ram_seleccionada)
            GraficoStockDSS(conn, ram_actual)
        with solara.Card("Reporte"):
            ReporteMIS(conn, ram_actual)

    with solara.Card("Registrar"):
        Registro(conn)
