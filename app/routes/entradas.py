from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import entrada as EM
from app.models import usuario as UM
from database.conexion import query_fetchone

entradas_bp = Blueprint('entradas', __name__, url_prefix='/entradas')


@entradas_bp.route('/')
def index():
    return render_template('entradas/index.html',
                           historial=EM.obtener_historial(50))


@entradas_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        placa         = request.form.get('placa', '').strip().upper()
        tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip()
        tipo_registro = request.form.get('tipo_registro', '').strip()
        observacion   = request.form.get('observacion', '').strip()

        if not all([placa, tipo_vehiculo, tipo_registro]):
            flash('Placa, tipo de vehiculo y tipo de movimiento son obligatorios.', 'danger')
            return redirect(url_for('entradas.registrar'))

        # Buscar si la placa pertenece a un usuario mensual activo
        usuario = query_fetchone(
            "SELECT id FROM usuarios WHERE placa=? AND estado='activo'", (placa,)
        )
        usuario_id = usuario['id'] if usuario else None

        # Buscar celda del usuario si existe
        celda_id = None
        if usuario_id:
            celda = query_fetchone(
                "SELECT id FROM celdas WHERE usuario_id=?", (usuario_id,)
            )
            celda_id = celda['id'] if celda else None

        EM.registrar(placa, tipo_vehiculo, tipo_registro, celda_id, usuario_id, observacion)
        flash(f'{tipo_registro.upper()} registrada para la placa {placa}.', 'success')
        return redirect(url_for('entradas.index'))

    return render_template('entradas/registrar.html')


@entradas_bp.route('/buscar')
def buscar():
    placa = request.args.get('placa', '').strip().upper()
    resultados = EM.buscar_por_placa(placa) if placa else []
    return render_template('entradas/buscar.html',
                           resultados=resultados, placa=placa)
