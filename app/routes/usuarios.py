from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import usuario as M
from app.models import celda as CM

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/')
def index():
    q = request.args.get('q', '').strip()
    lista = M.buscar(q) if q else M.obtener_todos()
    return render_template('usuarios/index.html', usuarios=lista, busqueda=q)


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        cedula        = request.form.get('cedula', '').strip()
        nombre        = request.form.get('nombre', '').strip()
        telefono      = request.form.get('telefono', '').strip()
        correo        = request.form.get('correo', '').strip()
        tipo_vehiculo = request.form.get('tipo_vehiculo', '').strip()
        placa         = request.form.get('placa', '').strip().upper()
        celda_id      = request.form.get('celda_id', '').strip()

        if not all([cedula, nombre, telefono, tipo_vehiculo, placa]):
            flash('Completa todos los campos obligatorios.', 'danger')
            return redirect(url_for('usuarios.nuevo'))

        if M.existe_cedula(cedula):
            flash('Ya existe un usuario con esa cedula.', 'danger')
            return redirect(url_for('usuarios.nuevo'))

        if M.existe_placa(placa):
            flash('Ya existe un usuario con esa placa.', 'danger')
            return redirect(url_for('usuarios.nuevo'))

        if not CM.hay_disponibles(tipo_vehiculo):
            flash('No hay celdas disponibles para ese tipo de vehiculo.', 'danger')
            return redirect(url_for('usuarios.nuevo'))

        try:
            nuevo_id = M.registrar(cedula, nombre, telefono, correo, tipo_vehiculo, placa)
            if not nuevo_id:
                flash('Error al registrar el usuario.', 'danger')
                return redirect(url_for('usuarios.nuevo'))

            # Asignar celda
            if celda_id and celda_id.isdigit():
                CM.asignar(int(celda_id), nuevo_id)
            else:
                libres = CM.obtener_libres(tipo_vehiculo)
                if libres:
                    CM.asignar(libres[0]['id'], nuevo_id)

            flash(f'Usuario {nombre} registrado correctamente.', 'success')
            return redirect(url_for('usuarios.index'))

        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('usuarios.nuevo'))

    return render_template('usuarios/nuevo.html',
                           celdas_auto=CM.obtener_libres('auto'),
                           celdas_moto=CM.obtener_libres('moto'))


@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = M.obtener_por_id(id)
    if not usuario:
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('usuarios.index'))

    if request.method == 'POST':
        nombre   = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip()
        correo   = request.form.get('correo', '').strip()
        placa    = request.form.get('placa', '').strip().upper()

        if not all([nombre, telefono, placa]):
            flash('Nombre, telefono y placa son obligatorios.', 'danger')
            return redirect(url_for('usuarios.editar', id=id))

        if M.existe_placa(placa, excluir_id=id):
            flash('Esa placa ya pertenece a otro usuario.', 'danger')
            return redirect(url_for('usuarios.editar', id=id))

        M.actualizar(id, nombre, telefono, correo, placa)
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuarios.index'))

    return render_template('usuarios/editar.html', usuario=usuario)


@usuarios_bp.route('/inactivar/<int:id>', methods=['POST'])
def inactivar(id):
    usuario = M.obtener_por_id(id)
    if usuario:
        M.inactivar(id)
        flash(f'Usuario {usuario["nombre"]} inactivado. Celda liberada.', 'success')
    return redirect(url_for('usuarios.index'))


@usuarios_bp.route('/api/celdas/<tipo>')
def api_celdas(tipo):
    return jsonify(CM.obtener_libres(tipo))
