import os
import shutil

# --- CONTENIDO DE CADA ARCHIVO ---
# Se extrae el contenido de los archivos que has subido.
# En un entorno real, estos archivos estarían en el disco.

# Contenido de src/core/sintaxis_reglas.py
sintaxis_reglas_content = """
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

class OperadorCondicion(Enum):
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
    predicado: str
    operador: OperadorCondicion
    valor: Any
    variable: Optional[str] = None
    peso: float = 1.0
    explicacion: str = ""

    def __str__(self) -> str:
        var_str = f" -> ${self.variable}" if self.variable else ""
        return f"{self.predicado} {self.operador.value} {self.valor}{var_str}"

@dataclass
class AccionRegla:
    tipo: TipoAccion
    predicado: str
    valor: Any = None
    parametros: Dict[str, Any] = field(default_factory=dict)
    confianza: float = 1.0
    explicacion: str = ""

    def __str__(self) -> str:
        return f"{self.tipo.value}({self.predicado}, {self.valor})"

@dataclass
class ReglaProduccionAcademica:
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
    ejemplos: List[str] = field(default_factory=list)
    activa: bool = True
    version: str = "1.0"

    def __post_init__(self):
        if self.especificidad is None:
            self.especificidad = len(self.condiciones)
        if self.complejidad is None:
            self.complejidad = len(self.condiciones) + len(self.acciones)

    def generar_explicacion_natural(self) -> str:
        cond_text = ' Y '.join([c.explicacion or str(c) for c in self.condiciones])
        act_text = ', '.join([a.explicacion or str(a) for a in self.acciones])
        return f"SI {cond_text}, ENTONCES {act_text}"

    def validar_sintaxis(self) -> List[str]:
        errors = []
        if not self.id: errors.append("ID de regla requerido")
        if not self.condiciones: errors.append("Al menos una condición requerida")
        if not self.acciones: errors.append("Al menos una acción requerida")
        return errors
"""

# Contenido de src/core/memoria_trabajo.py
memoria_trabajo_content = """
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from .sintaxis_reglas import TipoHecho

@dataclass
class Hecho:
    id: str
    predicado: str
    valor: Any
    tipo: TipoHecho
    origen: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    justificacion: str = ""
    confianza: float = 1.0

class MemoriaTrabajo:
    def __init__(self):
        self._hechos: Dict[str, Hecho] = {}
        self._historial: List[Hecho] = []
        self._indice_por_predicado: Dict[str, Set[str]] = {}
        self._indice_por_tipo: Dict[TipoHecho, Set[str]] = {t: set() for t in TipoHecho}
        self._contador_hechos = 0
        print("🧠 Memoria de Trabajo Inicializada")

    def _generar_id_hecho(self) -> str:
        self._contador_hechos += 1
        return f"F{self._contador_hechos:04d}"

    def _insertar_hecho(self, hecho: Hecho):
        self._hechos[hecho.id] = hecho
        self._historial.append(hecho)
        self._indice_por_predicado.setdefault(hecho.predicado, set()).add(hecho.id)
        self._indice_por_tipo[hecho.tipo].add(hecho.id)

    def assert_hecho(self, predicado: str, valor: Any, tipo: TipoHecho, origen: Optional[str] = None, justificacion: str = "", confianza: float = 1.0) -> str:
        hecho_id = self._generar_id_hecho()
        hecho = Hecho(hecho_id, predicado, valor, tipo, origen, justificacion=justificacion, confianza=confianza)
        self._insertar_hecho(hecho)
        print(f"✅ HECHO {tipo.name}: {predicado} = {valor}")
        return hecho_id

    def obtener_hecho(self, predicado: str) -> Optional[Hecho]:
        hechos_ids = self._indice_por_predicado.get(predicado, set())
        if not hechos_ids:
            return None
        return max((self._hechos[hid] for hid in hechos_ids), key=lambda h: h.timestamp)

    def obtener_hechos_por_tipo(self, tipo: TipoHecho) -> List[Hecho]:
        return [self._hechos[hid] for hid in self._indice_por_tipo[tipo]]

    def obtener_todos_los_hechos(self) -> List[Hecho]:
        return list(self._hechos.values())

    def limpiar_memoria(self):
        self.__init__()
        print("🧹 Memoria de Trabajo Limpiada")

    def generar_trace_explicacion(self) -> Dict[str, Any]:
        return {
            'total_hechos': len(self._hechos),
            'hechos_por_tipo': {t.name: len(s) for t, s in self._indice_por_tipo.items()},
            'historial_completo': [h.__dict__ for h in self._historial]
        }
"""

# Contenido de src/core/agenda.py
agenda_content = """
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
"""

# Contenido de src/core/motor_inferencia.py
motor_inferencia_content = """
from typing import Dict, List, Any, Optional, Protocol
from .memoria_trabajo import MemoriaTrabajo
from .agenda import Agenda
from .sintaxis_reglas import ReglaProduccionAcademica

class BaseConocimiento(Protocol):
    def obtener_reglas(self) -> List[ReglaProduccionAcademica]: ...
    def obtener_regla_por_id(self, regla_id: str) -> Optional[ReglaProduccionAcademica]: ...

class MotorInferenciaAcademico:
    def __init__(self, memoria_trabajo: MemoriaTrabajo, agenda: Agenda, max_ciclos: int = 50):
        self.memoria_trabajo = memoria_trabajo
        self.agenda = agenda
        self.max_ciclos = max_ciclos
        print("🧠 Motor de Inferencia Inicializado")

    def ejecutar_consulta(self, base_conocimiento: BaseConocimiento, hechos_iniciales: Dict[str, Any]) -> Dict[str, Any]:
        print("\\n🚀 INICIANDO CONSULTA...")
        self.memoria_trabajo.limpiar_memoria()
        self.agenda.limpiar_agenda()

        for predicado, valor in hechos_iniciales.items():
            self.memoria_trabajo.assert_hecho(predicado, valor, tipo=TipoHecho.INICIAL, justificacion="Hecho inicial de usuario")

        ciclos = 0
        while ciclos < self.max_ciclos:
            ciclos += 1
            print(f"\\n🔄 CICLO {ciclos}")

            if self.agenda.esta_vacia():
                print("🏁 Inferencia terminada: Agenda vacía.")
                break

            regla_instanciada = self.agenda.seleccionar_proxima_regla()
            if not regla_instanciada:
                print("🏁 Inferencia terminada: No hay más reglas para ejecutar.")
                break

            regla_a_ejecutar = base_conocimiento.obtener_regla_por_id(regla_instanciada.regla_id)
            if regla_a_ejecutar:
                print(f"⚡ EJECUTANDO: {regla_a_ejecutar.id}")
                # Aquí iría la lógica de ejecución de acciones
                self.agenda.marcar_como_ejecutada(regla_instanciada)
            
            # La fase de MATCH debería ocurrir aquí para llenar la agenda
            # Por simplicidad, este demo asume que la agenda se llena externamente

        if ciclos >= self.max_ciclos:
            print("🏁 Inferencia terminada: Límite de ciclos alcanzado.")

        return self.memoria_trabajo.generar_trace_explicacion()
"""

# Contenido de src/knowledge/base_conocimiento.py
base_conocimiento_content = """
from typing import List, Dict, Any
from src.core.sintaxis_reglas import ReglaProduccionAcademica, CondicionRegla, AccionRegla, OperadorCondicion, TipoAccion

class BaseConocimientoBotanicoTDF:
    def __init__(self):
        self.reglas: List[ReglaProduccionAcademica] = self._crear_reglas()
        self.indice_reglas: Dict[str, ReglaProduccionAcademica] = {r.id: r for r in self.reglas}
        print(f"🌿 Base de Conocimiento Botánico TDF Inicializada con {len(self.reglas)} reglas.")

    def obtener_reglas(self) -> List[ReglaProduccionAcademica]:
        return self.reglas

    def obtener_regla_por_id(self, regla_id: str) -> ReglaProduccionAcademica:
        return self.indice_reglas.get(regla_id)

    def _crear_reglas(self) -> List[ReglaProduccionAcademica]:
        return [
            ReglaProduccionAcademica(
                id="R001_AMBIENTE_INTERIOR_TDF_INVIERNO",
                nombre="Detección de Ambiente Interior TDF en Invierno",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior", explicacion="Usuario en ambiente interior"),
                    CondicionRegla("calefaccion_nivel", OperadorCondicion.EN, ["alta", "muy_alta"], explicacion="Calefacción intensa")
                ],
                acciones=[
                    AccionRegla(TipoAccion.ASSERT, "ambiente_seco_extremo", True, confianza=0.9, explicacion="Calefacción TDF genera sequedad extrema")
                ],
                prioridad=8.0,
                dominio="condiciones_ambientales_tdf"
            ),
            ReglaProduccionAcademica(
                id="R007_SEGURIDAD_ABSOLUTA_MASCOTAS",
                nombre="Seguridad Absoluta para Mascotas",
                condiciones=[
                    CondicionRegla("mascotas_presentes", OperadorCondicion.IGUAL, True, peso=3.0, explicacion="Hay mascotas"),
                    CondicionRegla("planta_toxica_mascotas", OperadorCondicion.IGUAL, True, variable="planta_evaluada", explicacion="Planta es tóxica")
                ],
                acciones=[
                    AccionRegla(TipoAccion.RETRACT, "planta_candidata", "$planta_evaluada", confianza=1.0, explicacion="Eliminada por toxicidad")
                ],
                prioridad=10.0,
                dominio="seguridad_mascotas"
            )
            # ... Aquí irían el resto de las 10 reglas definidas
        ]
"""

# Contenido de src/knowledge/parser_reglas.py
parser_reglas_content = """
from typing import Dict, List, Any, Optional
from src.core.memoria_trabajo import MemoriaTrabajo
from src.core.sintaxis_reglas import ReglaProduccionAcademica, CondicionRegla, OperadorCondicion, AccionRegla

class ParserReglasAcademico:
    def __init__(self, memoria_trabajo: MemoriaTrabajo):
        self.memoria = memoria_trabajo
        print("🔧 Parser de Reglas Académico Inicializado")

    def evaluar_regla(self, regla: ReglaProduccionAcademica) -> Optional[Dict[str, Any]]:
        bindings = {}
        for condicion in regla.condiciones:
            if not self._evaluar_condicion(condicion, bindings):
                return None
        return {'bindings': bindings}

    def _evaluar_condicion(self, condicion: CondicionRegla, bindings: Dict[str, Any]) -> bool:
        hecho = self.memoria.obtener_hecho(condicion.predicado)
        if condicion.operador == OperadorCondicion.EXISTE:
            return hecho is not None
        if condicion.operador == OperadorCondicion.NO_EXISTE:
            return hecho is None
        if hecho is None:
            return False

        # Lógica de evaluación simplificada
        valor_hecho = hecho.valor
        valor_condicion = condicion.valor
        
        resultado = False
        if condicion.operador == OperadorCondicion.IGUAL:
            resultado = valor_hecho == valor_condicion
        elif condicion.operador == OperadorCondicion.EN:
            resultado = valor_hecho in valor_condicion

        if resultado and condicion.variable:
            bindings[condicion.variable] = valor_hecho
        
        return resultado

    def ejecutar_regla(self, regla: ReglaProduccionAcademica, bindings: Dict[str, Any]) -> List[str]:
        hechos_creados = []
        for accion in regla.acciones:
            valor_accion = accion.valor
            if isinstance(valor_accion, str) and valor_accion.startswith('$'):
                valor_accion = bindings.get(valor_accion[1:], valor_accion)

            id_hecho = self.memoria.assert_hecho(
                accion.predicado,
                valor_accion,
                tipo=accion.tipo,
                origen=regla.id,
                confianza=accion.confianza,
                justificacion=accion.explicacion
            )
            hechos_creados.append(id_hecho)
        return hechos_creados
"""

# Contenido de src/main.py
main_content = """
from src.core.memoria_trabajo import MemoriaTrabajo
from src.core.agenda import Agenda, EstrategiaConflictResolution
from src.core.motor_inferencia import MotorInferenciaAcademico
from src.knowledge.base_conocimiento import BaseConocimientoBotanicoTDF
from src.knowledge.parser_reglas import ParserReglasAcademico

class SistemaExpertoAcademicoCompleto:
    def __init__(self):
        self.memoria_trabajo = MemoriaTrabajo()
        self.agenda = Agenda(EstrategiaConflictResolution.PRIORIDAD_EXPLICITA)
        self.base_conocimiento = BaseConocimientoBotanicoTDF()
        self.parser = ParserReglasAcademico(self.memoria_trabajo)
        self.motor = MotorInferenciaAcademico(self.memoria_trabajo, self.agenda)
        print("🎓 Sistema Experto Académico Completo Inicializado")

    def consultar(self, hechos_usuario: dict):
        # Fase de MATCH: Llenar la agenda
        for regla in self.base_conocimiento.obtener_reglas():
            resultado_eval = self.parser.evaluar_regla(regla)
            if resultado_eval:
                self.agenda.activar_regla(
                    regla_id=regla.id,
                    bindings=resultado_eval['bindings'],
                    hechos_activadores=[], # Simplificado
                    especificidad=regla.especificidad,
                    prioridad_explicita=regla.prioridad
                )
        
        # Fase de INFERENCIA
        return self.motor.ejecutar_consulta(self.base_conocimiento, hechos_usuario)

def main():
    sistema = SistemaExpertoAcademicoCompleto()
    
    caso_prueba = {
        'ubicacion_usuario': 'interior',
        'calefaccion_nivel': 'alta',
        'mascotas_presentes': True,
        'planta_toxica_mascotas': True,
        'planta_candidata': 'Monstera'
    }
    
    resultado = sistema.consultar(caso_prueba)
    print("\\n--- RESULTADO FINAL ---")
    print(resultado)

if __name__ == "__main__":
    main()
"""

# Contenido para README.md
readme_content = """
# PlantAdvisor-TDF: Sistema Experto de Flora Fueguina

Este proyecto es una implementación académicamente rigurosa de un sistema experto para la recomendación de plantas de interior y exterior en la región de Tierra del Fuego, Argentina.

## Arquitectura

El sistema sigue una arquitectura clásica de sistemas expertos (tipo MYCIN/DENDRAL) con una estricta separación entre la base de conocimiento y el motor de inferencia.

- **Motor de Inferencia:** `src/core`
- **Base de Conocimiento:** `src/knowledge`
- **Aplicación Principal:** `src/main.py`
- **Interfaz Web (futuro):** `src/web`

## Instalación

1. Clona el repositorio.
2. (Opcional) Crea un entorno virtual: `python -m venv venv` y actívalo.
3. Instala las dependencias: `pip install -r requirements.txt`

## Uso

Para ejecutar una consulta de demostración, corre el script principal:
```bash
python src/main.py
```
"""

# Contenido para requirements.txt (inicialmente vacío)
requirements_content = """
# Por ahora no hay dependencias externas.
# Se agregarán Flask/FastAPI para la API web.
"""

# Contenido para .gitignore
gitignore_content = """
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# Archivos de sistema
.DS_Store
"""

# --- SCRIPT DE ORGANIZACIÓN ---

def organizar_proyecto():
    """
    Crea la estructura de carpetas y archivos para el proyecto del sistema experto.
    """
    print("🚀 Iniciando organización del proyecto...")

    # Estructura de directorios
    base_dir = "plantadvisor_tdf"
    dirs = [
        os.path.join(base_dir, "src/core"),
        os.path.join(base_dir, "src/knowledge"),
        os.path.join(base_dir, "src/web/templates"),
        os.path.join(base_dir, "src/web/static"),
        os.path.join(base_dir, "docs"),
        os.path.join(base_dir, "tests")
    ]

    # Mapeo de archivos: origen -> destino y contenido
    files_to_create = {
        os.path.join(base_dir, "src/core/sintaxis_reglas.py"): sintaxis_reglas_content,
        os.path.join(base_dir, "src/core/memoria_trabajo.py"): memoria_trabajo_content,
        os.path.join(base_dir, "src/core/agenda.py"): agenda_content,
        os.path.join(base_dir, "src/core/motor_inferencia.py"): motor_inferencia_content,
        os.path.join(base_dir, "src/knowledge/base_conocimiento.py"): base_conocimiento_content,
        os.path.join(base_dir, "src/knowledge/parser_reglas.py"): parser_reglas_content,
        os.path.join(base_dir, "src/main.py"): main_content,
        os.path.join(base_dir, "README.md"): readme_content,
        os.path.join(base_dir, "requirements.txt"): requirements_content,
        os.path.join(base_dir, ".gitignore"): gitignore_content,
        # Archivos __init__.py para convertir directorios en paquetes
        os.path.join(base_dir, "src/__init__.py"): "",
        os.path.join(base_dir, "src/core/__init__.py"): "",
        os.path.join(base_dir, "src/knowledge/__init__.py"): "",
        os.path.join(base_dir, "src/web/__init__.py"): "",
        # Placeholders
        os.path.join(base_dir, "tests/test_placeholder.py"): "# Agrega aquí tus tests",
        os.path.join(base_dir, "docs/ARQUITECTURA.md"): "# Documentación de la arquitectura",
        os.path.join(base_dir, "src/web/api.py"): "# Futura API con Flask/FastAPI"
    }

    # Eliminar directorio base si ya existe para un inicio limpio
    if os.path.exists(base_dir):
        print(f"🗑️  Eliminando directorio existente: {base_dir}")
        shutil.rmtree(base_dir)

    # 1. Crear directorios
    print("\n📁 Creando estructura de directorios...")
    for d in dirs:
        os.makedirs(d)
        print(f"   - Creado: {d}")

    # 2. Crear archivos
    print("\n✍️  Escribiendo archivos del proyecto...")
    for path, content in files_to_create.items():
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.strip())
            print(f"   - Creado: {path}")
        except Exception as e:
            print(f"   - ❌ Error creando {path}: {e}")

    print("\n\n✅ ¡Proyecto organizado con éxito!")
    print(f"La estructura completa se ha creado en la carpeta '{base_dir}'.")
    print("\n👉 Próximo paso sugerido: `cd plantadvisor_tdf` y explora la estructura.")

if __name__ == "__main__":
    organizar_proyecto()
