from flask import Flask
from controlador.principial import metodoPrincipal


def pruebaModo(entrada):
    return metodoPrincipal(entrada)


app = Flask(__name__)


@app.route("/interpretar")
def hello():
    return pruebaModo("aca va a ir el texto de entrada")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
