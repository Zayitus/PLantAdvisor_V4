from typing import List, Dict, Optional
from src.core.sintaxis_reglas import ReglaProduccionAcademica, CondicionRegla, AccionRegla, OperadorCondicion, TipoAccion

class BaseConocimientoBotanicoTDF:
    """Contiene el conocimiento experto en forma de reglas de producción."""
    def __init__(self):
        self.reglas: List[ReglaProduccionAcademica] = self._crear_reglas()
        self.indice_reglas: Dict[str, ReglaProduccionAcademica] = {r.id: r for r in self.reglas}
        print(f"🌿 Base de Conocimiento TDF Inicializada con {len(self.reglas)} reglas.")

    def obtener_reglas(self) -> List[ReglaProduccionAcademica]:
        return self.reglas

    def obtener_regla_por_id(self, regla_id: str) -> Optional[ReglaProduccionAcademica]:
        return self.indice_reglas.get(regla_id)

    def _crear_reglas(self) -> List[ReglaProduccionAcademica]:
        return [
            # --- REGLA DE DIAGNÓSTICO ---
            ReglaProduccionAcademica(
                id="R001_AMBIENTE_INTERIOR_TDF_INVIERNO",
                nombre="Detección de Ambiente Interior TDF en Invierno",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("calefaccion_nivel", OperadorCondicion.EN, ["alta", "muy_alta"]),
                    CondicionRegla("ambiente_seco_extremo", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.ASSERT, "ambiente_seco_extremo", True, confianza=0.9, explicacion="Calefacción TDF genera sequedad extrema")],
                prioridad=9.5, dominio="condiciones_ambientales_tdf"
            ),
            
            # --- REGLAS DE RECOMENDACIÓN (Ordenadas por prioridad descendente) ---
            ReglaProduccionAcademica(
                id="R011_EXTERIOR_MATA_NEGRA",
                nombre="Recomendar Mata Negra para Exterior Resistente",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "principiante"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "alta"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Mata Negra", confianza=0.97, explicacion="La Mata Negra es un arbusto nativo extremadamente resistente al viento y al sol directo. Es una opción perfecta y de bajo mantenimiento para jardines en TDF.")],
                prioridad=9.0, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R008_EXTERIOR_RESISTENTE",
                nombre="Recomendar Planta Resistente para Exterior",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "principiante"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "decorativa"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Calafate", confianza=0.98, explicacion="El Calafate es un arbusto nativo extremadamente resistente al viento y las duras condiciones de TDF, ideal para principiantes.")],
                prioridad=8.5, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R017_EXTERIOR_LENGAS",
                nombre="Recomendar Lengas para Jardín Amplio",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "avanzado"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "decorativa"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Lengas", confianza=0.90, explicacion="La Lenga es el árbol emblemático de los bosques andino-patagónicos. Ideal para un jardinero avanzado que desea una pieza central icónica y de gran porte.")],
                prioridad=8.3, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R019_EXTERIOR_CHAURA",
                nombre="Recomendar Chaura para Frutos Decorativos",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "intermedio"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "decorativa"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "media"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Chaura", confianza=0.91, explicacion="La Chaura es un arbusto perenne muy atractivo, especialmente por sus frutos coloridos (blancos, rosados o rojos). Es una gran adición para un jardín con luz media.")],
                prioridad=8.3, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R012_EXTERIOR_NIRE",
                nombre="Recomendar Ñire para Exterior Adaptable",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "intermedio"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "decorativa"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Ñire", confianza=0.94, explicacion="El Ñire es un árbol nativo muy adaptable, conocido por los hermosos colores de sus hojas en otoño. Ideal para dar un toque local y resistente a cualquier jardín.")],
                prioridad=8.2, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R015_EXTERIOR_ORQUIDEA",
                nombre="Recomendar Orquídea de Magallanes para Expertos",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "avanzado"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "flores"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Orquídea de Magallanes", confianza=0.85, explicacion="La Orquídea de Magallanes es una joya nativa. Es delicada y un desafío gratificante para un jardinero experimentado que busca una flor única.")],
                prioridad=8.1, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R016_EXTERIOR_ZAPATITO",
                nombre="Recomendar Zapatito de la Virgen",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "intermedio"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "flores"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "media"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Zapatito de la Virgen", confianza=0.89, explicacion="El Zapatito de la Virgen tiene una de las flores más curiosas y atractivas de la flora nativa, ideal para un lugar con luz parcial en el jardín.")],
                prioridad=8.1, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R005_EXTERIOR_FLORES",
                nombre="Recomendar Planta con Flores para Exterior",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "flores"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Notro / Ciruelillo", confianza=0.95, explicacion="El Notro es un árbol nativo famoso por sus espectaculares flores rojas, ideal para jardines en TDF.")],
                prioridad=8.0, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R014_INTERIOR_FLORES_INVIERNO",
                nombre="Recomendar Cactus de Navidad para Flores en Interior",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "flores"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "intermedio"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Cactus de Navidad", confianza=0.91, explicacion="El Cactus de Navidad es famoso por su espectacular floración invernal, ideal para dar color a los interiores durante los meses fríos.")],
                prioridad=7.9, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R009_INTERIOR_AVANZADO_DECORATIVA",
                nombre="Recomendar Planta Decorativa para Usuario Avanzado",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "avanzado"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "decorativa"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "media"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Monstera Deliciosa", confianza=0.9, explicacion="La Monstera Deliciosa es una planta icónica y muy decorativa que recompensa los cuidados de un usuario más experimentado.")],
                prioridad=7.8, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R013_INTERIOR_HUMEDAD",
                nombre="Recomendar Helecho para Ambiente Húmedo",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "decorativa"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "intermedio"),
                    CondicionRegla("calefaccion_nivel", OperadorCondicion.IGUAL, "baja"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Helecho Serrucho", confianza=0.88, explicacion="El Helecho Serrucho ama la humedad. Un ambiente con calefacción baja sugiere mayor humedad, ideal para esta planta.")],
                prioridad=7.6, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R010_INTERIOR_UTILITARIA",
                nombre="Recomendar Planta Utilitaria de Interior",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "utilitaria"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "alta"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Aloe Vera", confianza=0.93, explicacion="El Aloe Vera es una planta utilitaria excelente por el gel de sus hojas, y prospera con mucha luz indirecta o algo de sol directo.")],
                prioridad=7.5, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R003_PRINCIPIANTE_INTERIOR",
                nombre="Recomendar para Principiantes en Interior",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("experiencia_usuario", OperadorCondicion.IGUAL, "principiante"),
                    CondicionRegla("mascotas_presentes", OperadorCondicion.IGUAL, True),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Lazo de Amor", confianza=0.9, explicacion="El Lazo de Amor es extremadamente resistente, fácil de cuidar y seguro para mascotas.")],
                prioridad=7.5, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R018_EXTERIOR_FRUTILLA_DIABLO",
                nombre="Recomendar Frutilla del Diablo para Cubresuelos",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "decorativa"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "baja"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Frutilla del Diablo", confianza=0.88, explicacion="La Frutilla del Diablo es un excelente cubresuelos nativo que prospera en zonas sombrías y húmedas del jardín, donde otras plantas no crecen.")],
                prioridad=7.4, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R002_RECOMENDAR_SANSEVIERIA_SECO",
                nombre="Recomendar Sansevieria para Ambiente Seco",
                condiciones=[
                    CondicionRegla("ambiente_seco_extremo", OperadorCondicion.IGUAL, True),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Sansevieria / Lengua de suegra", confianza=0.95, explicacion="La Sansevieria es ideal para ambientes secos y requiere muy poco riego.")],
                prioridad=7.3, dominio="recomendacion_final"
            ),
            
            # --- REGLAS AÑADIDAS EN ESTA ACTUALIZACIÓN (BLOQUE 5) ---
            ReglaProduccionAcademica(
                id="R020_INTERIOR_MENTA",
                nombre="Recomendar Menta para Interior Aromático/Utilitario",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.EN, ["aromatica", "utilitaria"]),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "alta"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Menta", confianza=0.89, explicacion="La Menta crece vigorosamente en interiores con mucha luz, ideal para tener hierbas frescas a mano para cocinar o disfrutar de su aroma.")],
                prioridad=7.2, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R021_EXTERIOR_ROMERO",
                nombre="Recomendar Romero para Exterior Aromático/Utilitario",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.EN, ["aromatica", "utilitaria"]),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "alta"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Romero Rastrero", confianza=0.90, explicacion="El Romero Rastrero es una excelente opción para exterior a pleno sol. Es resistente, de bajo mantenimiento y sirve tanto como condimento como planta aromática.")],
                prioridad=7.1, dominio="recomendacion_final"
            ),

            ReglaProduccionAcademica(
                id="R004_INTERIOR_POCA_LUZ",
                nombre="Recomendar para Interior con Poca Luz",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "interior"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "baja"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Potus", confianza=0.92, explicacion="El Potus es una de las plantas más tolerantes a condiciones de baja luminosidad.")],
                prioridad=7.0, dominio="recomendacion_final"
            ),
            ReglaProduccionAcademica(
                id="R006_EXTERIOR_AROMATICA_LAVANDA",
                nombre="Recomendar Lavanda para Exterior Aromática",
                condiciones=[
                    CondicionRegla("ubicacion_usuario", OperadorCondicion.IGUAL, "exterior"),
                    CondicionRegla("proposito_planta", OperadorCondicion.IGUAL, "aromatica"),
                    CondicionRegla("iluminacion_disponible", OperadorCondicion.IGUAL, "alta"),
                    CondicionRegla("planta_ideal", OperadorCondicion.NO_EXISTE, None)
                ],
                acciones=[AccionRegla(TipoAccion.RECOMMEND, "planta_ideal", "Lavanda", confianza=0.9, explicacion="La Lavanda prospera a pleno sol, es resistente y ofrece un aroma excepcional.")],
                prioridad=7.0, dominio="recomendacion_final"
            ),
        ]