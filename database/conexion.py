"""
Conexion a SQL Server - Parqueadero Autos Colombia
"""

import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=ParqueaderoAutoColombia;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)


def query_fetchall(sql, params=None):
    """SELECT que retorna lista de diccionarios."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    finally:
        cur.close()
        conn.close()


def query_fetchone(sql, params=None):
    """SELECT que retorna un solo diccionario o None."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        cols = [c[0] for c in cur.description]
        row = cur.fetchone()
        return dict(zip(cols, row)) if row else None
    finally:
        cur.close()
        conn.close()


def query_scalar(sql, params=None):
    """SELECT que retorna un solo valor escalar (COUNT, MAX, etc)."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
        conn.close()


def query_insert(sql, params=None):
    """
    INSERT con OUTPUT INSERTED.id para obtener el ID generado.
    El SQL DEBE incluir 'OUTPUT INSERTED.id'.
    Retorna el ID insertado como entero.
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        row = cur.fetchone()
        conn.commit()
        return row[0] if row else None
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


def query_commit(sql, params=None):
    """UPDATE / DELETE / INSERT sin retorno de ID."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
