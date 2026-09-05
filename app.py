from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def inicio():
    return redirect(url_for("registro"))


@app.route("/registro", methods=["GET", "POST"])
def registro():
    return render_template("registro.html")


@app.route("/colaboradores")
def colaboradores():
    return render_template("colaboradores.html")


@app.route("/resumen")
def resumen():
    return render_template("resumen.html")


if __name__ == "__main__":
    app.run(debug=True)