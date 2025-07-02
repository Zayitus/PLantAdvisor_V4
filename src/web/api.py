import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.sistema_experto import SistemaExpertoPlantaTDF

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app = Flask(__name__,
            static_folder=os.path.join(project_root, 'src/web/static'),
            template_folder=os.path.join(project_root, 'src/web/templates'))
CORS(app)

try:
    sistema_experto = SistemaExpertoPlantaTDF()
except Exception as e:
    print(f"FATAL: Error al inicializar el sistema experto: {e}")
    sistema_experto = None

@app.route('/')
def serve_index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/api/consulta', methods=['POST'])
def consultar():
    if not sistema_experto:
        return jsonify({"error": "El sistema experto no está disponible."}), 500

    print("\n--- Petición a /api/consulta recibida ---")
    datos_usuario = request.json
    if not datos_usuario:
        return jsonify({"error": "No se recibieron datos en la petición."}), 400

    for key, value in datos_usuario.items():
        if isinstance(value, str):
            if value.lower() == 'true': datos_usuario[key] = True
            elif value.lower() == 'false': datos_usuario[key] = False
    
    try:
        resultado_trace = sistema_experto.consultar(datos_usuario)
        
        # --- CORRECCIÓN FINAL ---
        # Con la serialización correcta en memoria_trabajo.py, esta comparación
        # ahora funcionará como se espera.
        conclusiones = [h for h in resultado_trace.get('hechos', []) if h.get('tipo') == 'conclusion']
        hechos_derivados = [h for h in resultado_trace.get('hechos', []) if h.get('tipo') == 'derivado']

        respuesta = {
            "conclusiones": conclusiones,
            "hechos_derivados": hechos_derivados,
            "mensaje": "Consulta procesada exitosamente."
        }
        return jsonify(respuesta)

    except Exception as e:
        print(f"Error durante la consulta: {e}")
        return jsonify({"error": f"Ocurrió un error interno: {str(e)}"}), 500