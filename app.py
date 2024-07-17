from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/')
def index():
    return "Bienvenido a la aplicación de tendencias de Google!"

@app.route('/google-trends', methods=['POST'])
def google_trends():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid input: No JSON payload received"}), 400
        if 'palabras_clave' not in data:
            return jsonify({"error": "Invalid input: 'palabras_clave' field is missing"}), 400
        
        palabras_clave = data['palabras_clave']
        if not isinstance(palabras_clave, list) or not all(isinstance(item, str) for item in palabras_clave):
            return jsonify({"error": "Invalid input: 'palabras_clave' must be a list of strings"}), 400
        
        pytrends = TrendReq(hl='es-MX', tz=360)
        pytrends.build_payload(palabras_clave, cat=0, timeframe='today 12-m', geo='MX', gprop='')
        tendencias = pytrends.interest_over_time()
        
        if tendencias.empty:
            return jsonify({"message": "No trends data available for the given keywords"}), 200
        
        result = tendencias.reset_index().to_dict(orient='records')
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
