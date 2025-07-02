document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('consulta-form');
    const resultadosSection = document.getElementById('resultados');
    const loader = document.getElementById('loader');
    const contenidoResultados = document.getElementById('contenido-resultados');

    const plantImages = {
        "Sansevieria / Lengua de suegra": "sansevieria.jpg",
        "Lazo de Amor": "lazo_de_amor.jpg",
        "Potus": "potus.jpg",
        "Notro / Ciruelillo": "notro.jpg",
        "Lavanda": "lavanda.jpg",
        "Calafate": "calafate.jpg",
        "Monstera Deliciosa": "monstera.jpg",
        "Aloe Vera": "aloe_vera.jpg",
        "Mata Negra": "mata_negra.jpg",
        "Ñire": "nire.jpg",
        "Helecho Serrucho": "helecho_serrucho.jpg",
        "Cactus de Navidad": "cactus_navidad.jpg",
        "Orquídea de Magallanes": "orquidea_magallanes.jpg",
        "Zapatito de la Virgen": "zapatito_virgen.jpg",
        "Lengas": "lengas.jpg",
        "Frutilla del Diablo": "frutilla_diablo.jpg",
        "Chaura": "chaura.jpg"
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        resultadosSection.classList.remove('hidden');
        loader.style.display = 'flex';
        contenidoResultados.classList.add('hidden');
        contenidoResultados.innerHTML = '';

        const formData = new FormData(form);
        const datosUsuario = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/api/consulta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(datosUsuario),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error en la respuesta del servidor');
            }

            const data = await response.json();
            loader.style.display = 'none';
            mostrarResultados(data);
            contenidoResultados.classList.remove('hidden');

        } catch (error) {
            console.error('Error al consultar:', error);
            loader.style.display = 'none';
            contenidoResultados.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg" role="alert"><p class="font-bold">Error en la consulta</p><p>${error.message}</p></div>`;
            contenidoResultados.classList.remove('hidden');
        }
    });

    function mostrarResultados(data) {
        let html = '';

        const recomendaciones = data.conclusiones.filter(c => c.predicado === 'planta_ideal');
        
        const uniqueRecomendaciones = [];
        const seenPlants = new Set();
        recomendaciones.forEach(rec => {
            if (!seenPlants.has(rec.valor)) {
                uniqueRecomendaciones.push(rec);
                seenPlants.add(rec.valor);
            }
        });

        if (uniqueRecomendaciones.length > 0) {
            html += '<h3 class="text-xl font-semibold text-slate-800 mb-4">Estas son tus opciones ideales:</h3>';
            html += '<div class="grid grid-cols-1 md:grid-cols-2 gap-6">';

            uniqueRecomendaciones.forEach(rec => {
                const plantName = rec.valor;
                const imageName = plantImages[plantName] || 'placeholder.png';

                html += `
                    <div class="bg-white border border-slate-200 rounded-xl p-5 flex flex-col card-hover-effect">
                        <img src="/static/images/${imageName}" alt="Imagen de ${plantName}" class="w-full h-48 object-cover rounded-lg shadow-sm mb-4" onerror="this.onerror=null;this.src='/static/images/placeholder.png';">
                        <div class="flex-grow">
                            <p class="font-bold text-lg text-slate-900">${plantName}</p>
                            <p class="mt-2 text-sm text-slate-600">${rec.justificacion}</p>
                        </div>
                        <div class="mt-4 pt-3 border-t border-slate-200 text-right">
                            <span class="text-xs text-slate-500 font-semibold">Confianza del Experto:</span>
                            <span class="font-bold text-green-600">${(rec.confianza * 100).toFixed(0)}%</span>
                        </div>
                    </div>
                `;
            });

            html += '</div>';

        } else {
             html += `<div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-lg text-center">
                        <p class="font-bold">No se encontraron recomendaciones específicas.</p>
                        <p>El sistema no pudo llegar a una conclusión final con los datos proporcionados. ¡Intenta con otras combinaciones!</p>
                    </div>`;
        }

        if (data.hechos_derivados && data.hechos_derivados.length > 0) {
            html += '<h3 class="text-xl font-semibold text-slate-800 mt-8 mb-3 border-t pt-6">Razonamiento Detallado:</h3>';
            html += '<ul class="list-disc list-inside space-y-2 bg-slate-100 p-4 rounded-lg text-sm">';
            data.hechos_derivados.forEach(hecho => {
                html += `<li class="text-slate-700"><span class="font-semibold">${hecho.justificacion}:</span> <span class="bg-green-100 text-green-800 font-medium px-2.5 py-0.5 rounded-full">${hecho.predicado} = ${hecho.valor}</span> <span class="text-slate-400">(Regla: ${hecho.origen})</span></li>`;
            });
            html += '</ul>';
        }

        contenidoResultados.innerHTML = html;
    }
});