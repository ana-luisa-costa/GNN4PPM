## KG Construction with YARRRML

This folder contains the YARRRML mappings used to build RDF graphs for each dataset.

### Folder Layout

- `BPIC12A/db_mapping_BPIC12_Application.yarrrml`
- `BPIC12W/db_mapping_BPIC12_Work.yarrrml`
- `BPIC12WC/db_mapping_BPIC12_WC.yarrrml`
- `BPIC13O/db_mapping_BPIC13_OpenProblems.yarrrml`
- `BPIC20P/db_mapping_BPIC20_Prepaid.yarrrml`
- `BPIC20R/db_mapping_BPIC20_Request.yarrrml`

## Prerequisites

- PostgreSQL (local or remote)
- Java 11+ (for RMLMapper)
- Node.js + npm (for YARRRML parser)

Install the YARRRML parser globally:

```bash
npm install -g @rmlio/yarrrml-parser
```

Download RMLMapper jar (example):

```bash
curl -L -o rmlmapper.jar https://github.com/RMLio/rmlmapper-java/releases/latest/download/rmlmapper.jar
```

## End-to-End Workflow

1. Load your dataset CSV into PostgreSQL.
2. Run the YARRRML parser to generate an RML mapping (`.rml.ttl`).
3. Run RMLMapper on that RML file to generate RDF (`.ttl`).

---

## 1) Load CSV into PostgreSQL

Create a database (example for BPIC12):

```sql
CREATE DATABASE bpic12;
```

Create a table that matches your CSV header. Example table name used in mappings:

```sql
CREATE TABLE public.bpic12_subprocess_application_stage (
    caseid_case_concept_name text,
    case_othern_case_reg_date text,
    case_othern_case_amount_req text,
    eventid text,
    event_othern_org_resource text,
    event_otherc_lifecycle_transition text,
    event_activity_concept_name text,
    event_timestamp_time_timestamp text
);
```

Import CSV (run in `psql`):

```sql
\copy public.bpic12_subprocess_application_stage
FROM 'C:/path/to/BPIC12_A.csv'
WITH (FORMAT csv, HEADER true);
```

If your mapping uses row order (for directly-follows edges), ensure `csv_pos` exists:

```sql
ALTER TABLE public.bpic12_subprocess_application_stage
ADD COLUMN IF NOT EXISTS csv_pos bigint;

WITH ranked AS (
    SELECT ctid, row_number() OVER () AS rn
    FROM public.bpic12_subprocess_application_stage
)
UPDATE public.bpic12_subprocess_application_stage t
SET csv_pos = r.rn
FROM ranked r
WHERE t.ctid = r.ctid;
```

## 2) Parse YARRRML into RML

Example for BPIC12A:

```bash
yarrrml-parser -i BPIC12A/db_mapping_BPIC12_Application.yarrrml -o BPIC12A/mapping.rml.ttl
```

## 3) Execute RMLMapper to Generate RDF

```bash
java -jar rmlmapper.jar \
  -m BPIC12A/mapping.rml.ttl \
  -o BPIC12A/BPIC12_A.ttl \
  -s turtle
```

Move or copy the output TTL to your project data path, for example:

- `data/raw/BPIC12_A/BPIC12_A.ttl`

## Notes

- The current mappings use JDBC sources like:
  - `jdbc:postgresql://localhost:5432/<db>?user=<user>&password=<password>`
- Update database name, user, password, and table name according to your local setup.

## Run with Dataset Scripts

Each dataset folder includes two helper scripts named after the dataset:

- `run_mapping_BPIC12A.sh` / `run_mapping_BPIC12A.bat` (BPIC12A folder)
- `run_mapping_BPIC12W.sh` / `run_mapping_BPIC12W.bat` (BPIC12W folder)
- `run_mapping_BPIC12WC.sh` / `run_mapping_BPIC12WC.bat` (BPIC12WC folder)
- `run_mapping_BPIC13O.sh` / `run_mapping_BPIC13O.bat` (BPIC13O folder)
- `run_mapping_BPIC20P.sh` / `run_mapping_BPIC20P.bat` (BPIC20P folder)
- `run_mapping_BPIC20R.sh` / `run_mapping_BPIC20R.bat` (BPIC20R folder)

These scripts run both steps automatically:

1. Parse local `.yarrrml` to `mapping.rml.ttl`.
2. Run RMLMapper to produce the dataset `.ttl` file.

Both scripts accept an optional first argument for the RMLMapper jar path.
If omitted, they default to `kg-construction/rmlmapper.jar`.

Examples:

```bash
# from BPIC12A folder
bash run_mapping_BPIC12A.sh

# custom jar path
bash run_mapping_BPIC12A.sh /absolute/path/to/rmlmapper.jar
```

```bat
REM from BPIC12A folder
run_mapping_BPIC12A.bat

REM custom jar path
run_mapping_BPIC12A.bat C:\path\to\rmlmapper.jar
```

