
from flask import abort
from mysql.connector import IntegrityError
from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_connection

asignaturas_bp = Blueprint(
    "asignaturas",
    __name__,
    url_prefix="/asignaturas"
)


@asignaturas_bp.route("/")
def listar():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.id_asignatura,
               a.nombre,
               a.descripcion,
               a.nivel,
               d.nombre AS nombre_docente,
               d.apellido AS apellido_docente
        FROM asignaturas a
        INNER JOIN docentes d
            ON a.id_docente = d.id_docente
        ORDER BY a.nombre
    """)

    asignaturas = cursor.fetchall()
    cursor.close()
    conexion.close()

    return render_template(
        "asignaturas/listar.html",
        asignaturas=asignaturas
    )


@asignaturas_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM asignaturas
            WHERE id_asignatura = %s
        """, (id,))
        asignatura = cursor.fetchone()

        if asignatura is None:
            abort(404)

        if request.method == "POST":
            nombre = request.form.get("nombre", "").strip()
            descripcion = request.form.get("descripcion", "").strip()
            nivel = request.form.get("nivel", "").strip()
            id_docente = request.form.get("id_docente", type=int)

            if not nombre or not id_docente:
                flash("Nombre y docente son obligatorios.", "danger")
            else:
                try:
                    cursor.execute("""
                        UPDATE asignaturas
                        SET nombre = %s,
                            descripcion = %s,
                            nivel = %s,
                            id_docente = %s
                        WHERE id_asignatura = %s
                    """, (
                        nombre, descripcion or None,
                        nivel or None, id_docente, id
                    ))
                    conexion.commit()
                    flash("Asignatura actualizada.", "success")
                    return redirect(url_for("asignaturas.listar"))

                except IntegrityError:
                    conexion.rollback()
                    flash(
                        "La asignatura está duplicada para ese docente "
                        "o el docente seleccionado no existe.",
                        "danger"
                    )

        cursor.execute("""
            SELECT id_docente, nombre, apellido
            FROM docentes
            WHERE estado = 'Activo'
               OR id_docente = %s
            ORDER BY apellido, nombre
        """, (asignatura["id_docente"],))
        docentes = cursor.fetchall()

        return render_template(
            "asignaturas/formulario.html",
            asignatura=asignatura,
            docentes=docentes
        )
    finally:
        cursor.close()
        conexion.close()



@asignaturas_bp.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            DELETE FROM asignaturas
            WHERE id_asignatura = %s
        """, (id,))

        if cursor.rowcount == 0:
            abort(404)

        conexion.commit()
        flash(
            "Asignatura eliminada. Sus notas asociadas también "
            "se eliminaron.",
            "success"
        )
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("asignaturas.listar"))



@asignaturas_bp.route("/nueva", methods=["GET", "POST"])
def nueva():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form.get("descripcion", "").strip()
        nivel = request.form.get("nivel", "").strip()
        id_docente = request.form["id_docente"]

        try:
            cursor.execute("""
                INSERT INTO asignaturas
                    (nombre, descripcion, nivel, id_docente)
                VALUES (%s, %s, %s, %s)
            """, (
                nombre,
                descripcion or None,
                nivel or None,
                id_docente
            ))

            conexion.commit()
            flash("Asignatura registrada correctamente.", "success")
            return redirect(url_for("asignaturas.listar"))

        except Exception:
            conexion.rollback()
            flash(
                "No se pudo registrar la asignatura. "
                "Verifica los datos y que no esté duplicada.",
                "danger"
            )

    cursor.execute("""
        SELECT id_docente, nombre, apellido
        FROM docentes
        WHERE estado = 'Activo'
        ORDER BY apellido, nombre
    """)
    docentes = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "asignaturas/formulario.html",
        docentes=docentes,
        asignatura=None
    )

