# SafeHer ML Python Environment

## Environment

- Python: 3.12.6
- Virtual environment: `ml-model/.venv`
- Dependency lock snapshot: `ml-model/requirements.txt` (all resolved packages pinned)
- Raw datasets were not read or changed during environment validation.
- The existing `jupyter` dependency was retained and JupyterLab was added for the requested notebook environment.

## Installed direct dependencies

| Package | Installed version |
| --- | ---: |
| pandas | 3.1.1 |
| numpy | 2.5.5 |
| matplotlib | 3.11.2 |
| seaborn | 0.13.2 |
| scikit-learn | 1.9.1 |
| jupyterlab | 4.6.6 |
| joblib | 1.6.0 |
| jupyter (retained existing dependency) | 1.1.1 |

The requirements file records the full resolved package snapshot from the virtual environment, not just these direct packages.

## Windows PowerShell

From the repository root:

```powershell
.\ml-model\.venv\Scripts\Activate.ps1
python --version
python -m pip install -r ml-model\requirements.txt
jupyter lab
```

If PowerShell blocks activation, do not change the machine's execution policy. Use the direct executable commands below.

## Windows Command Prompt

From the repository root:

```bat
ml-model\.venv\Scripts\activate.bat
python --version
python -m pip install -r ml-model\requirements.txt
jupyter lab
```

## Use without activation

From the repository root, invoke the environment explicitly:

```powershell
.\ml-model\.venv\Scripts\python.exe --version
.\ml-model\.venv\Scripts\python.exe -m pip install -r ml-model\requirements.txt
.\ml-model\.venv\Scripts\python.exe -m pip check
.\ml-model\.venv\Scripts\python.exe -m jupyterlab
```

On Windows Command Prompt, the equivalent executable path is `ml-model\.venv\Scripts\python.exe`.

## VS Code interpreter

1. Open the repository folder in VS Code.
2. Run **Python: Select Interpreter** from the Command Palette (`Ctrl+Shift+P`).
3. Select or enter `ml-model/.venv/Scripts/python.exe`.

## Recreate or verify dependencies

The environment was created with Python 3.12.6 and the installed packages were installed through the environment's Python/pip. The direct package install request was:

```powershell
.\ml-model\.venv\Scripts\python.exe -m pip install pandas numpy matplotlib seaborn scikit-learn jupyterlab joblib jupyter
```

For reproducibility, create `ml-model/.venv` using Python 3.12.6 and install the pinned snapshot:

```powershell
python -m venv ml-model\.venv
.\ml-model\.venv\Scripts\python.exe -m pip install -r ml-model\requirements.txt
```

Environment verification commands:

```powershell
.\ml-model\.venv\Scripts\python.exe -c "import pandas, numpy, matplotlib, seaborn, sklearn, joblib, jupyterlab; print('imports OK')"
.\ml-model\.venv\Scripts\python.exe -m jupyterlab --version
.\ml-model\.venv\Scripts\python.exe -m pip freeze
.\ml-model\.venv\Scripts\python.exe -m pip check
```

## Validation performed

- Python executable: Python 3.12.6; virtual-environment pip: 24.2.
- Imports of pandas, NumPy, Matplotlib, seaborn, scikit-learn, joblib, and JupyterLab: passed.
- JupyterLab CLI version check: passed, 4.6.6.
- Small in-memory pandas DataFrame creation: passed.
- NumPy array addition (`[1, 2] + 1`): passed, result `[2, 3]`.
- Matplotlib figure creation using the non-interactive Agg backend: passed.
- scikit-learn and joblib imports: passed.
- `pip check`: passed; no broken requirements found.
- No model was trained and no project dataset was used in these smoke checks.

Matplotlib printed a warning that it could not write its font cache under the current user's profile due to permission denial. Figure creation still succeeded. If this recurs on another machine, configure `MPLCONFIGDIR` to a user-writable cache location before importing Matplotlib.

## Known limitations and next-phase input

- Dependency versions are pinned to the versions resolved in this Windows environment. Reproduction on another operating system or Python patch version should be verified there.
- MongoDB Atlas is not configured or accessed as part of this setup.
- Dataset provenance, licensing, geographic definitions, and other Phase 2B findings remain unresolved and must be reviewed before preprocessing or EDA begins.
- This phase only prepares the environment. It does not preprocess data, perform EDA or feature engineering, train models, or add API integration.
