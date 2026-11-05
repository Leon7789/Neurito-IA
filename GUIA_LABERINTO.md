# Neurito 3.0: aprende a encontrar comida en un laberinto

Neurito busca comida dentro de tres laberintos. Su cerebro debe elegir entre arriba, abajo, izquierda y derecha. La red se construye con NumPy, y Pygame dibuja el escenario, la mascota y una gráfica de la pérdida.

## Cómo aprende

1. BFS calcula rutas cortas y genera ejemplos etiquetados: mapa, posición, meta y movimiento recomendado.
2. Los ejemplos se dividen en entrenamiento (80 %) y prueba (20 %). Los pares posición-meta de prueba no aparecen en entrenamiento.
3. Cada entrada incluye un vector one-hot de tres mapas y dos vectores one-hot de 81 casillas: 165 características.
4. La arquitectura es 165 → 96 → 4. Usa ReLU en la capa oculta y Softmax en las cuatro salidas.
5. El entrenamiento minimiza entropía cruzada multiclase mediante retropropagación y descenso de gradiente con mini-lotes.
6. Durante el juego, el modelo decide sin consultar BFS. BFS es el experto que proporcionó las etiquetas.

Esto es aprendizaje supervisado por imitación, NO aprendizaje por refuerzo.

## Dos modos

- Red pura: toma la salida de mayor probabilidad. Puede chocar con paredes o quedarse en ciclos.
- Asistido: descarta movimientos contra paredes y penaliza casillas visitadas. Son reglas adicionales, no conocimientos aprendidos por la red.

La precisión de clasificación no equivale al porcentaje de laberintos completados.

## Estructura

- laberinto_mundo.py: mapas, movimiento, BFS y navegación asistida.
- laberinto_red.py: red neuronal y entrenamiento con NumPy.
- laberinto.py: juego Pygame, sprites y pérdida.
- test_laberinto.py: pruebas automáticas.
- GUIA_LABERINTO.md: esta guía.

Reutiliza assets/neutral_1.png, neutral_2.png y neutral_3.png. No modifica las versiones anteriores.

## Ejecutar

    uv sync
    uv run laberinto.py

## Controles

| Tecla | Acción |
|---|---|
| 1 | Entrenar una época |
| 2 | Entrenar cien épocas |
| 3 | Entrenamiento continuo |
| A | Alternar red pura y navegación asistida |
| P | Alternar navegación automática y paso a paso |
| Espacio | Avanzar un paso en modo manual |
| N | Cambiar mapa |
| G | Nuevas posiciones y meta |
| C | Reiniciar contadores |
| R | Reiniciar pesos y entrenamiento |
| Esc | Salir |

## Probar automáticamente

    uv run python -m unittest -v test_laberinto.py

## Experimentos

## 1. Observa Neurito sin entrenar. ¿Por qué se atasca?
La red elige movimientos dando pasos aleatorios y no sabe donde esta la comida,se choca contra las apredes o atraviesa casillas
## 2. Entrena 100, 200 y 400 épocas. Compara pérdida, precisión y movimientos.
Al aumentar las épocas, la pérdida disminuyó y la precisión mejoró. Desde las 300 épocas no hubo choques durante esta evaluación. Después siguió mejorando la clasificación, aunque el contador de obstáculos esquivados se mantuvo igual.
## 3. Compara red pura frente a navegación asistida. ¿Qué parte corresponde al modelo y cuál a las reglas?
La red pura escoge la dirección con mayor probabilidad predicha. La asistida aplica dos reglas adicionales, no permite atravesar paredes y resta puntuación a las casillas ya visitadas. Tras 400 épocas, la red pura completó 82,68 % y la asistida 99,58 %. Respuesta: el aprendizaje está en los pesos de la red; las restricciones y penalizaciones de la asistencia son reglas programadas, no aprendizaje neuronal.

## 4. Cambia las 96 neuronas ocultas por 16, 32 o 128.
Con 16 neuronas la red tiene menos capacidad para aprender patrones. Al aumentar a 32 mejoró la precisión; usar 128 no garantizó un mejor resultado en prueba. Una red más grande no siempre generaliza mejor.
## 5. Cambia la tasa de aprendizaje 0.45 y observa si converge.
n este experimento, 0,10 aprendió más despacio; 0,45 tuvo buen desempeño y 0,90 convergió más rápido y obtuvo mejor precisión. Esto no significa que aumentar la tasa siempre sea mejor donde tasas demasiado altas pueden volver inestable el entrenamiento.

## 6. Cambia de mapa. Los mapas forman parte del entrenamiento, pero las combinaciones de inicio y meta usadas para probar no se entrenaron.
El proyecto entrena con ejemplos de los tres mapas, por eso puede resolver nuevas combinaciones de inicio y comida en esos mapas. La prueba automática confirmó que los 716 ejemplos de prueba no se repiten en entrenamiento. Sin embargo, esto no demuestra que pueda resolver un mapa completamente nuevo, ya que la entrada incluye el identificador de los tres mapas conocidos.
## 7. Haz vibecoding para verificar como mejora o empeora Neurito al cambiar DFS, por BFS y A*
DFS encuentra un camino, pero no necesariamente el más corto. BFS sí encuentra rutas mínimas en estos laberintos de movimientos con costo uniforme. A* también encontró rutas mínimas y exploró menos nodos en promedio gracias a la heurística. El modelo original usa BFS para generar etiquetas: sustituir BFS por DFS podría darle ejemplos de rutas menos eficientes. A* puede generar rutas óptimas con menor exploración en estos casos.

## Alcance y limitaciones

El modelo no interpreta capturas de pantalla: trabaja con características estructuradas. Conoce el identificador de cada mapa. Los tres mapas pertenecen al mismo universo de entrenamiento. La evaluación demuestra generalización a pares de posición-meta no entrenados, no a laberintos totalmente desconocidos. Para eso habría que representar también las paredes de cualquier mapa nuevo y entrenar y evaluar en mapas separados.
