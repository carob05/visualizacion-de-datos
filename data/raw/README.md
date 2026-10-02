# Datos en bruto

## nightingale.csv

Mortalidad mensual del ejército británico en la Guerra de Crimea (abril de 1854 a marzo de 1856).

- **Fuente de las cifras originales:** Nightingale, F. (1858). *Notes on Matters Affecting the Health, Efficiency, and Hospital Administration of the British Army*, y Nightingale, F. (1859). *A Contribution to the Sanitary History of the British Army during the Late War with Russia*.
- **Versión digitalizada:** conjunto `Nightingale` del paquete de R [HistData](https://CRAN.R-project.org/package=HistData) (Friendly, Dray, Li y Bellhouse), copia distribuida en [Rdatasets](https://vincentarelbundock.github.io/Rdatasets/).
- **Licencia de HistData:** GPL. Si publicas el repositorio, conserva esta atribución y revisa que sea compatible con la licencia que elijas para el libro.
- **Variables:** `Army` (tamaño medio mensual del ejército), `Disease`, `Wounds`, `Other` (muertes por enfermedad prevenible, heridas y otras causas), y las tasas anuales por 1000 (`*.rate`, calculadas como 12 * 1000 * muertes / Army).
