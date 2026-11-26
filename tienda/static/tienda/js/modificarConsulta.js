document.addEventListener("DOMContentLoaded", () => {
    const formulario = document.getElementById("form-modificar");
    const resultado = document.getElementById("resultado");

    formulario.addEventListener("submit", async (event) => {
        event.preventDefault();
        resultado.className = "";
        resultado.innerHTML = "";

        try {
            // Envía el formulario por POST a la misma URL
            const respuesta = await fetch("", { method: "POST", body: new FormData(formulario) });
            const data = await respuesta.json();

            if (data.success) {
                resultado.className = "mensaje";
                resultado.innerText = data.message;
                // Vuelve al panel después de 1,5 segundos
                setTimeout(() => { window.location.href = "/panel/"; }, 1500);
            } else {
                resultado.className = "mensaje mensaje-error";
                for (const campo in data.errors) {
                    resultado.innerHTML += `<p>${data.errors[campo].join(", ")}</p>`;
                }
            }
        } catch (error) {
            resultado.className = "mensaje mensaje-error";
            resultado.innerText = "Error de conexión.";
            console.error("Error en la solicitud:", error);
        }
    });
});