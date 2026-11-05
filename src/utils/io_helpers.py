
import csv
import json
from datetime import datetime
from typing import Dict, Tuple, Optional

import numpy as np
import torch


def load_entity2id(path: str) -> Dict[str, int]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_embeddings(path: str) -> torch.Tensor:
    return torch.tensor(np.load(path), dtype=torch.float)


def load_case_split(split_path: str) -> Tuple[set, set, set]:
    with open(split_path, encoding="utf-8") as f:
        d = json.load(f)
    return set(d["train"]), set(d["val"]), set(d.get("test", []))


def load_temporal_case_split_from_csv(csv_path: str, train_ratio: float = 0.8,
                                      val_ratio: float = 0.1):
    """Strict temporal case split with boundaries at case-start quantiles.

    A case is kept only if its whole span (first to last event) lies inside
    one window; cases crossing a boundary are dropped (no train/val/test
    overlap in time).
    """
    case_start: Dict[str, float] = {}
    case_end: Dict[str, float] = {}
    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = str(row["caseID_case_concept_name"]).strip()
            ts_str = str(row["event_timestamp_time_timestamp"]).strip()[:14]  # yyyymmddHHMMSS
            ts = datetime.strptime(ts_str, "%Y%m%d%H%M%S").timestamp()
            if cid not in case_start:
                case_start[cid] = ts
                case_end[cid] = ts
            else:
                case_start[cid] = min(case_start[cid], ts)
                case_end[cid] = max(case_end[cid], ts)

    ordered = sorted(case_start, key=lambda c: (case_start[c], c))
    n = len(ordered)
    t1 = case_start[ordered[int(n * train_ratio)]]                 # train/val boundary
    t2 = case_start[ordered[int(n * (train_ratio + val_ratio))]]   # val/test boundary

    train_cases, val_cases, test_cases = set(), set(), set()
    n_overlap = 0
    for c in ordered:
        s, e = case_start[c], case_end[c]
        if s < t1 and e < t1:
            train_cases.add(c)
        elif t1 <= s and e < t2:
            val_cases.add(c)
        elif t2 <= s:
            test_cases.add(c)
        else:
            n_overlap += 1  # spans a boundary

    print(f"Temporal case split: {len(train_cases)} train / "
          f"{len(val_cases)} val / {len(test_cases)} test  "
          f"(dropped {n_overlap} boundary-overlapping; total {n})")
    return train_cases, val_cases, test_cases


def load_pt(path: str) -> dict:
    return torch.load(path, map_location="cpu", weights_only=False)


def load_vocabs(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_id2ent(path: str) -> Optional[Dict[int, str]]:
    with open(path, encoding="utf-8") as f:
        ent2id = json.load(f)
    return {i: uri for uri, i in ent2id.items()}
