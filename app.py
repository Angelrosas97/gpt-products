from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

# Ruta para la URL raíz
@app.route('/')
def index():
    return "Bienvenido a la aplicación de tendencias de Google!"

@app.route('/google-trends', methods=['POST'])
def google_trends():
    data = request.get_json()
    palabras_clave = data['palabras_clave']
    pytrends = TrendReq(hl='es-MX', tz=360)
    pytrends.build_payload(palabras_clave, cat=0, timeframe='today 12-m', geo='MX', gprop='')
    tendencias = pytrends.interest_over_time()
    if not tendencias.empty:
        result = tendencias.reset_index().to_dict(orient='records')
    else:
        result = []
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
