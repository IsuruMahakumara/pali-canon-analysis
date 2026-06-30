## Repository Structure & Notebook Conventions

This repository enforces strict structural hygiene to maintain modularity and prevent pipeline clutter as the algorithmic engine scales.

### 1. Naming Standard
* **Casing:** All filenames must use `snake_case` exclusively. No spaces, no hyphens.
* **Format:** `[Functional Prefix]_[Subject]_[Action].ipynb`

### 2. Standard Functional Prefixes

Every notebook must lead with one of these approved prefixes to group files by their layer in the engineering stack:

| Prefix | Domain Lifecycle Phase | Core Operational Focus |
| :--- | :--- | :--- |
| `etl_` | Extract, Transform, Load | BigQuery data ingestion, historical bootstrapping, delta accumulation. |
| `qa_`  | Quality Assurance & Validation | Schema integrity verification, outlier detection, data sanity parsing. |
| `eda_` | Exploratory Data Analysis | Data profiling, asset liquidity mapping, statistical distributions. |
| `feat_`| Feature Engineering | Alpha factor generation, moving averages, mathematical derivatives. |
| `sim_` | Simulation & Backtesting | Backtesting execution loops, signal performance verifications. |
| `exp_` | Experimentation & Scratchpad | Short-lived algorithmic prototypes and sandboxed code exploration. |

### 3. Unified Directory Layout

```text
├── config/                     # Global system configurations and schema definitions
│   └── bq_schemas.json         # Hard schemas for BigQuery tables
├── ingest/                        # Production codebase (C++ engine / Python core)
│   ├── bq_pipeline.py          # Stable, automated daily delta accumulator scripts
│   └── client.py               # Optimized BigQuery initialization clients
├── notebooks/                  # Interactive research and verification sandbox
│   ├── etl_01_cse_bootstrap.ipynb   # Step 1: Run once to set up tables and pre-2026 data
│   ├── etl_02_cse_accumulator.ipynb # Step 2: Daily automated execution loop code
│   ├── qa_01_schema_checks.ipynb    # Validates BigQuery structural integrity
│   ├── eda_01_cse_liquidity.ipynb   # Visualizes historical market profile dynamics
│   ├── feat_01_moving_averages.ipynb# Prototypes time-series signal generation
│   └── exp_01_stochastic_test.ipynb # Sandboxed testing for raw trading mechanics
└── tests/                      # Native unit testing suites

```

### 4. Core Development Rules

* **Deterministic Sequence:** Within any functional prefix domain, notebooks must follow a strict double-digit sequential ordering (`01`, `02`) to declare dependency and execution priority.
* **Single Responsibility Mandate:** A notebook must execute exactly one logical task. Never combine extraction pipelines (`etl_`) with algorithmic feature modeling (`feat_`) in the same file.
* **The Production Pivot:** Notebooks are strictly tools for research, bootstrapping, and visual debugging. Once a pipeline process or mathematical formula stabilizes, the logic must be extracted into a pure, unit-tested module within the `src/` directory.
* **Sandbox Separation:** Experimental scratchpads (`exp_`) are strictly prohibited on the `main` branch. Perform scratchpad work on short-lived feature branches and delete ephemeral files prior to opening a pull request.

```

