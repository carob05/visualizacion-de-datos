"""Figuras de la seccion 1.4 'De los datos a una historia'.

Datos: muertes mensuales del ejercito britanico en la Guerra de Crimea
(abril de 1854 a marzo de 1856), del paquete de R HistData (conjunto 'Nightingale'),
que recoge las cifras publicadas por Florence Nightingale en 1858 y 1859.
Las tasas son anuales por 1000 soldados: 12 * 1000 * muertes / tamano del ejercito.

Genera dos figuras con LOS MISMOS datos:
  nightingale-exploratoria.png : para explorar (sin mensaje).
  nightingale-explicativa.png  : para comunicar (con un mensaje claro).

Uso (desde la raiz del repositorio):
    python python/historia.py
"""

import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data" / "raw" / "nightingale.csv"
SALIDA = RAIZ / "images" / "graficos"

AZUL, NARANJA, GRIS, GRIS_OSCURO = "#2f6fb3", "#d98a1d", "#9aa0a8", "#555555"
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
REFORMA = datetime(1855, 3, 1)  # llega la Comision Sanitaria


def cargar():
    filas = []
    with open(DATOS, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            filas.append({
                "fecha": datetime.strptime(r["Date"], "%Y-%m-%d"),
                "enfermedad": float(r["Disease.rate"]),
                "heridas": float(r["Wounds.rate"]),
                "otras": float(r["Other.rate"]),
                "muertes_enf": int(r["Disease"]),
                "muertes_her": int(r["Wounds"]),
                "muertes_otras": int(r["Other"]),
            })
    return filas


def miles(valor):
    return f"{valor:,.0f}".replace(",", ".")


def formato_eje(eje, fechas):
    eje.set_xticks(fechas[::3])
    eje.set_xticklabels([f"{MESES[d.month - 1]}\n{d.year}" for d in fechas[::3]], fontsize=8.5)
    eje.yaxis.set_major_formatter(lambda v, _: miles(v))


def figura_exploratoria(filas):
    f = [r["fecha"] for r in filas]
    fig, eje = plt.subplots(figsize=(9, 4.6))
    eje.plot(f, [r["enfermedad"] for r in filas], color=AZUL, lw=1.8, marker="o", ms=3, label="Enfermedad")
    eje.plot(f, [r["heridas"] for r in filas], color=NARANJA, lw=1.8, marker="o", ms=3, label="Heridas")
    eje.plot(f, [r["otras"] for r in filas], color=GRIS, lw=1.8, marker="o", ms=3, label="Otras causas")
    eje.set_title("Muertes por causa y por mes", loc="left", fontsize=12)
    eje.set_ylabel("Tasa anual por 1.000 soldados")
    eje.grid(alpha=0.3)
    eje.legend(frameon=False)
    formato_eje(eje, f)
    for lado in ("top", "right"):
        eje.spines[lado].set_visible(False)
    fig.text(0.01, 0.01, "Datos: HistData (Nightingale), a partir de Nightingale (1858, 1859).",
             fontsize=8, color=GRIS_OSCURO)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    destino = SALIDA / "nightingale-exploratoria.png"
    fig.savefig(destino, dpi=200)
    print("Figura guardada en:", destino)


def figura_explicativa(filas):
    f = [r["fecha"] for r in filas]
    enf = [r["enfermedad"] for r in filas]
    total_enf = sum(r["muertes_enf"] for r in filas)
    total = total_enf + sum(r["muertes_her"] + r["muertes_otras"] for r in filas)

    fig, eje = plt.subplots(figsize=(9, 5.2))
    eje.axvspan(f[0], REFORMA, color="#f1f3f6", zorder=0)
    eje.plot(f, enf, color=AZUL, lw=3, zorder=3)
    eje.plot(f, [r["heridas"] for r in filas], color=NARANJA, lw=2.2, zorder=3)
    eje.plot(f, [r["otras"] for r in filas], color=GRIS, lw=1.6, zorder=2)

    # Etiquetas directas, en lugar de leyenda
    eje.text(f[14], 290, "Enfermedades", color=AZUL, fontweight="bold", ha="center", fontsize=10.5)
    eje.text(f[19], 105, "Heridas de guerra", color=NARANJA, fontweight="bold", ha="center", fontsize=10.5)
    eje.text(f[8], 190, "Otras causas", color=GRIS_OSCURO, ha="center", fontsize=9.5)

    # Linea de la reforma
    eje.axvline(REFORMA, color=GRIS_OSCURO, ls="--", lw=1.2, zorder=1)
    eje.text(REFORMA, 1140, " Marzo de 1855:\n llega la Comisión Sanitaria", va="top", fontsize=9.5,
             color=GRIS_OSCURO)

    # Punto maximo
    imax = enf.index(max(enf))
    eje.annotate(f"Enero de 1855: {miles(enf[imax])}", xy=(f[imax], enf[imax]), xytext=(f[2], 1010),
                 fontsize=9.5, color=AZUL, fontweight="bold",
                 arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.2))

    eje.set_ylim(0, 1200)
    eje.set_xlim(f[0], f[-1])
    formato_eje(eje, f)
    eje.set_ylabel("Muertes por año por cada 1.000 soldados\n(tasa anualizada)", fontsize=9.5)
    for lado in ("top", "right"):
        eje.spines[lado].set_visible(False)
    eje.grid(axis="y", alpha=0.25)

    fig.suptitle("Las enfermedades, no el combate, causaron la mayoría de las muertes\n"
                 "del ejército británico en Crimea, y cayeron tras las reformas sanitarias",
                 x=0.01, ha="left", fontsize=12.5, fontweight="bold")
    fig.text(0.01, 0.012,
             f"Datos: HistData (Nightingale), a partir de Nightingale (1858, 1859). "
             f"En estos 24 meses, {total_enf / total:.0%} de las muertes registradas fueron por enfermedad.",
             fontsize=8, color=GRIS_OSCURO)
    fig.tight_layout(rect=(0, 0.04, 1, 0.86))
    fig.subplots_adjust(top=0.80)
    destino = SALIDA / "nightingale-explicativa.png"
    fig.savefig(destino, dpi=200)
    print("Figura guardada en:", destino)


def resumen(filas):
    for nombre, sel in (("abr 1854 - mar 1855", [r for r in filas if r["fecha"] < datetime(1855, 4, 1)]),
                        ("abr 1855 - mar 1856", [r for r in filas if r["fecha"] >= datetime(1855, 4, 1)])):
        e = sum(r["muertes_enf"] for r in sel)
        h = sum(r["muertes_her"] for r in sel)
        print(f"{nombre}: enfermedad {e}, heridas {h}, razon {e / h:.1f}")


if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    datos = cargar()
    resumen(datos)
    figura_exploratoria(datos)
    figura_explicativa(datos)
