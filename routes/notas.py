
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, abort
)
from mysql.connector import IntegrityError
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection

notas_bp = Blueprint("notas", __name__, url_prefix="/notas")


@notas_bp.route("/")
def listar():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT n.id_nota,
               e.cedula,
               e.nombre AS nombre_estudiante,
               e.apellido AS apellido_estudiante,
               a.nombre AS nombre_asignatura,
               n.nota1,
               n.nota2,
               n.examen,
               n.promedio,
               n.observacion,
               n.fecha_actualizacion
        FROM notas n
        INNER JOIN estudiantes e
            ON n.id_estudiante = e.id_estudiante
        INNER JOIN asignaturas a
            ON n.id_asignatura = a.id_asignatura
        ORDER BY e.apellido, e.nombre, a.nombre
    """)

    notas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template("notas/listar.html", notas=notas)


@notas_bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        try:
            id_estudiante = int(request.form["id_estudiante"])
            id_asignatura = int(request.form["id_asignatura"])
            nota1 = float(request.form["nota1"])
            nota2 = float(request.form["nota2"])
            examen = float(request.form["examen"])
            observacion = request.form.get(
                "observacion", ""
            ).strip()

            if any(
                not 0 <= nota <= 10
                for nota in (nota1, nota2, examen)
            ):
                raise ValueError("Las notas deben estar entre 0 y 10.")

            cursor.execute("""
                INSERT INTO notas (
                    id_estudiante, id_asignatura,
                    nota1, nota2, examen, observacion
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_estudiante, id_asignatura,
                nota1, nota2, examen, observacion or None
            ))

            conexion.commit()
            flash("Notas registradas correctamente.", "success")
            return redirect(url_for("notas.listar"))

        except ValueError as error:
            conexion.rollback()
            flash(str(error), "danger")

        except Exception:
            conexion.rollback()
            flash(
                "No se pudieron guardar las notas. "
                "Verifica los datos y que no exista "
                "una nota para ese estudiante y asignatura.",
                "danger"
            )

    cursor.execute("""
        SELECT id_estudiante, cedula, nombre, apellido
        FROM estudiantes
        WHERE estado = 'Activo'
        ORDER BY apellido, nombre
    """)
    estudiantes = cursor.fetchall()

    cursor.execute("""
        SELECT id_asignatura, nombre
        FROM asignaturas
        ORDER BY nombre
    """)
    asignaturas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "notas/formulario.html",
        estudiantes=estudiantes,
        asignaturas=asignaturas
    )


@notas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM notas WHERE id_nota = %s
        """, (id,))
        nota = cursor.fetchone()

        if nota is None:
            abort(404)

        if request.method == "POST":
            try:
                nota1 = float(request.form["nota1"])
                nota2 = float(request.form["nota2"])
                examen = float(request.form["examen"])
                observacion = request.form.get(
                    "observacion", ""
                ).strip()

                valores = (nota1, nota2, examen)

                if any(
                    not 0 <= valor <= 10
                    for valor in valores
                ):
                    raise ValueError(
                        "Las calificaciones deben estar entre 0 y 10."
                    )

                cursor.execute("""
                    UPDATE notas
                    SET nota1 = %s,
                        nota2 = %s,
                        examen = %s,
                        observacion = %s
                    WHERE id_nota = %s
                """, (
                    nota1, nota2, examen,
                    observacion or None, id
                ))

                conexion.commit()
                flash("Notas actualizadas correctamente.", "success")
                return redirect(url_for("notas.listar"))

            except ValueError as error:
                conexion.rollback()
                flash(str(error), "danger")

        return render_template(
            "notas/formulario.html",
            nota=nota,
            estudiantes=[],
            asignaturas=[]
        )
    finally:
        cursor.close()
        conexion.close()

@notas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            DELETE FROM notas WHERE id_nota = %s
        """, (id,))

        if cursor.rowcount == 0:
            abort(404)

        conexion.commit()
        flash("Nota eliminada correctamente.", "success")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("notas.listar"))

