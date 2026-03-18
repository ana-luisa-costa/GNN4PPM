
import csv
import json
import random
from typing import Dict, Tuple, Optional

import numpy as np
import torch


def load_entity2id(path: str) -> Dict[str, int]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_embeddings(path: str) -> torch.Tensor:
    return torch.tensor(np.load(path), dtype=torch.float)


def load_case_split(split_path: str) -> Tuple[set, set]:
    with open(split_path, encoding="utf-8") as f:
        d = json.load(f)
    return set(d["train"]), set(d["val"])


def load_case_split_from_csv(csv_path: str, train_ratio: float = 0.8, seed: int = 42):
    cases = set()
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.add(str(row["caseID_case_concept_name"]).strip())

    unique_cases = sorted(cases)
    rng = random.Random(seed)
    rng.shuffle(unique_cases)

    n = len(unique_cases)
    split = int(n * train_ratio)
    train_cases = set(unique_cases[:split])
    val_cases = set(unique_cases[split:])
    print(f"Case split: {len(train_cases)} train / {len(val_cases)} val  (total {n})")
    return train_cases, val_cases, unique_cases


def load_pt(path: str) -> dict:
    return torch.load(path, map_location="cpu", weights_only=False)


def load_vocabs(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_id2ent(path: str) -> Optional[Dict[int, str]]:
    with open(path, encoding="utf-8") as f:
        ent2id = json.load(f)
    return {i: uri for uri, i in ent2id.items()}
