from flask import Flask, request
from flask_cors import CORS
from controlador.principial import metodoPrincipal
from flask import jsonify


app = Flask(__name__)
CORS(app)


@app.route("/", methods=['GET'])
def index():
    return 'OK!'


@app.route("/interpretar", methods=['GET', 'POST'])
def interpretar():
    if request.method == "POST":
        cuerpo = request.get_json()
        salida = cuerpo['peticion']
        response = jsonify(metodoPrincipal(salida))
        response.status_code = 200
        return response


if __name__ == "__main__":
    app.run()
