"""Cuarteto de Anscombe: calcula las estadísticas y genera la figura del capitulo 1.

Fuente de los datos:
Anscombe, F. J. (1973). Graphs in Statistical Analysis.
The American Statistician, 27(1), 17-21. https://doi.org/10.1080/00031305.1973.10478966

Uso (desde la raíz del repositorio):
    python python/anscombe.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Los conjuntos I, II y III comparten los mismos valores de x.
X123 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
X4 = [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8]

DATOS = {
    "I": (X123, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II": (X123, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": (X123, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV": (X4, [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "images" / "graficos"


def estadisticas(x, y):
    """Devuelve media, varianza (muestral), correlacion y recta de regresion."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    pendiente, ordenada = np.polyfit(x, y, 1)
    return {
        "media_x": x.mean(),
        "var_x": x.var(ddof=1),
        "media_y": y.mean(),
        "var_y": y.var(ddof=1),
        "r": np.corrcoef(x, y)[0, 1],
        "ordenada": ordenada,
        "pendiente": pendiente,
    }


def imprimir_tabla():
    print(f"{'Conjunto':<9}{'media x':>8}{'var x':>8}{'media y':>9}{'var y':>8}{'r':>8}  recta")
    for nombre, (x, y) in DATOS.items():
        e = estadisticas(x, y)
        print(
            f"{nombre:<9}{e['media_x']:>8.2f}{e['var_x']:>8.2f}{e['media_y']:>9.2f}"
            f"{e['var_y']:>8.3f}{e['r']:>8.3f}  y = {e['ordenada']:.2f} + {e['pendiente']:.3f}x"
        )


def graficar():
    SALIDA.mkdir(parents=True, exist_ok=True)
    azul, gris = "#2f6fb3", "#8a8a8a"
    fig, ejes = plt.subplots(2, 2, figsize=(8, 6.4), sharex=True, sharey=True)

    for eje, (nombre, (x, y)) in zip(ejes.ravel(), DATOS.items()):
        e = estadisticas(x, y)
        xs = np.array([3, 20])
        eje.plot(xs, e["ordenada"] + e["pendiente"] * xs, color=gris, lw=1.6, ls="--", zorder=1)
        eje.scatter(x, y, color=azul, s=46, edgecolor="white", linewidth=0.8, zorder=2)
        eje.set_title(f"Conjunto {nombre}", loc="left", fontsize=11, fontweight="bold")
        eje.set_xlim(3, 20)
        eje.set_ylim(2, 14)
        eje.set_xticks([5, 10, 15, 20])
        eje.grid(alpha=0.25)
        for lado in ("top", "right"):
            eje.spines[lado].set_visible(False)

    for eje in ejes[1]:
        eje.set_xlabel("x")
    for eje in ejes[:, 0]:
        eje.set_ylabel("y")

    fig.suptitle(
        "Cuatro conjuntos con la misma recta: y = 3,00 + 0,50x",
        fontsize=13,
        fontweight="bold",
        x=0.01,
        ha="left",
    )
    fig.text(
        0.01, 0.005,
        "Fuente: Anscombe (1973). La línea punteada es la recta de regresión de cada conjunto.",
        fontsize=8, color="#555555", ha="left",
    )
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    destino = SALIDA / "anscombe-cuarteto.png"
    fig.savefig(destino, dpi=200)
    print(f"Figura guardada en: {destino}")


if __name__ == "__main__":
    imprimir_tabla()
    graficar()
