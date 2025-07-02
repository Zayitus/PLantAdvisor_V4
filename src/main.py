import sys
import os

# Añadir el directorio raíz del proyecto al path para poder importar 'src'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sistema_experto import SistemaExpertoPlantaTDF

def main_cli():
    """Punto de entrada para la demostración en línea de comandos."""
    sistema = SistemaExpertoPlantaTDF()

    caso_prueba = {
        'ubicacion_usuario': 'interior',
        'calefaccion_nivel': 'alta',
        'mascotas_presentes': False
    }
    
    trace = sistema.consultar(caso_prueba)

    print("\n📊 RESULTADOS FINALES DE LA CONSULTA (CLI)")
    print("="*50)
    print(f"Total de hechos en memoria: {trace['total_hechos']}")
    
    conclusiones = [h for h in trace['hechos'] if h['tipo'] == 'CONCLUSION']
    if conclusiones:
        print("\n🎯 Conclusiones alcanzadas:")
        for c in conclusiones:
            print(f"  - {c['predicado']}: {c['valor']} (Confianza: {c['confianza']:.2f})")
    else:
        print("\n❌ No se alcanzaron conclusiones finales.")
        
    derivados = [h for h in trace['hechos'] if h['tipo'] == 'DERIVADO']
    if derivados:
        print("\n🧠 Hechos derivados durante la inferencia:")
        for d in derivados:
            print(f"  - {d['predicado']}: {d['valor']} (Derivado por: {d['origen']})")

if __name__ == "__main__":
    main_cli()

