# Subdirección de Aseo de una gobernación (caso guiado)

**App:** https://proyecto-sistemas-informacion.onrender.com/  
**Repositorio:** https://github.com/Sergio-latorre/Proyecto_sistemas_informacion

**Necesidad:** Saber cada mes cuánto recoge cada municipio para decidir dónde reforzar la recolección. **Quién decide:** Subdirectora de aseo. **Tipo de SI:** MIS.

## Componentes del sistema de información

- **hardware:** Computadores de la subdirección y el servidor donde corre la app
- **software:** App Solara, módulo datos.py y el motor SQLite
- **datos:** Una fila = lo que un municipio recogió de un material en un mes
- **personas:** Operador que registra, analista que consolida, subdirectora que decide
- **tic:** La red de la gobernación y el navegador por el que se abre la app

## Proceso

1. El operador registra la recolección
2. La app consolida por municipio
3. La subdirectora revisa el reporte
4. Se reasignan rutas

## Cómo se usa


1. El usuario abre la aplicación y consulta las laptops disponibles filtrando por memoria RAM.
2. El usuario revisa el reporte que muestra la cantidad de laptops y el precio promedio por marca.
3. El usuario puede registrar una nueva laptop mediante el formulario de registro.
4. Con la información obtenida, el usuario compara opciones y apoya la decisión de compra o selección de equipos.


## Datos personales (Ley 1581 de 2012)


La aplicación almacena información técnica de laptops, como modelo, precio, memoria RAM y marca.
No se recolectan datos personales de personas naturales, tales como nombres, correos electrónicos,
documentos de identidad, direcciones o números telefónicos. Por esta razón, la información gestionada
corresponde a datos de productos y no a datos personales protegidos por la Ley 1581 de 2012.


## Correr en su equipo

```
conda activate si2026
solara run app.py
```
