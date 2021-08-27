from flask import Flask, request
from controlador.principial import metodoPrincipal


def pruebaModo(entrada):
    return metodoPrincipal(entrada)


app = Flask(__name__)


@app.route("/interpretar", methods=['GET', 'POST'])
def interpretar():
    if request.method == "POST":
        cuerpo = request.get_json()
        salida = cuerpo['peticion']
        return pruebaModo(salida)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
