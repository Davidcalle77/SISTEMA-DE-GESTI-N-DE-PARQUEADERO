from database.conexion import query_fetchall, query_fetchone, query_scalar, query_commit
from app.models.pago import calcular_pago


def obtener_todas():
    return query_fetchall(
        """
        SELECT c.id, c.codigo, c.tipo, c.sector, c.estado,
               u.nombre AS usuario_nombre, u.placa AS usuario_placa,
               u.cedula AS usuario_cedula, u.telefono AS usuario_telefono,
               u.id AS usuario_id
        FROM celdas c
        LEFT JOIN usuarios u ON u.id = c.usuario_id
        ORDER BY c.sector, c.codigo
    """
    )


def obtener_por_id(id):
    return query_fetchone(
        """
        SELECT c.id, c.codigo, c.tipo, c.sector, c.estado,
               u.nombre AS usuario_nombre, u.placa AS usuario_placa,
               u.id AS usuario_id
        FROM celdas c
        LEFT JOIN usuarios u ON u.id = c.usuario_id
        WHERE c.id = ?
    """,
        (id,),
    )


def obtener_libres(tipo):
    return query_fetchall(
        """
        SELECT id, codigo, sector FROM celdas
        WHERE estado='libre' AND tipo=?
        ORDER BY codigo
    """,
        (tipo,),
    )


def hay_disponibles(tipo):
    return (
        query_scalar(
            "SELECT COUNT(1) FROM celdas WHERE estado='libre' AND tipo=?", (tipo,)
        )
        > 0
    )


def asignar(celda_id, usuario_id):
    return query_commit(
        """
        UPDATE celdas
        SET estado='ocupada', usuario_id=?, fecha_asignacion=GETDATE()
        WHERE id=?
    """,
        (usuario_id, celda_id),
    )


from app.models.pago import calcular_pago


def liberar(celda_id):
    # 1. Calcular pago automáticamente
    total_pagado = calcular_pago(celda_id)

    # 2. Obtener datos actuales
    celda = query_fetchone(
        """
        SELECT usuario_id, fecha_asignacion
        FROM celdas
        WHERE id=?
    """,
        (celda_id,),
    )

    if not celda:
        return False

    usuario_id = celda["usuario_id"]
    fecha_entrada = celda["fecha_asignacion"]

    # 3. Guardar historial (movimientos)
    query_commit(
        """
        INSERT INTO movimientos (celda_id, usuario_id, fecha_entrada, fecha_salida, total_pagado)
        VALUES (?, ?, ?, GETDATE(), ?)
    """,
        (celda_id, usuario_id, fecha_entrada, total_pagado),
    )

    # 4. Liberar celda
    return query_commit(
        """
        UPDATE celdas
        SET estado='libre', usuario_id=NULL, fecha_asignacion=NULL
        WHERE id=?
    """,
        (celda_id,),
    )

    # 2. Guardar en movimientos
    query_commit(
        """
        INSERT INTO movimientos (celda_id, usuario_id, fecha_entrada, fecha_salida, total_pagado)
        VALUES (?, ?, ?, GETDATE(), ?)
    """,
        (celda_id, usuario_id, fecha_entrada, total_pagado),
    )

    # 3. Liberar celda
    return query_commit(
        """
        UPDATE celdas
        SET estado='libre', usuario_id=NULL, fecha_asignacion=NULL
        WHERE id=?
    """,
        (celda_id,),
    )


def poner_mantenimiento(celda_id, motivo, fecha_fin=None):
    query_commit("UPDATE celdas SET estado='mantenimiento' WHERE id=?", (celda_id,))
    return query_commit(
        """
        INSERT INTO mantenimientos (celda_id, motivo, fecha_fin)
        VALUES (?, ?, ?)
    """,
        (celda_id, motivo, fecha_fin),
    )


def reporte():
    return query_fetchone(
        """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN estado='libre'          THEN 1 ELSE 0 END) AS libres,
            SUM(CASE WHEN estado='ocupada'        THEN 1 ELSE 0 END) AS ocupadas,
            SUM(CASE WHEN estado='mantenimiento'  THEN 1 ELSE 0 END) AS mantenimiento
        FROM celdas
    """
    )
