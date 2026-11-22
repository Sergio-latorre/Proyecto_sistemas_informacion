"""Capa de datos de mi proyecto: funciones con ?, sin tablero interactivo."""
import sqlite3
from pathlib import Path

AQUI = Path(__file__).parent  # la carpeta de este archivo; nunca una ruta fija de su equipo


def conectar():
    """Abre base.db. Si no existe (p. ej. en la nube), la crea con esquema.sql y semilla.sql."""
    nueva = not (AQUI / "base.db").exists()
    conn = sqlite3.connect(AQUI / "base.db", check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")  # que SQLite revise las llaves foráneas
    if nueva:
        conn.executescript((AQUI / "esquema.sql").read_text(encoding="utf-8"))
        conn.executescript((AQUI / "semilla.sql").read_text(encoding="utf-8"))
        conn.commit()
    return conn


def consultar(conn, parametro):
    """Consulta (TPS): filas de mi tabla de hechos filtradas por parametro."""
    return conn.execute( """
        SELECT * FROM laptops WHERE ram = ?
        """, (parametro,)).fetchall()

def reportar(conn, parametro):
    """Reporte (MIS): resumen con JOIN y GROUP BY, filtrado por parametro."""
    return conn.execute("""
        SELECT m.nombre, COUNT(*) AS cantidad, AVG(l.precio) AS precio_promedio
        FROM laptops l JOIN marcas m ON l.id_marca = m.id_marca
        WHERE l.ram= ?
        GROUP BY m.nombre """, (parametro,)).fetchall()

def registrar(conn, modelo, precio, ram, id_marca):
    """Registro (TPS): True si la base acepta la fila; False si la rechaza."""
    try:
        conn.execute("""
            INSERT INTO laptops(modelo, precio, ram, ssd, procesador, sistema_operativo , id_marca)
            VALUES (?,?,?,512, 'Intel i5', 'Windows 11', ?)
            """, (modelo, precio, ram, id_marca))
        conn.commit()
        return True
    except sqlite3.Error:
        conn.rollback()
        return False

