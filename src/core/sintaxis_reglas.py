from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# --- CORRECCIÓN AQUÍ ---
# La clase TipoHecho debe estar definida en este archivo para que otros
# módulos puedan importarla correctamente.
class TipoHecho(Enum):
    """Clasificación de hechos en la memoria de trabajo."""
    INICIAL = "inicial"
    DERIVADO = "derivado"
    CONCLUSION = "conclusion"

class OperadorCondicion(Enum):
    """Operadores para condiciones de reglas."""
    IGUAL = "=="
    DIFERENTE = "!="
    MENOR = "<"
    MENOR_IGUAL = "<="
    MAYOR = ">"
    MAYOR_IGUAL = ">="
    CONTIENE = "contains"
    EN = "in"
    NO_EN = "not_in"
    EXISTE = "exists"
    NO_EXISTE = "not_exists"
    COINCIDE_PATRON = "matches"

class TipoAccion(Enum):
    """Tipos de acciones en reglas."""
    ASSERT = "assert"
    RETRACT = "retract"
    MODIFY = "modify"
    CONCLUDE = "conclude"
    CALL_FUNCTION = "call"
    SET_VARIABLE = "set"
    INCREMENT = "increment"
    RECOMMEND = "recommend"

@dataclass
class CondicionRegla:
    """Representación de una condición SI en una regla."""
    predicado: str
    operador: OperadorCondicion
    valor: Any
    variable: Optional[str] = None
    peso: float = 1.0
    explicacion: str = ""

@dataclass
class AccionRegla:
    """Representación de una acción ENTONCES en una regla."""
    tipo: TipoAccion
    predicado: str
    valor: Any = None
    parametros: Dict[str, Any] = field(default_factory=dict)
    confianza: float = 1.0
    explicacion: str = ""

@dataclass
class ReglaProduccionAcademica:
    """Representación de una regla de producción completa."""
    id: str
    nombre: str
    condiciones: List[CondicionRegla]
    acciones: List[AccionRegla]
    prioridad: float = 0.0
    especificidad: Optional[int] = None
    complejidad: Optional[int] = None
    descripcion: str = ""
    dominio: str = ""
    fuente_conocimiento: str = ""

    def __post_init__(self):
        if self.especificidad is None:
            self.especificidad = len(self.condiciones)
        if self.complejidad is None:
            self.complejidad = len(self.condiciones) + len(self.acciones)