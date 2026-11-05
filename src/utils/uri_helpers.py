import re
from datetime import datetime, timezone
from typing import Dict, Hashable, List, Optional, Tuple

CASE_RE = re.compile(r"caseID\.org/(\d+)$")
EVENT_RE = re.compile(r"eventID\.org/(\d+)_(\d+)$")  # group1=event#, group2=caseID

P_TIME = "http://example.org/hasevent_timestamp_time_timestamp"


def get_case_of_entity(uri: str) -> Optional[str]:
    m = EVENT_RE.search(uri)
    if m:
        return m.group(2)  # Return caseID (group 2)
    m = CASE_RE.search(uri)
    if m:
        return m.group(1)
    return None


def parse_ts(ts: str) -> Optional[float]:
    ts = str(ts).strip()
    if len(ts) < 14 or not ts[:14].isdigit():
        return None
    try:
        dt = datetime.strptime(ts[:14], "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
        frac = ts[14:]
        frac_sec = (int(frac) / (10 ** len(frac))) if (frac and frac.isdigit()) else 0.0
        return dt.timestamp() + frac_sec
    except Exception:
        return None


def order_case_events(events: Dict[int, Tuple[Hashable, Optional[float]]]) -> List[Hashable]:
    """Order one case's events by timestamp, falling back to event# for ties.

    `events` maps event# → (item, timestamp). The event# follows CSV row order,
    which is not always temporal, so it only breaks ties. Events without a
    timestamp go last.
    """
    def key(num):
        ts = events[num][1]
        return (ts is None, ts if ts is not None else 0.0, num)
    return [events[num][0] for num in sorted(events, key=key)]
