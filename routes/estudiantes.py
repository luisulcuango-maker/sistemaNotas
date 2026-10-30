
from datetime import date
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, abort
)
from mysql.connector import IntegrityError
from db import get_connection

estudiantes_bp = Blueprint(
    "estudiantes",
    __name__,
    url_prefix="/estudiantes"
)


@estudiantes_bp.route("/")
def listar():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id_estudiante, cedula, nombre, apellido,
                   correo, fecha_nacimiento, estado, fecha_registro
            FROM estudiantes
            ORDER BY apellido, nombre
        """)
        estudiantes = cursor.fetchall()

        return render_template(
            "estudiantes/listar.html",
            estudiantes=estudiantes
        )
    finally:
        cursor.close()
        conexion.close()


@estudiantes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        cedula = request.form.get("cedula", "").strip()
        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        correo = request.form.get("correo", "").strip()
        fecha = request.form.get("fecha_nacimiento") or None
        estado = request.form.get("estado", "Activo")

        if not all([cedula, nombre, apellido, correo]):
            flash("Completa todos los campos obligatorios.", "danger")
            return render_template(
                "estudiantes/formulario.html",
                estudiante=None
            )

        if estado not in ("Activo", "Inactivo"):
            abort(400)

        try:
            fecha_validada = (
                date.fromisoformat(fecha) if fecha else None
            )
        except ValueError:
            flash("La fecha de nacimiento no es válida.", "danger")
            return render_template(
                "estudiantes/formulario.html",
                estudiante=None
            )

        conexion = get_connection()
        cursor = conexion.cursor()

        try:
            cursor.execute("""
                INSERT INTO estudiantes
                    (cedula, nombre, apellido, correo,
                     fecha_nacimiento, estado)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                cedula, nombre, apellido, correo,
                fecha_validada, estado
            ))
            conexion.commit()
            flash("Estudiante registrado correctamente.", "success")
            return redirect(url_for("estudiantes.listar"))

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
        "estudiantes/formulario.html",
        estudiante=None
    )


@estudiantes_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM estudiantes
            WHERE id_estudiante = %s
        """, (id,))
        estudiante = cursor.fetchone()

        if estudiante is None:
            abort(404)

        if request.method == "POST":
            cedula = request.form.get("cedula", "").strip()
            nombre = request.form.get("nombre", "").strip()
            apellido = request.form.get("apellido", "").strip()
            correo = request.form.get("correo", "").strip()
            fecha = request.form.get("fecha_nacimiento") or None
            estado = request.form.get("estado", "Activo")

            if not all([cedula, nombre, apellido, correo]):
                flash("Completa todos los campos obligatorios.", "danger")
                return render_template(
                    "estudiantes/formulario.html",
                    estudiante=estudiante
                )

            if estado not in ("Activo", "Inactivo"):
                abort(400)

            try:
                fecha_validada = (
                    date.fromisoformat(fecha) if fecha else None
                )
            except ValueError:
                flash("La fecha no es válida.", "danger")
                return render_template(
                    "estudiantes/formulario.html",
                    estudiante=estudiante
                )

            try:
                cursor.execute("""
                    UPDATE estudiantes
                    SET cedula = %s, nombre = %s,
                        apellido = %s, correo = %s,
                        fecha_nacimiento = %s, estado = %s
                    WHERE id_estudiante = %s
                """, (
                    cedula, nombre, apellido, correo,
                    fecha_validada, estado, id
                ))
                conexion.commit()
                flash("Estudiante actualizado correctamente.", "success")
                return redirect(url_for("estudiantes.listar"))

            except IntegrityError:
                conexion.rollback()
                flash(
                    "La cédula o el correo pertenecen a otro estudiante.",
                    "danger"
                )

        return render_template(
            "estudiantes/formulario.html",
            estudiante=estudiante
        )
    finally:
        cursor.close()
        conexion.close()


@estudiantes_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            DELETE FROM estudiantes
            WHERE id_estudiante = %s
        """, (id,))

        if cursor.rowcount == 0:
            abort(404)

        conexion.commit()
        flash("Estudiante eliminado correctamente.", "success")

    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("estudiantes.listar"))
