# Neurito 2.0: aprende a saltar

Este proyecto utiliza una red neuronal para decidir cuándo saltar un obstáculo. La mascota original de `main.py` decide entre comer, dormir y jugar. La versión nueva agrega un juego de saltos y permite observar cómo cambia su comportamiento al entrenar.

## Funcionamiento

La red recibe distancia, velocidad y tiempo estimado hasta el obstáculo. Normaliza las entradas y usa una arquitectura de **3 entradas, 12 neuronas ocultas y 1 salida**. La capa oculta usa ReLU y la salida usa sigmoide. Si la salida es mayor o igual a 0.5, intenta saltar.

Es aprendizaje supervisado: se generan ejemplos con etiquetas de saltar o esperar. La regla original indica saltar cuando faltan entre 7 y 13 fotogramas para llegar al obstáculo. Los pesos se ajustan con retropropagación y descenso de gradiente; los choques no actualizan la red como una recompensa.

## Archivos

| Archivo | Función |
|---|---|
| `main.py` | Mascota original: comer, dormir y jugar. |
| `salto_modelo.py` | Red neuronal, datos, entrenamiento y precisión. |
| `salto_juego.py` | Movimiento, gravedad, salto, obstáculos y colisiones. |
| `saltar.py` | Interfaz del juego con Pygame. |
| `pruebas_salto.py` | Ejecuta los cinco experimentos sin abrir una ventana. |
| `resultados_pruebas.csv` | Resultados obtenidos durante las pruebas. |
| `GUIA_SALTO.md` | Guía de uso y experimentos propuestos. |
| `assets/` | Imágenes de la mascota. |

## Ejecución

Desde la carpeta del proyecto, con Python 3.12 o superior y uv:

```bash
uv sync
uv run saltar.py
```

Para abrir la mascota original:

```bash
uv run main.py
```

Para reproducir los experimentos y generar nuevamente el CSV:

```bash
uv run pruebas_salto.py
```

Se conservan las dependencias originales de `pyproject.toml` y `uv.lock`. Las pruebas documentadas aquí se ejecutaron con Python 3.12.14 y NumPy 2.3.5 del entorno disponible, sin Pygame. Por eso se verificaron el modelo y la física, pero no la interfaz gráfica ni la instalación mediante `uv sync`.

## Controles del juego

| Tecla | Acción |
|---|---|
| 1 | Entrenar una época. |
| 2 | Entrenar cien épocas. |
| 3 | Activar o pausar entrenamiento continuo. |
| A | Alternar entre automático y manual. |
| Espacio | Saltar en modo manual. |
| C | Reiniciar pista y contadores. |
| R | Reiniciar pesos y contadores. |
| Esc | Salir. |

## Pruebas resueltas

Se utilizaron 5.000 ejemplos de entrenamiento y 1.500 de prueba, independientes del entrenamiento. Cada evaluación del juego comienza con una pista nueva y dura 9.000 fotogramas: equivale a cinco minutos a 30 FPS, aunque la simulación se ejecuta sin esperar ese tiempo. Se mantienen las semillas del proyecto: 42 para la red y 19 para la pista.

La pérdida de estas tablas se calcula sobre el conjunto de prueba después del entrenamiento. No es exactamente el último valor mostrado en la interfaz, que corresponde al entrenamiento antes de la última actualización de pesos. Los resultados corresponden a una semilla y no garantizan el mismo desempeño en cualquier escenario.

### 1. Juego sin entrenar

La red obtuvo **44,93 % de precisión, 0 obstáculos esquivados y 59 choques**. Los pesos iniciales todavía no representan la relación entre la distancia, la velocidad y el momento de saltar.

### 2. Entrenamiento de cien en cien épocas

| Épocas | Pérdida de prueba | Precisión | Esquivados | Choques |
|---:|---:|---:|---:|---:|
| 0 | 0,711350 | 44,93 % | 0 | 59 |
| 100 | 0,272084 | 91,20 % | 67 | 5 |
| 200 | 0,242181 | 91,87 % | 72 | 1 |
| 300 | 0,217284 | 92,33 % | 74 | 0 |
| 400 | 0,185093 | 92,60 % | 74 | 0 |
| 500 | 0,146009 | 94,13 % | 74 | 0 |

Al aumentar las épocas, la pérdida disminuyó y la precisión mejoró. Desde las 300 épocas no hubo choques durante esta evaluación. Después siguió mejorando la clasificación, aunque el contador de obstáculos esquivados se mantuvo igual.

### 3. Cambiar la cantidad de neuronas ocultas

Se entrenaron las tres arquitecturas durante 500 épocas, con tasa 0.8 y los mismos datos de entrenamiento y prueba.

| Neuronas ocultas | Pérdida de prueba | Precisión | Esquivados | Choques |
|---:|---:|---:|---:|---:|
| 3 | 0,223053 | 92,80 % | 74 | 0 |
| 12 | 0,146009 | 94,13 % | 74 | 0 |
| 24 | 0,101573 | 96,33 % | 74 | 0 |

La red con 24 neuronas clasificó mejor los ejemplos que no usó para entrenar. Sin embargo, las tres redes terminaron esta simulación sin choques. Más neuronas no produjeron más obstáculos esquivados en esta prueba. Una sola ejecución no demuestra que una arquitectura siempre generalice mejor.

### 4. Modificar la tasa de aprendizaje

Se mantuvieron 12 neuronas ocultas, los mismos datos y 500 épocas.

| Tasa | Pérdida de prueba | Precisión | Esquivados | Choques |
|---:|---:|---:|---:|---:|
| 0.01 | 0,518213 | 85,87 % | 0 | 56 |
| 0.8 | 0,146009 | 94,13 % | 74 | 0 |
| 1.2 | 0,098650 | 95,33 % | 74 | 0 |

Con 0.01, los ajustes fueron pequeños y 500 épocas no bastaron para conseguir un buen comportamiento en el juego. Con 1.2 se obtuvo menor pérdida final que con 0.8. En esta ejecución la tasa mayor funcionó bien; eso no significa que aumentarla siempre mejore el aprendizaje, porque puede generar oscilaciones o impedir la convergencia.

### 5. Cambiar la ventana de entrenamiento

Para modificar la ventana se cambió tanto la etiqueta como el intervalo usado para generar los ejemplos positivos. El script lo hace mediante `RedVentana`, sin alterar el modelo original. Todas las variantes usan 12 neuronas, tasa 0.8 y 500 épocas.

| Ventana, en fotogramas | Pérdida de prueba | Precisión | Esquivados | Choques |
|---|---:|---:|---:|---:|
| 7 a 13, original | 0,146009 | 94,13 % | 74 | 0 |
| 2 a 5, más tarde | 0,113308 | 96,67 % | 74 | 0 |
| 20 a 26, más temprano | 0,083946 | 96,80 % | 0 | 58 |

La ventana de 2 a 5 funcionó en esta pista. La de 20 a 26 tuvo buena precisión, pero el salto anticipado produjo choques: el personaje puede estar descendiendo cuando el obstáculo lo alcanza. Cada precisión se calcula frente a las etiquetas de su propia ventana; no son exactamente la misma tarea de clasificación.

### Pregunta central: ¿por qué una red puede tener buena precisión y aun así chocar?

Porque la precisión mide si la red imita las etiquetas de entrenamiento, no si completa el salto sin chocar. Si las etiquetas enseñan a saltar demasiado temprano, la red puede aprender esa regla con mucha precisión y fallar en el juego. También influyen la gravedad, el impulso, el tamaño de los objetos y que solo se puede saltar desde el suelo. Además, un error en un instante crítico puede causar una colisión aunque la mayoría de las predicciones sean correctas.

La prueba de la ventana de 20 a 26 lo muestra: obtuvo **96,80 % de precisión y 58 choques**. Por eso hay que revisar tanto la clasificación como el comportamiento real.

## Conclusión

El entrenamiento mejoró el comportamiento de Neurito. Con la configuración original, 500 épocas permitieron esquivar 74 obstáculos sin choques en la simulación. Las pruebas también mostraron que una buena precisión no basta: la regla usada para enseñar debe ser compatible con la física del juego.

## Entrega en GitHub

Rama preparada localmente: `pruebas-neurito-readme`.

El envío al repositorio, la creación del pull request y el merge quedan pendientes de disponer del repositorio destino y del acceso a GitHub. Este documento no presenta esas acciones como realizadas ni incluye enlaces inventados.
