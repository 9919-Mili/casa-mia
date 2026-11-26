CATEGORIAS = [
    {"slug": "hogar", "nombre": "Hogar", "tono": "terracota",
     "imagen": "tienda/imagenes/ensaladera.png", "bajada": "Cocina y mesa"},
    {"slug": "decoracion", "nombre": "Decoración", "tono": "rosa",
     "imagen": "tienda/imagenes/jarron.png", "bajada": "Jarrones y marcos"},
    {"slug": "accesorios", "nombre": "Accesorios", "tono": "crema",
     "imagen": "tienda/imagenes/tote.png", "bajada": "Bolsos y neceseres"},
    {"slug": "velas", "nombre": "Velas y Aromas", "tono": "verde",
     "imagen": "tienda/imagenes/vela.png", "bajada": "Para cada ambiente"},
    {"slug": "tazas", "nombre": "Tazas", "tono": "rosa",
     "imagen": "tienda/imagenes/Taza.png", "bajada": "Desayunos lindos"},
    {"slug": "otros", "nombre": "Otros", "tono": "terracota",
     "imagen": "tienda/imagenes/spa.png", "bajada": "Sets y cuidado personal"},
]

PRODUCTOS = [

    # Hogar
    {"id": "bowl-amaro", "nombre": "Bowl de cerámica Amaro", "categoria": "hogar",
     "precio": 14900, "tono": "terracota", "imagen": "tienda/imagenes/bowl.png", "destacado": True,
     "descripcion": "Profundo y liviano, para servir o desayunar."},
    {"id": "vasos-verdes", "nombre": "Vasos de vidrio verde (par)", "categoria": "hogar",
     "precio": 13900, "tono": "verde", "imagen": "tienda/imagenes/vasosverdes.png", "destacado": True,
     "descripcion": "Vidrio soplado con un verde suave."},
    {"id": "ensaladera-hoja", "nombre": "Ensaladera Hoja", "categoria": "hogar",
     "precio": 18700, "tono": "verde", "imagen": "tienda/imagenes/ensaladera.png", "destacado": False,
     "descripcion": "Una pieza grande para llevar a la mesa."},

    # Tazas
    {"id": "taza-lomo", "nombre": "Taza esmaltada Lomo", "categoria": "tazas",
     "precio": 8900, "tono": "terracota", "imagen": "tienda/imagenes/tazaEsm.png", "destacado": True,
     "descripcion": "Esmalte brillante y asa cómoda."},
    {"id": "taza-duraznillo", "nombre": "Taza con plato Duraznillo", "categoria": "tazas",
     "precio": 11500, "tono": "rosa", "imagen": "tienda/imagenes/Taza.png", "destacado": False,
     "descripcion": "Cerámica rosa viejo con plato a tono."},
    {"id": "taza-bosque", "nombre": "Set de 2 tazas Bosque", "categoria": "tazas",
     "precio": 16800, "tono": "verde", "imagen": "tienda/imagenes/tazaBosque.png", "destacado": False,
     "descripcion": "Dos tazas verdes para compartir la merienda."},
    {"id": "set-spa", "nombre": "Set Spa en casa", "categoria": "otros",
     "precio": 19800, "tono": "crema", "imagen": "tienda/imagenes/spa.png", "destacado": False,
     "descripcion": "Productos para el cuidado diario."},
    {"id": "vinchas", "nombre": "Vincha + Muñequeras", "categoria": "otros",
     "precio": 13200, "tono": "rosa", "imagen": "tienda/imagenes/vincha.png", "destacado": False,
     "descripcion": "Para un skincare comodo."},


    # Velas
    {"id": "vela-cedro", "nombre": "Vela Cedro y Palo Santo", "categoria": "velas",
     "precio": 12400, "tono": "rosa", "imagen": "tienda/imagenes/vela.png", "destacado": True,
     "descripcion": "Aroma amaderado en frasco de cerámica."},
    {"id": "vela-higo", "nombre": "Vela Higo y Vainilla", "categoria": "velas",
     "precio": 12400, "tono": "terracota", "imagen": "tienda/imagenes/velaHigo.png", "destacado": False,
     "descripcion": "Dulce y cálida, para tardes de lluvia."},

    # Decoración
    {"id": "jarron-curvas", "nombre": "Jarrón Curvas", "categoria": "decoracion",
     "precio": 21500, "tono": "rosa", "imagen": "tienda/imagenes/jarron.png", "destacado": True,
     "descripcion": "Formas orgánicas hechas a mano."},
    {"id": "marco-sol", "nombre": "Marco Sol de mañana", "categoria": "decoracion",
     "precio": 9800, "tono": "crema", "imagen": "tienda/imagenes/marco.png", "destacado": False,
     "descripcion": "Marco de madera clara para fotos de 13 x 18 cm."},

    # Accesorios
    {"id": "tote-lona", "nombre": "Tote bag de lona bordada", "categoria": "accesorios",
     "precio": 11200, "tono": "crema", "imagen": "tienda/imagenes/tote.png", "destacado": False,
     "descripcion": "Lona gruesa con bordado a mano."},
    {"id": "neceser-lunares", "nombre": "Neceser Lunares", "categoria": "accesorios",
     "precio": 8700, "tono": "rosa", "imagen": "tienda/imagenes/neceser.png", "destacado": False,
     "descripcion": "Chico, resistente y fácil de lavar."},

    # Otros
    {"id": "florero-tinta", "nombre": "Florero Tinta", "categoria": "otros",
     "precio": 24900, "tono": "verde", "imagen": "tienda/imagenes/florero.png", "destacado": False,
     "descripcion": "Cerámica con trazos pintados. Edición limitada."},
]

OCASIONES = [
    {"slug": "cumpleanos", "titulo": "Cumpleaños", "tono": "rosa", "foto": "ideasregalar1.png",
     "texto": "Algo lindo, chico y que se use de verdad.",
     "productos": ["taza-lomo", "vela-higo", "marco-sol", "neceser-lunares"]},
    {"slug": "casa-nueva", "titulo": "Casa nueva", "tono": "terracota", "foto": "ideasregalar2.png",
     "texto": "Para que la primera cena en la casa nueva ya tenga mesa puesta.",
     "productos": ["bowl-amaro", "vasos-verdes", "ensaladera-hoja"]},
    {"slug": "gracias", "titulo": "Un gracias", "tono": "verde", "foto": "ideasregalar3.png",
     "texto": "Detalles que agradecen sin exagerar: una vela, una taza, una bolsa bonita.",
     "productos": ["vela-cedro", "taza-duraznillo", "tote-lona"]},
    {"slug": "aniversario", "titulo": "Aniversarios y fechas especiales", "tono": "crema", "foto": "ideasregalar4.png",
     "texto": "Piezas de diseño para las fechas que se celebran en serio.",
     "productos": ["florero-tinta", "jarron-curvas", "taza-bosque"]},
]

VALORES = [
    {"titulo": "Lindo", "tono": "rosa",
     "texto": "Elegimos cada pieza por cómo se ve, cómo se siente en la mano y cómo queda en casa."},
    {"titulo": "Útil", "tono": "terracota",
     "texto": "Objetos pensados para usarse todos los días, no para quedarse en una vitrina."},
    {"titulo": "Original", "tono": "verde",
     "texto": "Buscamos diseños y hechuras que no se vean en todos lados."},
]