
## Overview

GNN4PPM is a pipeline that combines RDF graph embeddings with relational graph neural networks to predict process attributes and supports the publication "GNN4PPM: Multi-Target Predictive Process Monitoring with Relational Graph Convolutional Networks".

## Setup

### Prerequisites

- Python 3.9+
- Virtual environment
- Recommended Python version: 3.13.12

### Installation

1. Create and activate the virtual environment:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Full Pipeline

Run `main.py` for a specified dataset, such as for BPIC13_O.

```bash
python main.py BPIC13_O
```

#### Available Datasets

- BPIC12_A
- BPIC12_W
- BPIC12_WC
- BPIC13_O
- BPIC17_O
- BPIC20_P
- BPIC20_R

### KG Construction (YARRRML -> RML -> RDF)

RDF graphs can be generated from the dataset-specific YARRRML mappings in `kg-construction/`.

- Full instructions: `kg-construction/README.md`
- Includes workflow for:
    - loading CSV files into PostgreSQL,
    - parsing YARRRML into RML,
    - executing RMLMapper to generate `.ttl` RDF files.
- Dataset folders also include named helper scripts (`.sh` and `.bat`) to run parsing and mapping in one step.


## Data Structure

The pipeline expects datasets to be organized as:

```
data/raw/{DATASET}/
├── {DATASET}.ttl          # RDF graph in Turtle format
├── {DATASET}.csv          # Preprocessed event log
└── (generated files after build)
    ├── case_split.json
    ├── entity2id.json
    └── entity_embeddings.npy

data/processed/{DATASET}/
└── (generated files after pipeline)
    ├── best_val.pt
    ├── best_val_vocabs.json
    └── evaluation.txt
```
