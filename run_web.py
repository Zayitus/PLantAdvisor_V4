# Este archivo ahora es mucho más simple. Su única responsabilidad
# es importar la aplicación 'app' ya configurada desde api.py y ejecutarla.
from src.web.api import app

if __name__ == '__main__':
    print("🚀 Lanzando la aplicación web PlantAdvisor-TDF...")
    print("✅ Servidor iniciado. Abre tu navegador y ve a http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
