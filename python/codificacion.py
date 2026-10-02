"""Figura 'de la tabla al grafico': cada fila se convierte en una marca (un punto)
y cada valor en una posicion.

Usa el conjunto I del cuarteto de Anscombe (1973), el mismo de la seccion 1.1.
Fuente de los datos: https://doi.org/10.1080/00031305.1973.10478966

Uso (desde la raiz del repositorio):
    python python/codificacion.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch

from anscombe import DATOS

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "images" / "graficos"

AZUL, NARANJA, GRIS = "#2f6fb3", "#d98a1d", "#555555"
FILA_DESTACADA = 7  # indice de la fila (0 a 10) que se resalta: x = 4, y = 4,26


def fmt(valor):
    return f"{valor:g}".replace(".", ",") if float(valor).is_integer() else f"{valor:.2f}".replace(".", ",")


def graficar():
    SALIDA.mkdir(parents=True, exist_ok=True)
    x, y = DATOS["I"]
    fig = plt.figure(figsize=(9, 5.2))
    eje_t = fig.add_axes([0.03, 0.10, 0.34, 0.78])
    eje_g = fig.add_axes([0.52, 0.16, 0.45, 0.68])

    # --- Tabla (izquierda) ---
    eje_t.axis("off")
    eje_t.set_xlim(0, 1)
    eje_t.set_ylim(0, len(x) + 1.2)
    eje_t.text(0.30, len(x) + 0.55, "x", ha="center", va="center", fontweight="bold", fontsize=11)
    eje_t.text(0.72, len(x) + 0.55, "y", ha="center", va="center", fontweight="bold", fontsize=11)
    eje_t.plot([0.05, 0.95], [len(x) + 0.05, len(x) + 0.05], color=GRIS, lw=1)
    for i, (xi, yi) in enumerate(zip(x, y)):
        yy = len(x) - 0.5 - i
        destacada = i == FILA_DESTACADA
        if destacada:
            eje_t.add_patch(plt.Rectangle((0.05, yy - 0.42), 0.90, 0.84, color=NARANJA, alpha=0.25, lw=0))
        color = NARANJA if destacada else "black"
        peso = "bold" if destacada else "normal"
        eje_t.text(0.30, yy, fmt(xi), ha="center", va="center", color=color, fontweight=peso, fontsize=10.5)
        eje_t.text(0.72, yy, fmt(yi), ha="center", va="center", color=color, fontweight=peso, fontsize=10.5)
    eje_t.set_title("Datos: una tabla (cada fila es una observación)", loc="left", fontsize=10, color=GRIS)

    # --- Grafico (derecha) ---
    for i, (xi, yi) in enumerate(zip(x, y)):
        d = i == FILA_DESTACADA
        eje_g.scatter(xi, yi, s=90 if d else 46, color=NARANJA if d else AZUL,
                      edgecolor="white", linewidth=0.8, zorder=3)
    eje_g.set_xlim(2, 16)
    eje_g.set_ylim(2, 12)
    eje_g.set_xlabel("x  (posición horizontal)")
    eje_g.set_ylabel("y  (posición vertical)")
    eje_g.grid(alpha=0.25)
    for lado in ("top", "right"):
        eje_g.spines[lado].set_visible(False)
    eje_g.set_title("Gráfico: cada fila es un punto", loc="left", fontsize=10, color=GRIS)

    xd, yd = x[FILA_DESTACADA], y[FILA_DESTACADA]
    eje_g.annotate(
        "Una marca (un punto)\ncuya posición codifica\nx = 4 e y = 4,26",
        xy=(xd, yd), xytext=(6.3, 2.6), fontsize=9.5, color=NARANJA,
        arrowprops=dict(arrowstyle="->", color=NARANJA, lw=1.4),
    )

    # --- Flecha entre la fila y el punto ---
    yy = len(x) - 0.5 - FILA_DESTACADA
    fig.add_artist(ConnectionPatch(
        xyA=(0.95, yy), coordsA=eje_t.transData,
        xyB=(xd, yd), coordsB=eje_g.transData,
        arrowstyle="-|>", color=NARANJA, lw=1.4, linestyle="--", mutation_scale=14,
    ))

    fig.text(0.03, 0.01, "Datos: conjunto I de Anscombe (1973). Elaboración propia.",
             fontsize=8, color=GRIS)
    destino = SALIDA / "tabla-a-grafico.png"
    fig.savefig(destino, dpi=200)
    print(f"Figura guardada en: {destino}")


if __name__ == "__main__":
    graficar()
