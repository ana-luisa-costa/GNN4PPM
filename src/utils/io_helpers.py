
import csv
import json
from typing import Dict, Tuple, Optional

import numpy as np
import torch

from src.utils.uri_helpers import parse_ts


def load_entity2id(path: str) -> Dict[str, int]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_embeddings(path: str) -> torch.Tensor:
    return torch.tensor(np.load(path), dtype=torch.float)


def load_case_split(split_path: str) -> Tuple[set, set, set]:
    with open(split_path, encoding="utf-8") as f:
        d = json.load(f)
    return set(d["train"]), set(d["val"]), set(d.get("test", []))


def load_case_window_end(split_path: str) -> Dict[str, float]:
    """Case id → time from which its events must not be used (inf for test)."""
    with open(split_path, encoding="utf-8") as f:
        d = json.load(f)
    return {cid: d["window_end"][split] if d["window_end"][split] is not None else float("inf")
            for split in ("train", "val", "test") for cid in d[split]}


def load_temporal_case_split_from_csv(csv_path: str, train_ratio: float = 0.8,
                                      val_ratio: float = 0.1):
    """Temporal case split with boundaries at case-start quantiles.

    A case belongs to the window of its first event. A train or val case that
    is still running when the test window starts is dropped, so no case shares
    time with test. A train case running into the val window is kept, but its
    events from the end of the train window on are dropped later (see
    usable_event_uris), so no train and val events overlap in time.

    Returns (train_cases, val_cases, test_cases, window_end), where window_end
    maps each split to the time its events must stay before (None = no end).
    """
    case_start: Dict[str, float] = {}
    case_end: Dict[str, float] = {}
    with open(csv_path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            cid = str(row["caseID_case_concept_name"]).strip()
            ts = parse_ts(row["event_timestamp_time_timestamp"])
            case_start[cid] = min(ts, case_start.get(cid, ts))
            case_end[cid] = max(ts, case_end.get(cid, ts))

    ordered = sorted(case_start, key=lambda c: (case_start[c], c))
    n = len(ordered)
    t1 = case_start[ordered[int(n * train_ratio)]]                 # train/val boundary
    t2 = case_start[ordered[int(n * (train_ratio + val_ratio))]]   # val/test boundary

    before_test = {c for c in ordered if case_end[c] < t2}
    train_cases = {c for c in before_test if case_start[c] < t1}
    val_cases = {c for c in before_test if t1 <= case_start[c]}
    test_cases = {c for c in ordered if t2 <= case_start[c]}
    n_dropped = n - len(train_cases) - len(val_cases) - len(test_cases)

    print(f"Temporal case split: {len(train_cases)} train / "
          f"{len(val_cases)} val / {len(test_cases)} test  "
          f"(dropped {n_dropped} reaching the test window; total {n})")
    return train_cases, val_cases, test_cases, {"train": t1, "val": t2, "test": None}


def load_pt(path: str) -> dict:
    return torch.load(path, map_location="cpu", weights_only=False)


def load_vocabs(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_id2ent(path: str) -> Optional[Dict[int, str]]:
    with open(path, encoding="utf-8") as f:
        ent2id = json.load(f)
    return {i: uri for uri, i in ent2id.items()}
