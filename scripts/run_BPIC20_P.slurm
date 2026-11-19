#!/bin/bash
#SBATCH --job-name=BPIC20_P_pipeline
#SBATCH --partition=compute
#SBATCH --gres=gpu:nvidia:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail

cd ~/GNN4PPM
source myenv/bin/activate
export PYTHONPATH="$PWD:${PYTHONPATH:-}"

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK

RAW=data/raw/BPIC20_P
PROC=data/processed/BPIC20_P
NAME=BPIC20_P
mkdir -p "$PROC"

echo "HOST: $(hostname)"
echo "START: $(date)"

echo "=== [1/3] RDF2Vec ==="
python3 -u src/build_rdf2vec.py \
  --ttl $RAW/$NAME.ttl \
  --csv $RAW/$NAME.csv \
  --out $RAW

echo "=== [2/3] Train ==="
python3 -u src/train.py \
  --ttl $RAW/$NAME.ttl \
  --emb $RAW/entity_embeddings.npy \
  --entity2id $RAW/entity2id.json \
  --temporal_split $RAW/temporal_split.json \
  --save_best_val $PROC/best_val.pt

echo "=== [3/3] Evaluate ==="
python3 -u src/evaluate.py \
  --best $PROC/best_val.pt \
  --output $PROC/evaluation.txt \
  --vocabs $PROC/best_val_vocabs.json \
  --entity2id $RAW/entity2id.json \
  --show_examples 5

echo "END: $(date)"
