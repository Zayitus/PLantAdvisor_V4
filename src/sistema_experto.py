from .core.memoria_trabajo import MemoriaTrabajo, TipoHecho
from .core.agenda import Agenda, EstrategiaConflictResolution
from .core.motor_inferencia import MotorInferenciaAcademico
from .knowledge.base_conocimiento import BaseConocimientoBotanicoTDF
from .knowledge.parser_reglas import ParserReglasAcademico

class SistemaExpertoPlantaTDF:
    """
    Clase que encapsula el sistema experto completo, haciéndolo reutilizable.
    """
    def __init__(self):
        """Inicializa todos los componentes del sistema experto."""
        print("="*50)
        print("🎓 INICIALIZANDO SISTEMA EXPERTO DE FLORA FUEGUINA 🎓")
        print("="*50)
        self.memoria = MemoriaTrabajo()
        self.agenda = Agenda(EstrategiaConflictResolution.PRIORIDAD_EXPLICITA)
        self.parser = ParserReglasAcademico(self.memoria)
        self.base_conocimiento = BaseConocimientoBotanicoTDF()
        self.motor = MotorInferenciaAcademico(self.memoria, self.agenda, self.parser)
        print("\n✅ Sistema listo para recibir consultas.")

    def consultar(self, hechos_iniciales: dict) -> dict:
        """
        Realiza una consulta completa al sistema experto.
        """
        # Limpiar estado de la consulta anterior
        self.memoria.limpiar_memoria()
        self.agenda.limpiar_agenda()

        print("\n📝 HECHOS INICIALES RECIBIDOS:")
        for predicado, valor in hechos_iniciales.items():
            self.memoria.assert_hecho(predicado, valor, tipo=TipoHecho.INICIAL, justificacion="Dato de entrada del usuario")

        # Ejecutar el motor de inferencia
        self.motor.inferir(self.base_conocimiento)

        print("\n" + "="*50)
        print("📊 CONSULTA FINALIZADA")
        print("="*50)
        
        return self.memoria.generar_trace_explicacion()
