# Code for the spillover framework manuscript

This repository contains Python code for the illustrative figures in the spillover framework manuscript.

Figure 2   Illustrative seasonality in relative exposure opportunity |
Figure 3  Synthetic illustration of spatial drivers of transmission |
Figure 4(e)   Patch-specific environment-to-human transmission coefficients (PUUV example) |
Figure 5   Community-weighted acquisition component (Lyme disease example) |
Figure 6 Movement, spatial overlap, and temporal changes in transmission coefficients |

1. Download this repository and open a Jupyter notebook in the repository folder.
2. Install the dependencies in a notebook cell:

```python
%pip install -r requirements.txt
```

3. Copy the code for the required figure into a notebook code cell and run it. Use a fresh kernel for each figure.


Output filenames and save locations are specified in each figure's code.

The Figure 4(e) code displays the plot using `plt.show()` and saves PNG, PDF, TIFF, and CSV files in a `Figure 4` folder under the notebook's current working directory.


See [LICENSE](LICENSE).
