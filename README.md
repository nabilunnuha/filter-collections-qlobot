# Filter-Collections

## Overview
To convert collections from pdc bot to qlobot csv or filter collections csv from qlobot.

## Requirements
- [pymongo](https://pypi.org/project/pymongo/)==4.2.0
- [pandas](https://pypi.org/project/pandas/)
- [pyarrow](https://pypi.org/project/pyarrow/)
- [tqdm](https://pypi.org/project/tqdm/)
- [colorama](https://pypi.org/project/colorama/)

## How to Run

1. **Activate Virtual Environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

2. **Install Required Modules:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the filter collections csv:**
    ```bash
    python filter_from_collection.py
    ```
    
3. **Run the convert pdc collections to qlobot csv:**
    ```bash
    python filter_from_pdc.py
    ```

## Package Information

- **Author:** [Nabilunnuha](https://github.com/nabilunnuha)

## Notes
- Ensure that you have Python installed on your system before running the commands.
- The virtual environment is recommended for managing dependencies and preventing conflicts with other projects.
