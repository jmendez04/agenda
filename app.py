from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)


def calcular_edad(fecha_nacimiento):
    fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date()
    hoy = datetime.now().date()

    edad = hoy.year - fecha.year

    if (hoy.month, hoy.day) < (fecha.month, fecha.day):
        edad -= 1

    return edad


def cargar_colaboradores():
    colaboradores = []

    if os.path.exists("colaboradores.txt"):
        with open("colaboradores.txt", "r", encoding="utf-8") as archivo:

            for linea in archivo:
                datos = linea.strip().split("|")

                if len(datos) == 4:
                    colaborador = {
                        "nombre": datos[0],
                        "apellido": datos[1],
                        "fecha_nacimiento": datos[2],
                        "dia_semana": datos[3]
                    }

                    colaborador["edad"] = calcular_edad(
                        colaborador["fecha_nacimiento"]
                    )

                    colaboradores.append(colaborador)

    return colaboradores


def contar_por_dia(colaboradores):
    resumen = {
        "Lunes": 0,
        "Martes": 0,
        "Miércoles": 0,
        "Jueves": 0,
        "Viernes": 0,
        "Sábado": 0,
        "Domingo": 0
    }

    for colaborador in colaboradores:
        dia = colaborador["dia_semana"]

        if dia in resumen:
            resumen[dia] += 1

    return resumen


# Pagina de bienvenida
@app.route("/")
@app.route("/base")
def inicio():
    return render_template("base.html")


# Pagina de registro
@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form.get("nombre", "").strip()
        apellido = request.form.get("apellido", "").strip()
        fecha_nacimiento = request.form.get("fecha_nacimiento", "")
        dia_semana = request.form.get("dia_semana", "")

        if nombre == "" or apellido == "" or fecha_nacimiento == "" or dia_semana == "":
            return render_template(
                "registro.html",
                error="Todos los campos son obligatorios."
            )

        colaborador = {
            "nombre": nombre,
            "apellido": apellido,
            "fecha_nacimiento": fecha_nacimiento,
            "dia_semana": dia_semana
        }

        with open("colaboradores.txt", "a", encoding="utf-8") as archivo:
            archivo.write(
                f"{colaborador['nombre']}|"
                f"{colaborador['apellido']}|"
                f"{colaborador['fecha_nacimiento']}|"
                f"{colaborador['dia_semana']}\n"
            )

        return redirect(url_for("colaboradores"))

    return render_template("registro.html")


# Pagina de colaboradores
@app.route("/colaboradores")
def colaboradores():

    lista = cargar_colaboradores()

    return render_template(
        "colaboradores.html",
        colaboradores=lista
    )


# Pagina de resumen
@app.route("/resumen")
def resumen():

    lista = cargar_colaboradores()
    resumen_dias = contar_por_dia(lista)

    return render_template(
        "resumen.html",
        resumen=resumen_dias
    )


if __name__ == "__main__":
    app.run(debug=True)