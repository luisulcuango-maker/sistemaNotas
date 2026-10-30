
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, abort
)
from mysql.connector import IntegrityError
from db import get_connection

docentes_bp = Blueprint(
    "docentes", __name__, url_prefix="/docentes"
)


@docentes_bp.route("/")
def listar():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id_docente, cedula, nombre, apellido,
                   correo, especialidad, estado
            FROM docentes
            ORDER BY apellido, nombre
        """)
        docentes = cursor.fetchall()

        return render_template(
            "docentes/listar.html", docentes=docentes
        )
    finally:
        cursor.close()
        conexion.close()


@docentes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        cedula = request.form.get("cedula", "").strip()
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        correo = request.form.get("correo", "").strip()
        especialidad = request.form.get("especialidad", "").strip()
        estado = request.form.get("estado", "Activo")

        if not all([cedula, nombre, apellido, correo]):
            flash("Completa los campos obligatorios.", "danger")
            return render_template(
                "docentes/formulario.html", docente=None
            )

        if estado not in ("Activo", "Inactivo"):
            abort(400)

        conexion = get_connection()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO docentes
                    (cedula, nombre, apellido, correo,
                     especialidad, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                cedula, nombre, apellido, correo,
                especialidad or None, estado
            ))
            conexion.commit()
            flash("Docente registrado correctamente.", "success")
            return redirect(url_for("docentes.listar"))

        except IntegrityError:
            conexion.rollback()
            flash(
                "La cédula o el correo ya están registrados.",
                "danger"
            )
        finally:
            cursor.close()
            conexion.close()

    return render_template(
        "docentes/formulario.html", docente=None
    )


@docentes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM docentes WHERE id_docente = %s
        """, (id,))
        docente = cursor.fetchone()

        if docente is None:
            abort(404)

        if request.method == "POST":
            cedula = request.form.get("cedula", "").strip()
            nombre = request.form.get("nombre", "").strip()
            apellido = request.form.get("apellido", "").strip()
            correo = request.form.get("correo", "").strip()
            especialidad = request.form.get("especialidad", "").strip()
            estado = request.form.get("estado", "Activo")

            if not all([cedula, nombre, apellido, correo]):
                flash("Completa los campos obligatorios.", "danger")
                return render_template(
                    "docentes/formulario.html", docente=docente
                )

            if estado not in ("Activo", "Inactivo"):
                abort(400)

            try:
                cursor.execute("""
                    UPDATE docentes
                    SET cedula = %s, nombre = %s,
                        apellido = %s, correo = %s,
                        especialidad = %s, estado = %s
                    WHERE id_docente = %s
                """, (
                    cedula, nombre, apellido, correo,
                    especialidad or None, estado, id
                ))
                conexion.commit()
                flash("Docente actualizado correctamente.", "success")
                return redirect(url_for("docentes.listar"))

            except IntegrityError:
                conexion.rollback()
                flash(
                    "La cédula o el correo ya pertenecen a otro docente.",
                    "danger"
                )

        return render_template(
            "docentes/formulario.html", docente=docente
        )
    finally:
        cursor.close()
        conexion.close()


@docentes_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            DELETE FROM docentes WHERE id_docente = %s
        """, (id,))

        if cursor.rowcount == 0:
            abort(404)

        conexion.commit()
        flash("Docente eliminado correctamente.", "success")

    except IntegrityError:
        conexion.rollback()
        flash(
            "No se puede eliminar: el docente tiene asignaturas asociadas.",
            "danger"
        )
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("docentes.listar"))
