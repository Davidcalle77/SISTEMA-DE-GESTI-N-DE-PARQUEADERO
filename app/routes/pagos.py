from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import pago as PM
from app.models import usuario as UM

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')


@pagos_bp.route('/')
def index():
    return render_template('pagos/index.html',
                           pagos=PM.obtener_todos(),
                           usuarios=UM.obtener_todos(),
                           resumen=PM.resumen())


@pagos_bp.route('/registrar', methods=['POST'])
def registrar():
    usuario_id  = request.form.get('usuario_id', '').strip()
    monto       = request.form.get('monto', '').strip()
    mes_pagado  = request.form.get('mes_pagado', '').strip()
    observacion = request.form.get('observacion', '').strip()

    if not all([usuario_id, monto, mes_pagado]):
        flash('Usuario, monto y mes son obligatorios.', 'danger')
        return redirect(url_for('pagos.index'))

    try:
        monto_float = float(monto)
        if monto_float <= 0:
            raise ValueError
    except ValueError:
        flash('El monto debe ser un numero mayor a cero.', 'danger')
        return redirect(url_for('pagos.index'))

    PM.registrar(int(usuario_id), monto_float, mes_pagado, observacion)
    flash('Pago registrado correctamente.', 'success')
    return redirect(url_for('pagos.index'))


@pagos_bp.route('/pendientes')
def pendientes():
    return render_template('pagos/pendientes.html',
                           usuarios=PM.estado_por_usuario())
