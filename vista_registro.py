
import inspect
import json
from pathlib import Path

import solara
import datos

EJ = json.loads(
    (Path(__file__).parent / "ejemplos.json").read_text(
        encoding="utf-8"
    )
)

REGISTRO = getattr(datos, EJ["registro_valido"][0])

CAMPOS = list(
    inspect.signature(REGISTRO).parameters
)[1:]

campos = {
    c: solara.reactive("")
    for c in CAMPOS
}

mensaje = solara.reactive("")


def procesar(conn, valores):
    """Valida y registra. Devuelve 'Registrado' o 'Rechazado: ...'."""

    # Campo vacío
    for valor in valores.values():
        if str(valor).strip() == "":
            return "Rechazado: campo vacío"

    try:
        datos_convertidos = {}

        for nombre, valor in valores.items():

            if nombre in ("precio",):
                datos_convertidos[nombre] = float(valor)

            elif nombre in ("ram", "id_marca"):
                datos_convertidos[nombre] = int(valor)

            else:
                datos_convertidos[nombre] = valor

    except ValueError:
        return "Rechazado: dato numérico inválido"

    ok = REGISTRO(
        conn,
        *[
            datos_convertidos[c]
            for c in CAMPOS
        ]
    )

    return (
        "Registrado"
        if ok
        else "Rechazado: la base rechazó el registro"
    )


@solara.component
def Registro(conn):

    for nombre, estado in campos.items():
        solara.InputText(
            nombre,
            value=estado
        )

    def guardar():

        valores = {
            nombre: estado.value
            for nombre, estado in campos.items()
        }

        mensaje.set(
            procesar(conn, valores)
        )

    solara.Button(
        "Guardar",
        on_click=guardar
    )

    solara.Markdown(
        mensaje.value
    )
