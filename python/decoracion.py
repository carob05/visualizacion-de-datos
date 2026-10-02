"""Figuras de la seccion 1.3 'Visualizar no es decorar'.

1) recargado-vs-limpio.png : los mismos datos en una version recargada y en una limpia.
2) eje-truncado.png        : los mismos datos con el eje y truncado y con el eje desde cero.

Los datos son FICTICIOS y se usan solo con fines didacticos.
Factor de mentira (Tufte, 1983): efecto mostrado en el grafico / efecto en los datos.

Uso (desde la raiz del repositorio):
    python python/decoracion.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "images" / "graficos"

AZUL, GRIS, GRIS_OSCURO, NARANJA = "#2f6fb3", "#b9bec6", "#555555", "#d98a1d"

# Datos ficticios: medio de transporte usado por estudiantes (% de estudiantes)
TRANSPORTE = {"Ómnibus": 42, "A pie": 25, "Bicicleta": 14, "Auto": 12, "Moto": 7}


def recargado(eje):
    nombres, valores = list(TRANSPORTE), list(TRANSPORTE.values())
    colores = ["#ff2d55", "#34c759", "#ffcc00", "#af52de", "#00c7be"]
    eje.set_facecolor("#cfe8ff")
    x = np.arange(len(nombres))
    eje.bar(x + 0.08, valores, width=0.7, color="#777777", alpha=0.6, zorder=2)  # sombra
    barras = eje.bar(x, valores, width=0.7, color=colores, edgecolor="black",
                     linewidth=2.2, hatch="//", zorder=3)
    for barra, v in zip(barras, valores):
        eje.text(barra.get_x() + barra.get_width() / 2, v + 1.2, f"{v}%", ha="center",
                 fontsize=11, fontweight="bold", color="#b00020", zorder=4)
    eje.set_xticks(x)
    eje.set_xticklabels(nombres, rotation=45, ha="right", fontweight="bold")
    eje.set_ylim(0, 50)
    eje.set_yticks(range(0, 51, 5))
    eje.grid(axis="y", color="black", lw=1.4, ls="--", zorder=1)
    eje.set_ylabel("PORCENTAJE (%)", fontweight="bold")
    eje.set_title("¡¡ MEDIOS DE TRANSPORTE !!", fontsize=13, fontweight="bold",
                  color="#b00020", pad=10)
    for lado in eje.spines.values():
        lado.set_linewidth(3)
    eje.legend(barras, nombres, title="Medio", loc="upper right", fontsize=8, framealpha=1)


def limpio(eje):
    # De mayor a menor, para que el orden cuente la historia
    items = sorted(TRANSPORTE.items(), key=lambda kv: kv[1])
    nombres, valores = [k for k, _ in items], [v for _, v in items]
    colores = [AZUL if v == max(valores) else GRIS for v in valores]
    y = np.arange(len(nombres))
    eje.barh(y, valores, color=colores, height=0.62)
    for yi, v, n in zip(y, valores, nombres):
        eje.text(v + 0.8, yi, f"{v} %", va="center", fontsize=11,
                 fontweight="bold" if v == max(valores) else "normal",
                 color=AZUL if v == max(valores) else GRIS_OSCURO)
    eje.set_yticks(y)
    eje.set_yticklabels(nombres, fontsize=11)
    eje.set_xlim(0, 50)
    eje.tick_params(left=False, bottom=False, labelbottom=False)
    for lado in eje.spines.values():
        lado.set_visible(False)
    eje.set_title("El ómnibus es el medio de transporte\nmás usado por los estudiantes",
                  loc="left", fontsize=12, fontweight="bold", pad=12)
    eje.text(0, 1.02, "", transform=eje.transAxes)


def figura_recargado_vs_limpio():
    fig, (a, b) = plt.subplots(1, 2, figsize=(10.5, 4.9), gridspec_kw={"width_ratios": [1.05, 1]})
    fig.patch.set_facecolor("white")
    recargado(a)
    limpio(b)
    fig.text(0.02, 0.965, "Antes: versión recargada", fontsize=11, color=GRIS_OSCURO, fontweight="bold")
    fig.text(0.54, 0.965, "Después: versión limpia", fontsize=11, color=GRIS_OSCURO, fontweight="bold")
    fig.text(0.02, 0.01,
             "Datos ficticios con fines didácticos: % de estudiantes por medio de transporte. "
             "El gráfico de la izquierda está exagerado a propósito.",
             fontsize=8, color=GRIS_OSCURO)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    destino = SALIDA / "recargado-vs-limpio.png"
    fig.savefig(destino, dpi=200)
    print("Figura guardada en:", destino)


def figura_eje_truncado():
    etiquetas, valores = ["Enero", "Febrero"], [95, 100]
    efecto_datos = (valores[1] - valores[0]) / valores[0]
    base = 90
    efecto_grafico = ((valores[1] - base) - (valores[0] - base)) / (valores[0] - base)
    factor = efecto_grafico / efecto_datos

    fig, (a, b) = plt.subplots(1, 2, figsize=(9.5, 4.4))
    for eje, ymin, titulo in ((a, base, f"Eje desde {base}"), (b, 0, "Eje desde 0")):
        barras = eje.bar(etiquetas, valores, color=[GRIS, AZUL], width=0.55)
        eje.set_ylim(ymin, 105)
        for barra, v in zip(barras, valores):
            eje.text(barra.get_x() + barra.get_width() / 2, v + 0.8, str(v), ha="center", fontweight="bold")
        eje.set_title(titulo, loc="left", fontsize=11, fontweight="bold", pad=24)
        eje.set_ylabel("Ventas (miles de unidades)")
        for lado in ("top", "right"):
            eje.spines[lado].set_visible(False)
    a.text(0, 1.03, "Febrero parece el doble de enero", transform=a.transAxes, va="bottom",
           color=NARANJA, fontweight="bold", fontsize=10)
    b.text(0, 1.03, "La diferencia real es de 5,3 %", transform=b.transAxes, va="bottom",
           color=NARANJA, fontweight="bold", fontsize=10)
    fig.text(0.02, 0.01,
             ("Datos ficticios. Efecto en los datos: " + f"{efecto_datos:.1%}".replace(".", ",")
              + ". Efecto en el gráfico de la izquierda: " + f"{efecto_grafico:.0%}"
              + f". Factor de mentira: {factor:.0f}."),
             fontsize=8, color=GRIS_OSCURO)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    destino = SALIDA / "eje-truncado.png"
    fig.savefig(destino, dpi=200)
    print("Figura guardada en:", destino)
    print(f"efecto datos={efecto_datos:.4f} efecto grafico={efecto_grafico:.4f} factor={factor:.2f}")


if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    figura_recargado_vs_limpio()
    figura_eje_truncado()
