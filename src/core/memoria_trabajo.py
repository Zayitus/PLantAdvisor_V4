from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from .sintaxis_reglas import TipoHecho

@dataclass
class Hecho:
    """Representa una unidad de información en la memoria de trabajo."""
    id: str
    predicado: str
    valor: Any
    tipo: TipoHecho
    origen: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    justificacion: str = ""
    confianza: float = 1.0

class MemoriaTrabajo:
    """Almacena y gestiona los hechos del sistema."""
    def __init__(self):
        self._hechos: Dict[str, Hecho] = {}
        self._indice_por_predicado: Dict[str, Set[str]] = {}
        self._indice_por_tipo: Dict[TipoHecho, Set[str]] = {t: set() for t in TipoHecho}
        self._contador_hechos = 0
        print("🧠 Memoria de Trabajo Inicializada")

    def _generar_id_hecho(self) -> str:
        self._contador_hechos += 1
        return f"F{self._contador_hechos:04d}"

    def assert_hecho(self, predicado: str, valor: Any, tipo: TipoHecho, origen: Optional[str] = None, justificacion: str = "", confianza: float = 1.0) -> str:
        hecho_id = self._generar_id_hecho()
        hecho = Hecho(hecho_id, predicado, valor, tipo, origen, justificacion=justificacion, confianza=confianza)
        self._hechos[hecho.id] = hecho
        self._indice_por_predicado.setdefault(hecho.predicado, set()).add(hecho.id)
        self._indice_por_tipo[hecho.tipo].add(hecho.id)
        print(f"   [Memoria] Hecho {tipo.name} agregado: {predicado} = {valor}")
        return hecho_id

    def obtener_hecho(self, predicado: str) -> Optional[Hecho]:
        hechos_ids = self._indice_por_predicado.get(predicado, set())
        if not hechos_ids:
            return None
        return max((self._hechos[hid] for hid in hechos_ids), key=lambda h: h.timestamp)
    
    def obtener_hechos_por_tipo(self, tipo: TipoHecho) -> List[Hecho]:
        """Obtiene una lista de hechos de un tipo específico."""
        ids = self._indice_por_tipo.get(tipo, set())
        return [self._hechos[id] for id in ids]

    def limpiar_memoria(self):
        self._hechos.clear()
        self._indice_por_predicado.clear()
        self._indice_por_tipo = {t: set() for t in TipoHecho}
        self._contador_hechos = 0
        print("🧹 Memoria de Trabajo Limpiada")

    def generar_trace_explicacion(self) -> Dict[str, Any]:
        hechos_serializados = []
        for h in self._hechos.values():
            hecho_dict = h.__dict__.copy()
            hecho_dict['tipo'] = h.tipo.value 
            hecho_dict['timestamp'] = h.timestamp.isoformat()
            hechos_serializados.append(hecho_dict)

        return {
            'total_hechos': len(self._hechos),
            'hechos_por_tipo': {t.value: len(s) for t, s in self._indice_por_tipo.items()},
            'hechos': hechos_serializados
        }