Repository: UFMG-obesidade_infantil — quick orientation for AI coding agents

Keep this short and actionable. Use these notes when making edits, adding pages, or changing data pipelines.

- Big picture
  - This is a Streamlit dashboard (plotly + pandas) for anthropometric indicators (0–9 years).
  - Root UI entry is `Menu.py` (sets page config and welcome text). The repo also uses `pages/` to provide Streamlit multipage screens (e.g., `pages/A)_Dados__gerais.py`).
  - Data is loaded eagerly at import time by `dataset.py` from `dados/originais/*.csv`. Edits to data-loading should preserve the module-level variables: e.g. `df_categ_geral`, `df_geral_cadunico`, `df_categ_regiao`, and their `_prev` counterparts.

- Run / dev workflow (what actually works)
  - Install dependencies: pip install -r requirements.txt
  - Run the app from the repository root so relative paths work. The README mentions `main.py`, but the actual entry is `Menu.py` in the project root. Use:
    - streamlit run Menu.py
  - Important: run commands from repo root (the code uses Path("dados") relative paths).

- Data & I/O conventions (critical)
  - CSVs live in `dados/originais/` and are read with pandas using sep=',' and decimal='.'. Missing or moved files will cause import-time errors because `dataset.py` executes reads during import.
  - Common column names to expect across CSVs: `tabela`, `categoria`, `sexo`, `region_cadunico`, `idade_cat`, `med_altura`, `med_peso`, `med_imc`, `prev_obesidade`, `prev_excesso`.
  - Many plotting helpers convert comma decimals to dots before numeric conversions (e.g., `str.replace(',', '.')`). Keep that when transforming prevalence columns.

- Patterns & gotchas for contributors / agents
  - dataset.py has side effects: importing it runs file I/O and defines DataFrame globals. When refactoring, preserve the module-level names or update all pages that `from dataset import ...`.
  - Plotting functions are inconsistent: some return a Plotly `fig` (e.g., `plot_zscore_brasil`), others call `st.plotly_chart` directly (e.g., `plot_zscore_por_regiao`). If you refactor or reuse a helper, normalize behavior or document the expected usage.
  - UI localization: code, comments, and strings are in Portuguese. Keep labels and variable names consistent with existing Portuguese names to avoid confusion.

- Where to look for examples
  - `pages/A)_Dados__gerais.py` — simple page showing how filters and two-column layout are implemented and how plotting helpers are used.
  - `dataset.py` — canonical data-loading and DataFrame names used across the app.
  - `graficos.py` — canonical plotting helpers (plotly + streamlit). Use as source of color palettes, age-ordering and column conventions.

- If you change data paths or file names
  - Update `dataset.py` and all `from dataset import ...` usages. Run the app from repo root to validate.

- Tests / lint / build
  - No test suite is present. Focus on small manual validations:
    - Run `python -c "import dataset; print(dataset.df_categ_geral.shape)"` from repo root to confirm data loads.
    - Start Streamlit and manually click through pages.

- When to ask the maintainer
  - If you need to change column names in CSVs, ask before renaming — many pages and plotting helpers rely on exact column names.

If anything in here is unclear or you want me to expand a section (examples of common edits, tests, or a normalization of plotting helpers), tell me which section to refine.
