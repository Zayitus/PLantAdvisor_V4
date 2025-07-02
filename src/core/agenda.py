from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import copy

class EstrategiaConflictResolution(Enum):
    ESPECIFICIDAD = "especificidad"
    RECENCIA = "recencia"
    PRIORIDAD_EXPLICITA = "prioridad"

@dataclass
class ReglaInstanciada:
    regla_id: str
    bindings: Dict[str, Any]
    hechos_activadores: List[str]
    timestamp_activacion: datetime = field(default_factory=datetime.now)
    especificidad: int = 0
    prioridad_explicita: float = 0.0
    ya_ejecutada: bool = False

class Agenda:
    def __init__(self, estrategia: EstrategiaConflictResolution = EstrategiaConflictResolution.ESPECIFICIDAD):
        self._reglas_instanciadas: List[ReglaInstanciada] = []
        self._estrategia = estrategia
        self._historial_ejecucion: List[ReglaInstanciada] = []
        print(f"📋 Agenda Inicializada con estrategia: {estrategia.value}")

    def activar_regla(self, regla_id: str, bindings: Dict[str, Any], hechos_activadores: List[str], especificidad: int, prioridad_explicita: float):
        instancia = ReglaInstanciada(regla_id, copy.deepcopy(bindings), hechos_activadores, especificidad=especificidad, prioridad_explicita=prioridad_explicita)
        self._reglas_instanciadas.append(instancia)
        print(f"⚡ REGLA ACTIVADA: {regla_id}")

    def seleccionar_proxima_regla(self) -> Optional[ReglaInstanciada]:
        candidatos = [r for r in self._reglas_instanciadas if not r.ya_ejecutada]
        if not candidatos:
            return None

        if self._estrategia == EstrategiaConflictResolution.ESPECIFICIDAD:
            seleccionada = max(candidatos, key=lambda r: r.especificidad)
        elif self._estrategia == EstrategiaConflictResolution.RECENCIA:
            seleccionada = max(candidatos, key=lambda r: r.timestamp_activacion)
        else: # PRIORIDAD_EXPLICITA
            seleccionada = max(candidatos, key=lambda r: r.prioridad_explicita)
        
        print(f"✅ REGLA SELECCIONADA: {seleccionada.regla_id} por {self._estrategia.name}")
        return seleccionada

    def marcar_como_ejecutada(self, regla_instanciada: ReglaInstanciada):
        regla_instanciada.ya_ejecutada = True
        self._historial_ejecucion.append(regla_instanciada)

    def esta_vacia(self) -> bool:
        return all(r.ya_ejecutada for r in self._reglas_instanciadas)

    def limpiar_agenda(self):
        self.__init__(self._estrategia)
        print("🧹 Agenda Limpiada")