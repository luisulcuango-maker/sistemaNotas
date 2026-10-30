
import os
from flask import Flask

from routes.estudiantes import estudiantes_bp
from routes.docentes import docentes_bp
from routes.asignaturas import asignaturas_bp
from routes.notas import notas_bp


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "clave-desarrollo-temporal"
    )

    app.register_blueprint(estudiantes_bp)
    app.register_blueprint(docentes_bp)
    app.register_blueprint(asignaturas_bp)
    app.register_blueprint(notas_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
