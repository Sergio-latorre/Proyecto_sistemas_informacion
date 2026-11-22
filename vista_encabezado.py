import json
from pathlib import Path

import solara

FICHA = json.loads((Path(__file__).parent / "ficha.json").read_text(encoding="utf-8"))
@solara.component
def Encabezado():

    solara.Title(FICHA["organizacion"])

    solara.Markdown(f"""
# {FICHA["organizacion"]}

## Necesidad
{FICHA["necesidad"]}

## Quién decide
{FICHA["quien_decide"]}

## Componentes del Sistema de Información

### Hardware
{FICHA["hardware"]}

### Software
{FICHA["software"]}

### Datos
{FICHA["datos"]}

### Personas
{FICHA["personas"]}

### TIC
{FICHA["tic"]}
""")
