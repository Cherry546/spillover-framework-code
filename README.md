# Code for the spillover framework manuscript

This repository contains Python code for the illustrative figures in the spillover framework manuscript.

## Figures

| Figure | Code file | Content |
| --- | --- | --- |
| Figure 2 | [fig2_seasonality.py](fig2_seasonality.py) | Illustrative seasonality in relative exposure opportunity |
| Figure 3 | [fig3_spatial_drivers.py](fig3_spatial_drivers.py) | Synthetic illustration of spatial drivers of transmission |
| Figure 4(e) | [fig4_puuv.py](fig4_puuv.py) | Patch-specific environment-to-human transmission coefficients (PUUV example) |
| Figure 5 | [fig5_lyme_acquisition_component.py](fig5_lyme_acquisition_component.py) | Community-weighted acquisition component (Lyme disease example) |
| Figure 6 | [fig6_movement_overlap.py](fig6_movement_overlap.py) | Movement, spatial overlap, and temporal changes in transmission coefficients |

Panels 4(a)-(d) were drawn manually. The Figure 4 code generates panel (e) only.

## Run in Jupyter Notebook

1. Download the repository and open a Jupyter notebook in the repository folder.
2. Install NumPy, Matplotlib, and SciPy by running this notebook cell:

```python
%pip install -r requirements.txt
```

3. Open the code file for the required figure, copy its full contents into a notebook code cell, and run the cell. Use a fresh kernel for each figure.

Each file saves its figure and displays it using `plt.show()`.

## Output files

| Figure | Saved files | Save location |
| --- | --- | --- |
| Figure 2 | `fig2.png` | Desktop, if that folder exists; otherwise the current working directory |
| Figure 3 | `fig3.png` | Desktop, if that folder exists; otherwise the current working directory |
| Figure 4(e) | `Figure4_panel_e.png`, `.pdf`, `.tif`; `Figure4_coefficients.csv` | `Figure 4/` under the current working directory |
| Figure 5 | `fig5_lyme_acquisition_component.png`, `.tif`, `.pdf`, `.eps` | `outputs/figures/` under the current working directory |
| Figure 6 | `Figure6.png` | Desktop, if that folder exists; otherwise the current working directory |

The Desktop location is `Path.home() / "Desktop"`. The current working directory is the notebook kernel's working directory. Output folders are created automatically; rerunning a figure replaces files with the same names.

For Figure 5, use PNG, TIFF, or PDF to retain the intended appearance of transparent elements. EPS renders transparent elements as opaque.

## License

See [LICENSE](LICENSE).
