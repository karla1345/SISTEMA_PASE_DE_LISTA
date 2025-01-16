document.addEventListener('DOMContentLoaded', () => {
    // Formulario de nuevo estudiante
    const nuevoEstudianteForm = document.getElementById('nuevo-estudiante-form');
    if (nuevoEstudianteForm) {
        nuevoEstudianteForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('/lista', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    location.reload();  // Recargar la página para mostrar el nuevo estudiante
                }
            } catch (error) {
                console.error('Error al agregar estudiante:', error);
            }
        });
    }

    // Botones de asistencia
    const botonesAsistencia = document.querySelectorAll('.btn-toggle-asistencia');
    botonesAsistencia.forEach(boton => {
        boton.addEventListener('click', async (e) => {
            const estudianteId = e.target.closest('tr').dataset.id;
            
            try {
                const response = await fetch('/marcar_asistencia', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: id=${estudianteId}
                });
                
                const data = await response.json();
                if (data.success) {
                    e.target.classList.toggle('btn-presente');
                    e.target.classList.toggle('btn-ausente');
                    e.target.textContent = e.target.textContent === 'Presente' ? 'Ausente' : 'Presente';
                }
            } catch (error) {
                console.error('Error al marcar asistencia:', error);
            }
        });
    });
});