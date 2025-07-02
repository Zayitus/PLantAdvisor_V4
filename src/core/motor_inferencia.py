from typing import Protocol, List, Optional, Callable
from .memoria_trabajo import MemoriaTrabajo, TipoHecho
from .agenda import Agenda
from .sintaxis_reglas import ReglaProduccionAcademica
from ..knowledge.parser_reglas import ParserReglasAcademico 

class BaseConocimiento(Protocol):
    def obtener_reglas(self) -> List[ReglaProduccionAcademica]: ...
    def obtener_regla_por_id(self, regla_id: str) -> Optional[ReglaProduccionAcademica]: ...

class MotorInferenciaAcademico:
    """Orquesta el ciclo de inferencia completo."""
    def __init__(self, memoria: MemoriaTrabajo, agenda: Agenda, parser: ParserReglasAcademico, max_ciclos: int = 10):
        self.memoria = memoria
        self.agenda = agenda
        self.parser = parser
        self.max_ciclos = max_ciclos
        self.razon_terminacion = ""
        self.ciclos_ejecutados = 0
        print("🧠 Motor de Inferencia Inicializado")

    def inferir(self, base_conocimiento: BaseConocimiento):
        """
        Ejecuta el ciclo completo de inferencia: Match, Conflict-Resolution, Act.
        """
        print("\n🚀 INICIANDO INFERENCIA...")
        self.ciclos_ejecutados = 0
        
        # --- LÓGICA DEL BUCLE MODIFICADA ---
        # El motor ahora continuará hasta que la agenda esté vacía o se alcance el límite de ciclos,
        # permitiendo que se generen múltiples conclusiones.
        while self.ciclos_ejecutados < self.max_ciclos:
            self.ciclos_ejecutados += 1
            print(f"\n--- CICLO DE INFERENCIA {self.ciclos_ejecutados} ---")

            print("1. FASE MATCH: Buscando reglas aplicables...")
            reglas_activadas_este_ciclo = 0
            for regla in base_conocimiento.obtener_reglas():
                resultado_eval = self.parser.evaluar_regla(regla)
                if resultado_eval:
                    # La lógica para no reactivar reglas ya está en la Agenda
                    self.agenda.activar_regla(
                        regla_id=regla.id,
                        bindings=resultado_eval['bindings'],
                        hechos_activadores=[], 
                        especificidad=regla.especificidad,
                        prioridad_explicita=regla.prioridad
                    )
                    reglas_activadas_este_ciclo +=1
            
            print("2. FASE CONFLICT RESOLUTION: Seleccionando la mejor regla...")
            regla_instanciada = self.agenda.seleccionar_proxima_regla()
            
            if not regla_instanciada:
                self.razon_terminacion = "Agenda vacía - no hay más reglas para ejecutar."
                break

            print("3. FASE ACT: Ejecutando acciones de la regla...")
            regla_a_ejecutar = base_conocimiento.obtener_regla_por_id(regla_instanciada.regla_id)
            if regla_a_ejecutar:
                self.parser.ejecutar_acciones(regla_a_ejecutar, regla_instanciada.bindings)
                self.agenda.marcar_como_ejecutada(regla_instanciada)
        
        if self.ciclos_ejecutados >= self.max_ciclos:
            self.razon_terminacion = f"Límite de ciclos ({self.max_ciclos}) alcanzado."
            
        print(f"🏁 Inferencia terminada: {self.razon_terminacion}")
