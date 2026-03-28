from database.conexion import query_fetchall, query_commit


def registrar(placa, tipo_vehiculo, tipo_registro, celda_id=None, usuario_id=None, observacion=None):
    return query_commit("""
        INSERT INTO entradas_salidas
               (placa, tipo_vehiculo, tipo_registro, celda_id, usuario_id, observacion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (placa, tipo_vehiculo, tipo_registro, celda_id, usuario_id, observacion or None))


def obtener_historial(limite=50):
    return query_fetchall(f"""
        SELECT TOP {int(limite)}
            e.id, e.placa, e.tipo_vehiculo, e.tipo_registro,
            c.codigo AS celda,
            u.nombre AS usuario,
            CONVERT(VARCHAR,e.fecha_hora,120) AS fecha_hora,
            e.observacion
        FROM entradas_salidas e
        LEFT JOIN celdas   c ON c.id = e.celda_id
        LEFT JOIN usuarios u ON u.id = e.usuario_id
        ORDER BY e.fecha_hora DESC
    """)


def buscar_por_placa(placa):
    return query_fetchall("""
        SELECT e.id, e.placa, e.tipo_vehiculo, e.tipo_registro,
               c.codigo AS celda,
               CONVERT(VARCHAR,e.fecha_hora,120) AS fecha_hora,
               e.observacion
        FROM entradas_salidas e
        LEFT JOIN celdas c ON c.id = e.celda_id
        WHERE e.placa LIKE ?
        ORDER BY e.fecha_hora DESC
    """, (f"%{placa}%",))
