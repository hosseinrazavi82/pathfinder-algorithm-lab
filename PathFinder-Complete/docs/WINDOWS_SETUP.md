# Windows setup — step by step

## 1. Install Python and VS Code

Install a recent Python release (3.11 or newer) from https://www.python.org/downloads/windows/ and install VS Code from https://code.visualstudio.com/. In PowerShell or VS Code Terminal check:

```powershell
py --version
```

## 2. Open the correct folder

Unzip `PathFinder-Complete.zip` using **Extract All**. In VS Code choose **File → Open Folder** and select the inner `PathFinder-Complete` folder, where `app.py` and `requirements.txt` are visible.

## 3. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

If `py` is not recognized, use `python` instead. If pip is unavailable, run `py -m ensurepip --upgrade`, and retry.

## 4. Launch the browser interface

```powershell
py -m streamlit run app.py
```

Your terminal should show a `Local URL` such as `http://localhost:8501`. Open this address in the browser. To stop the server, return to the terminal and press **Ctrl+C**.

## 5. Run automated tests (optional but recommended)

```powershell
py -m pip install -r requirements-dev.txt
py -m pytest -q
```

## 6. Run the terminal version

```powershell
py main.py
```

## Common issues

- **`No module named streamlit`** — dependencies were not installed in the Python interpreter used to launch the app. Use the same `py` executable for both commands.
- **`can't open file 'app.py'`** — open the terminal in the project root, not a parent directory.
- **A port is already in use** — run `py -m streamlit run app.py --server.port 8502`.
- **The browser doesn't open automatically** — copy the URL printed in the terminal manually.
- **PowerShell activation errors** — a virtual environment is optional here; no activation is required.
