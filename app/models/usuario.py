from database.conexion import query_fetchall, query_fetchone, query_scalar, query_insert, query_commit


def obtener_todos():
    return query_fetchall("""
        SELECT u.id, u.cedula, u.nombre, u.telefono, u.correo,
               u.tipo_vehiculo, u.placa, u.estado,
               CONVERT(VARCHAR,u.fecha_registro,103) AS fecha_registro,
               c.codigo AS celda, c.id AS celda_id
        FROM usuarios u
        LEFT JOIN celdas c ON c.usuario_id = u.id
        WHERE u.estado = 'activo'
        ORDER BY u.nombre
    """)


def obtener_por_id(id):
    return query_fetchone("""
        SELECT u.id, u.cedula, u.nombre, u.telefono, u.correo,
               u.tipo_vehiculo, u.placa, u.estado,
               c.codigo AS celda, c.id AS celda_id
        FROM usuarios u
        LEFT JOIN celdas c ON c.usuario_id = u.id
        WHERE u.id = ?
    """, (id,))


def buscar(termino):
    t = f"%{termino}%"
    return query_fetchall("""
        SELECT u.id, u.cedula, u.nombre, u.telefono, u.correo,
               u.tipo_vehiculo, u.placa, u.estado,
               CONVERT(VARCHAR,u.fecha_registro,103) AS fecha_registro,
               c.codigo AS celda, c.id AS celda_id
        FROM usuarios u
        LEFT JOIN celdas c ON c.usuario_id = u.id
        WHERE u.estado='activo'
          AND (u.cedula LIKE ? OR u.placa LIKE ? OR u.nombre LIKE ?)
        ORDER BY u.nombre
    """, (t, t, t))


def registrar(cedula, nombre, telefono, correo, tipo_vehiculo, placa):
    """Inserta usuario y retorna el ID generado."""
    return query_insert("""
        INSERT INTO usuarios (cedula, nombre, telefono, correo, tipo_vehiculo, placa)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cedula, nombre, telefono, correo or None, tipo_vehiculo, placa))


def actualizar(id, nombre, telefono, correo, placa):
    return query_commit("""
        UPDATE usuarios SET nombre=?, telefono=?, correo=?, placa=?
        WHERE id=?
    """, (nombre, telefono, correo or None, placa, id))


def inactivar(id):
    query_commit("UPDATE celdas SET estado='libre', usuario_id=NULL, fecha_asignacion=NULL WHERE usuario_id=?", (id,))
    return query_commit("UPDATE usuarios SET estado='inactivo', fecha_baja=GETDATE() WHERE id=?", (id,))


def existe_cedula(cedula, excluir_id=None):
    if excluir_id:
        return query_scalar("SELECT COUNT(1) FROM usuarios WHERE cedula=? AND id!=?", (cedula, excluir_id)) > 0
    return query_scalar("SELECT COUNT(1) FROM usuarios WHERE cedula=?", (cedula,)) > 0


def existe_placa(placa, excluir_id=None):
    if excluir_id:
        return query_scalar("SELECT COUNT(1) FROM usuarios WHERE placa=? AND id!=?", (placa, excluir_id)) > 0
    return query_scalar("SELECT COUNT(1) FROM usuarios WHERE placa=?", (placa,)) > 0
