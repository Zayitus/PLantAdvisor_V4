from typing import Dict, List, Any, Optional
from src.core.memoria_trabajo import MemoriaTrabajo, TipoHecho
from src.core.sintaxis_reglas import ReglaProduccionAcademica, CondicionRegla, OperadorCondicion, TipoAccion, AccionRegla

class ParserReglasAcademico:
    """Evalúa y ejecuta reglas de forma dinámica."""
    def __init__(self, memoria_trabajo: MemoriaTrabajo):
        self.memoria = memoria_trabajo
        print("🔧 Parser de Reglas Académico Inicializado")

    def evaluar_regla(self, regla: ReglaProduccionAcademica) -> Optional[Dict[str, Any]]:
        """Evalúa si las condiciones de una regla se cumplen."""
        bindings = {}
        for condicion in regla.condiciones:
            if not self._evaluar_condicion(condicion, bindings):
                return None
        return {'bindings': bindings}

    def _evaluar_condicion(self, condicion: CondicionRegla, bindings: Dict[str, Any]) -> bool:
        """
        Lógica interna completa para evaluar una única condición.
        """
        hecho = self.memoria.obtener_hecho(condicion.predicado)

        # --- LÓGICA COMPLETA RESTAURADA ---
        if condicion.operador == OperadorCondicion.NO_EXISTE:
            return hecho is None
        if condicion.operador == OperadorCondicion.EXISTE:
            return hecho is not None

        if hecho is None:
            return False

        valor_hecho = hecho.valor
        valor_condicion = condicion.valor
        
        resultado = False
        if condicion.operador == OperadorCondicion.IGUAL:
            resultado = (valor_hecho == valor_condicion)
        elif condicion.operador == OperadorCondicion.DIFERENTE:
            resultado = (valor_hecho != valor_condicion)
        elif condicion.operador == OperadorCondicion.EN:
            resultado = (isinstance(valor_condicion, list) and valor_hecho in valor_condicion)
        elif condicion.operador == OperadorCondicion.NO_EN:
            resultado = (isinstance(valor_condicion, list) and valor_hecho not in valor_condicion)
        # Se pueden añadir aquí los demás operadores (>, <, etc.) si fueran necesarios.

        if resultado and condicion.variable:
            bindings[condicion.variable] = valor_hecho
        
        return resultado

    def ejecutar_acciones(self, regla: ReglaProduccionAcademica, bindings: Dict[str, Any]) -> List[str]:
        """Ejecuta la lista de acciones de la parte ENTONCES de una regla."""
        hechos_creados = []
        for accion in regla.acciones:
            valor_accion = accion.valor
            if isinstance(valor_accion, str) and valor_accion.startswith('$'):
                valor_accion = bindings.get(valor_accion[1:], valor_accion)

            if accion.tipo in [TipoAccion.ASSERT, TipoAccion.CONCLUDE, TipoAccion.RECOMMEND]:
                 id_hecho = self.memoria.assert_hecho(
                    predicado=accion.predicado,
                    valor=valor_accion,
                    tipo=TipoHecho.DERIVADO if accion.tipo == TipoAccion.ASSERT else TipoHecho.CONCLUSION,
                    origen=regla.id,
                    confianza=accion.confianza,
                    justificacion=accion.explicacion
                )
                 hechos_creados.append(id_hecho)
        return hechos_creados
