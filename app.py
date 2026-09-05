from flask import Flask, render_template
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
                        "dia_turno": datos[3]
                    }

                    colaborador["edad"] = calcular_edad(datos[2])
                    colaboradores.append(colaborador)

    return colaboradores


# Pagina de bienvenida
@app.route("/")
@app.route("/base")
def inicio():
    return render_template("base.html")


# Pagina de colaboradores
@app.route("/colaboradores")
def colaboradores():
    lista = cargar_colaboradores()

    return render_template(
        "colaboradores.html",
        colaboradores=lista
    )


if __name__ == "__main__":
    app.run(debug=True)