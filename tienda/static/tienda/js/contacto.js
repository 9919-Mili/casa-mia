(function () {
  "use strict";

  var form = document.getElementById("form-contacto");
  if (!form) return;

  var MAX_MENSAJE = 800;

  var reglas = {
    nombre: function (v) {
      v = v.trim();
      if (v.length < 3) return "Escribí tu nombre y apellido (mínimo 3 caracteres).";
      if (!/^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ'’ .-]+$/.test(v)) return "El nombre solo puede contener letras y espacios.";
      return "";
    },
    email: function (v) {
      v = v.trim();
      if (!v) return "Ingresá tu correo electrónico.";
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) return "Ingresá un correo válido, por ejemplo nombre@dominio.com.";
      return "";
    },
    telefono: function (v) {
      v = v.trim();
      if (!v) return "";
      if (!/^[0-9 +()-]+$/.test(v)) return "El teléfono solo puede contener números, espacios, + ( ) y -.";
      if (v.replace(/\D/g, "").length < 8) return "El teléfono debe tener al menos 8 dígitos.";
      return "";
    },
    motivo: function (v) {
      return v ? "" : "Elegí un motivo para poder ayudarte mejor.";
    },
    mensaje: function (v) {
      v = v.trim();
      if (v.length < 10) return "El mensaje es muy corto (mínimo 10 caracteres).";
      if (v.split(/\s+/).length < 3) return "Escribí al menos tres palabras para que podamos entender tu consulta.";
      if (v.length > MAX_MENSAJE) return "El mensaje no puede superar los " + MAX_MENSAJE + " caracteres.";
      return "";
    }
  };

  function mostrar(nombre, mensaje) {
    var caja = form.querySelector('[data-campo="' + nombre + '"]');
    caja.querySelector(".campo-error").textContent = mensaje;
    caja.classList.toggle("tiene-error", mensaje !== "");
    caja.classList.toggle("es-valido", mensaje === "" && form.elements[nombre].value.trim() !== "");
  }

  function validar(nombre) {
    var mensaje = reglas[nombre](form.elements[nombre].value);
    mostrar(nombre, mensaje);
    return mensaje === "";
  }

  Object.keys(reglas).forEach(function (nombre) {
    var campo = form.elements[nombre];
    campo.addEventListener("blur", function () { validar(nombre); });
    campo.addEventListener("input", function () {
      var caja = form.querySelector('[data-campo="' + nombre + '"]');
      if (caja.classList.contains("tiene-error")) validar(nombre);
    });
  });

  // Contador de caracteres del mensaje
  var mensaje = form.elements.mensaje;
  var contador = document.createElement("p");
  contador.className = "contador";
  mensaje.insertAdjacentElement("afterend", contador);
  function actualizarContador() {
    contador.textContent = mensaje.value.length + " / " + MAX_MENSAJE;
  }
  mensaje.addEventListener("input", actualizarContador);
  actualizarContador();

  form.addEventListener("submit", function (evento) {
    var primerInvalido = null;
    Object.keys(reglas).forEach(function (nombre) {
      if (!validar(nombre) && !primerInvalido) primerInvalido = form.elements[nombre];
    });
    if (primerInvalido) {
      evento.preventDefault();
      primerInvalido.focus();
      return;
    }
    var boton = form.querySelector('button[type="submit"]');
    boton.disabled = true;
    boton.textContent = "Enviando…";
  });
})();