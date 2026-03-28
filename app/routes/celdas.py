from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import celda as CM

from app.models.pago import calcular_pago

celdas_bp = Blueprint("celdas", __name__, url_prefix="/celdas")


@celdas_bp.route("/pago/<int:id>")
def ver_pago(id):
    total = calcular_pago(id)
    return f"Total a pagar: ${total}"


@celdas_bp.route("/")
def index():
    return render_template(
        "celdas/index.html", celdas=CM.obtener_todas(), reporte=CM.reporte()
    )


@celdas_bp.route("/api/mapa")
def api_mapa():
    return jsonify(CM.obtener_todas())


@celdas_bp.route("/liberar/<int:id>", methods=["POST"])
def liberar(id):
    celda = CM.obtener_por_id(id)
    if not celda:
        flash("Celda no encontrada.", "danger")
        return redirect(url_for("celdas.index"))
    CM.liberar(id)
    flash(f'Celda {celda["codigo"]} liberada correctamente.', "success")
    return redirect(url_for("celdas.index"))


@celdas_bp.route("/mantenimiento/<int:id>", methods=["POST"])
def mantenimiento(id):
    celda = CM.obtener_por_id(id)
    if not celda:
        flash("Celda no encontrada.", "danger")
        return redirect(url_for("celdas.index"))

    if celda["estado"] == "ocupada":
        flash("La celda esta ocupada. Inactiva el usuario primero.", "danger")
        return redirect(url_for("celdas.index"))

    motivo = request.form.get("motivo", "").strip()
    fecha_fin = request.form.get("fecha_fin", "").strip() or None

    if not motivo:
        flash("Debes ingresar el motivo del mantenimiento.", "danger")
        return redirect(url_for("celdas.index"))

    CM.poner_mantenimiento(id, motivo, fecha_fin)
    flash(f'Celda {celda["codigo"]} puesta en mantenimiento.', "warning")
    return redirect(url_for("celdas.index"))
