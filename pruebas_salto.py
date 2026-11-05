"""Reproduce los cinco experimentos sin abrir la interfaz gráfica."""
import csv
import platform
from pathlib import Path
import numpy as np
from salto_modelo import RedSalto
from salto_juego import JuegoSalto

FRAMES = 9000

class RedVentana(RedSalto):
    def __init__(self, ventana=(7, 13), **kwargs):
        self.ventana = ventana
        super().__init__(**kwargs)

    def etiqueta(self, distancia, velocidad):
        t = np.asarray(distancia) / np.maximum(np.asarray(velocidad), 0.001)
        lo, hi = self.ventana
        return ((t >= lo) & (t <= hi)).astype(float).reshape(-1, 1)

    def generar_datos(self, n=5000):
        v = self.rng.uniform(4.5, 8.5, n)
        lo, hi = self.ventana
        t = np.concatenate((self.rng.uniform(lo + .5, hi - .5, n // 2),
                            self.rng.uniform(0, 60, n - n // 2)))
        self.rng.shuffle(t)
        return self.preparar_entradas(v * t, v), self.etiqueta(v * t, v)


def simular(red):
    juego = JuegoSalto()
    for _ in range(FRAMES):
        if red.probabilidad(juego.distancia, juego.velocidad) >= .5 and juego.en_suelo:
            juego.saltar()
        juego.actualizar()
    return juego.esquivados, juego.choques


def medir(red, X, y, grupo, ventana):
    p = np.clip(red.adelante(X)[2], 1e-8, 1 - 1e-8)
    loss = -np.mean(y * np.log(p) + (1-y)*np.log(1-p))
    esquivados, choques = simular(red)
    return dict(experimento=grupo, ocultas=red.ocultas, tasa=red.tasa,
                ventana=ventana, epocas=red.epocas, perdida_prueba=round(float(loss), 6),
                precision_pct=round(red.precision(X, y)*100, 2),
                esquivados=esquivados, choques=choques)


def ejecutar():
    filas = []
    # Exactamente los datos y la inicialización de saltar.py.
    red = RedSalto()
    X, y = red.generar_datos(5000)
    Xt, yt = red.generar_datos(1500)
    for epoca in range(501):
        if epoca % 100 == 0:
            filas.append(medir(red, Xt, yt, '1-2 entrenamiento', '7-13'))
        if epoca < 500:
            red.entrenar_epoca(X, y)
    # Mismos datos para comparar arquitectura y tasa, sin confundir el efecto.
    for grupo, ocultas, tasa in [('3 arquitectura', 3, .8), ('3 arquitectura', 24, .8),
                                 ('4 tasa', 12, .01), ('4 tasa', 12, 1.2)]:
        red = RedSalto(ocultas=ocultas, tasa=tasa)
        for _ in range(500):
            red.entrenar_epoca(X, y)
        filas.append(medir(red, Xt, yt, grupo, '7-13'))
    for ventana in [(2, 5), (20, 26)]:
        red = RedVentana(ventana=ventana)
        Xv, yv = red.generar_datos(5000)
        Xvt, yvt = red.generar_datos(1500)
        for _ in range(500):
            red.entrenar_epoca(Xv, yv)
        filas.append(medir(red, Xvt, yvt, '5 ventana', f'{ventana[0]}-{ventana[1]}'))
    destino = Path(__file__).with_name('resultados_pruebas.csv')
    with destino.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0]))
        writer.writeheader()
        writer.writerows(filas)
    print(f'Python {platform.python_version()} / NumPy {np.__version__} / {FRAMES} frames por evaluación')
    for fila in filas:
        print(fila)

if __name__ == '__main__':
    ejecutar()
