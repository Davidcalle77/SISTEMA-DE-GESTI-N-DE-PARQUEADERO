from database.conexion import query_fetchall, query_fetchone, query_commit

from database.conexion import query_fetchone
from datetime import datetime


def calcular_pago(celda_id, tarifa_hora=2000):
    # Primero intenta obtener la fecha de entrada de entradas_salidas
    entrada = query_fetchone(
        """
        SELECT TOP 1 fecha_hora
        FROM entradas_salidas
        WHERE celda_id = ? AND tipo_registro = 'entrada'
        ORDER BY fecha_hora DESC
    """,
        (celda_id,),
    )
    
    # Si no hay entrada en entradas_salidas, obtén de celdas.fecha_asignacion
    if not entrada:
        entrada = query_fetchone(
            """
            SELECT fecha_asignacion AS fecha_hora
            FROM celdas
            WHERE id = ? AND estado = 'ocupada'
        """,
            (celda_id,),
        )

    if not entrada or not entrada["fecha_hora"]:
        return 0

    fecha_entrada = entrada["fecha_hora"]
    fecha_salida = datetime.now()

    tiempo = fecha_salida - fecha_entrada
    horas = tiempo.total_seconds() / 3600

    # mínimo 1 hora
    horas = max(1, round(horas))

    total = horas * tarifa_hora

    return total


def obtener_todos():
    return query_fetchall(
        """
        SELECT p.id, u.nombre, u.cedula, u.placa,
               p.monto, p.mes_pagado, p.estado,
               CONVERT(VARCHAR,p.fecha_pago,103) AS fecha_pago,
               p.observacion
        FROM pagos p
        JOIN usuarios u ON u.id = p.usuario_id
        ORDER BY p.fecha_pago DESC
    """
    )


def obtener_por_usuario(usuario_id):
    return query_fetchall(
        """
        SELECT p.id, p.monto, p.mes_pagado, p.estado,
               CONVERT(VARCHAR,p.fecha_pago,103) AS fecha_pago,
               p.observacion
        FROM pagos p WHERE p.usuario_id=?
        ORDER BY p.fecha_pago DESC
    """,
        (usuario_id,),
    )


def registrar(usuario_id, monto, mes_pagado, observacion=None):
    return query_commit(
        """
        INSERT INTO pagos (usuario_id, monto, mes_pagado, estado, observacion)
        VALUES (?, ?, ?, 'pagado', ?)
    """,
        (usuario_id, monto, mes_pagado, observacion or None),
    )


def estado_por_usuario():
    return query_fetchall(
        """
        SELECT u.id, u.nombre, u.cedula, u.placa,
               ISNULL(
                   (SELECT TOP 1 mes_pagado FROM pagos
                    WHERE usuario_id=u.id AND estado='pagado'
                    ORDER BY fecha_pago DESC),
               'Sin pagos') AS ultimo_pago
        FROM usuarios u
        WHERE u.estado='activo'
        ORDER BY u.nombre
    """
    )


def resumen():
    return query_fetchone(
        """
        SELECT COUNT(*) AS total_pagos,
               ISNULL(SUM(monto),0) AS total_recaudado
        FROM pagos WHERE estado='pagado'
    """
    )
