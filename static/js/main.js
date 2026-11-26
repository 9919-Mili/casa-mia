(function () {
  "use strict";

  var boton = document.querySelector(".nav-toggle");
  var menu = document.getElementById("menu-principal");
  if (!boton || !menu) return;

  boton.addEventListener("click", function () {
    var abierto = menu.classList.toggle("abierto");
    boton.setAttribute("aria-expanded", abierto ? "true" : "false");
    boton.setAttribute("aria-label", abierto ? "Cerrar menú" : "Abrir menú");
  });
})();