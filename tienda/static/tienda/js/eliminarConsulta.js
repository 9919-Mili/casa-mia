let consultaIdAEliminar = null;

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("confirmar-eliminar");
    const confirmarBtn = document.getElementById("confirmar-eliminar-btn");
    const cancelarBtn = document.getElementById("cancelar-eliminar-btn");
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    // 1. Al tocar "Eliminar" en una fila: guardar el id y abrir el modal
    document.querySelectorAll(".eliminar-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            consultaIdAEliminar = btn.dataset.id;
            document.getElementById("eliminar-nombre").textContent = btn.dataset.nombre;
            modal.showModal();
        });
    });

    // 2. Cancelar: cerrar el modal sin hacer nada
    cancelarBtn.addEventListener("click", () => modal.close());

    // 3. Confirmar: pedirle al servidor que borre
    confirmarBtn.addEventListener("click", () => {
        if (!consultaIdAEliminar) return;

        fetch(`/eliminarConsulta/${consultaIdAEliminar}/`, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Recargamos para que el resumen estadístico se actualice
                window.location.reload();
            }
            modal.close();
        })
        .catch(error => {
            console.error("Error al eliminar:", error);
            modal.close();
        });
    });
});