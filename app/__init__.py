from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = os.getenv('SECRET_KEY', 'parqueadero2025')

    from app.routes.usuarios import usuarios_bp
    from app.routes.celdas   import celdas_bp
    from app.routes.entradas import entradas_bp
    from app.routes.pagos    import pagos_bp

    app.register_blueprint(usuarios_bp)
    app.register_blueprint(celdas_bp)
    app.register_blueprint(entradas_bp)
    app.register_blueprint(pagos_bp)

    @app.route('/')
    def dashboard():
        from app.models.celda   import reporte
        from app.models.usuario import obtener_todos
        from app.models.entrada import obtener_historial
        rep      = reporte()
        usuarios = obtener_todos()
        historial = obtener_historial(5)
        return render_template('dashboard.html',
                               reporte=rep,
                               total_usuarios=len(usuarios),
                               historial=historial)

    return app
