#!/usr/bin/env python3
"""Index local/GCS JSONLs and write hub/_trajs.json (compact step logs)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HUB = Path(__file__).resolve().parent
if str(HUB) not in sys.path:
    sys.path.insert(0, str(HUB))

from _build import TASKS  # noqa: E402
from _traj import FILE_RE, SEED5, TRAJS_JSON, canon_id, episode_from_task, extract_compact  # noqa: E402

TRAJ_ROOT = Path("/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories")

# Prefer these folders when several copies exist for the same episode.
PREFERRED = (
    "ui031_ui060_sol_seed0_gcp/trajs",
    "d460_d481_sol_seed0_gcp/trajs",
    "n440_n449_prompt_review_sol_seed0_gcp/trajs",
    "four_prompt_rerun_sol_seed0_gcp/trajs",
    "prompt_review_sol_seed0_gcp/trajs",
    "mp130_162_sol_seed0_gcp/trajs",
    "md002_proc_trap_sol_3seed_20260810",
    "m432_m444_feedback_sol_seed0_gcp/trajs",
    "confirmed_5seed_sol_gcp/trajs",
    "br201_220_fast_slice_a_sol_seed0_local",
    "br201_220_partial_sol_seed0_local",
)

# Cards whose why-text has no live hash (or a stale one). Latest hub episode only.
HUB_EPISODES = {
    "md_002": "314d3c64",
    "mp_161": "837f6cb3",
    "mp_131": "71ea6cb0",
    "mp_132": "e05be9f7",
    "mp_142": "11f32f4f",
    "mp_147": "e345be91",
    "n440": "25bfd1b5",
    "n441": "b433bdaf",
    "n442": "59c401f8",
    "n443": "9e22f698",
    "n444": "478f5acb",
    "n445": "fc386edd",
    "n448": "155270ee",
    "n449": "975c9a01",
    "fb2b": "0c4b89d8",
    "n446": "698f47d9",
    "n447": "aedcc099",
    # mp130–151: first successful Cloud Run seed0 (034938Z), unless a later cited rerun exists
    "mp_130": "b3eefe80",
    "mp_133": "8d2acf0d",
    "mp_134": "7f438f38",
    "mp_135": "ce148e8f",
    "mp_136": "3a991be2",
    "mp_137": "d32521d3",
    "mp_138": "89a2f590",
    "mp_139": "75a75d11",
    "mp_140": "8874e4c9",
    "mp_141": "ea866807",
    "mp_143": "8f1a5251",
    "mp_144": "15cf938c",
    "mp_145": "e1cdad31",
    "mp_146": "86267980",
    "mp_148": "4d6e349a",
    "mp_149": "ddcc6145",
    "mp_150": "f1d75f4f",
    "mp_151": "895c4821",
    "mp_156": "98c76628",
    # remainder seed0 (035638Z) — later pass for these ids
    "mp_152": "0703962e",
    "mp_153": "b5ca34d2",
    "mp_154": "da490d6d",
    "mp_155": "ecfd3889",
    "mp_157": "c8ab38ca",
    "mp_158": "9444aca6",
    "mp_159": "a861b64f",
    "mp_160": "c430fbd5",
    "mp_162": "11551ecf",
}

GCS_PREFIX = {
    "ui_": "gs://gemini-503300-filtration-runs/filtration/ui031_ui060_20260814/ui031-ui060-sol-seed0-20260814T184710Z/artifacts/",
    "d4": "gs://gemini-503300-filtration-runs/filtration/d460_d481_20260813/d460-d481-sol-seed0-20260813T235806Z/artifacts/",
}


def index_jsonls() -> tuple[dict[str, list[Path]], dict[str, list[Path]]]:
    by_ep: dict[str, list[Path]] = {}
    by_slug: dict[str, list[Path]] = {}
    for p in TRAJ_ROOT.rglob("*.jsonl"):
        m = FILE_RE.match(p.name)
        if not m:
            continue
        by_ep.setdefault(m.group("ep"), []).append(p)
        slug = m.group("slug")
        by_slug.setdefault(slug, []).append(p)
        # also index bare task prefix (ui_031_..., d460_...)
        head = slug.split("_", 2)
        if len(head) >= 2:
            by_slug.setdefault("_".join(head[:2]) if slug.startswith("ui_") else head[0], []).append(p)
    return by_ep, by_slug


def rank(path: Path) -> tuple[int, int]:
    rel = str(path.relative_to(TRAJ_ROOT)) if path.is_relative_to(TRAJ_ROOT) else str(path)
    for i, pref in enumerate(PREFERRED):
        if rel.startswith(pref):
            return (i, len(rel))
    return (len(PREFERRED) + 1, len(rel))


def pick(cands: list[Path]) -> Path:
    return sorted(cands, key=rank)[0]


def gcs_for(hid: str, path: Path) -> str:
    for prefix, bucket in GCS_PREFIX.items():
        if hid.startswith(prefix):
            return bucket + path.name
    return ""


def find_by_slug(by_slug: dict[str, list[Path]], slug: str, seed: int = 0) -> Path | None:
    cands = by_slug.get(slug) or []
    seeded = [p for p in cands if f"__{seed}__" in p.name]
    pool = seeded or cands
    return pick(pool) if pool else None


def main() -> None:
    by_ep, by_slug = index_jsonls()
    catalog: dict[str, dict] = {}
    missing: list[str] = []
    for task in TASKS:
        hid = canon_id(task["id"])
        ep = HUB_EPISODES.get(hid) or episode_from_task(task)
        # Confirmed hub cards: prefer the episode the card cites; m431 uses ff9024e6.
        if hid in SEED5 and SEED5[hid].get("hub_episode"):
            ep = SEED5[hid]["hub_episode"]
        path = None
        if ep and ep in by_ep:
            path = pick(by_ep[ep])
        if path is None:
            path = find_by_slug(by_slug, task["slug"])
        if path is None:
            path = find_by_slug(by_slug, hid)
        if path is None:
            missing.append(f"{hid} ep={ep or '?'} slug={task['slug']}")
            continue
        try:
            compact = extract_compact(path, gcs=gcs_for(hid, path))
        except Exception as exc:  # noqa: BLE001
            missing.append(f"{hid} extract-fail {path.name}: {exc}")
            continue
        compact["hub_id"] = hid
        catalog[hid] = compact
        print(f"ok {hid:12} {compact['episode']} {compact['steps_n']:3} {path.name}")

    TRAJS_JSON.write_text(json.dumps(catalog, ensure_ascii=False, indent=None), encoding="utf-8")
    print(f"\nwrote {TRAJS_JSON}  n={len(catalog)} missing={len(missing)}")
    for line in missing:
        print("MISSING", line)


if __name__ == "__main__":
    main()
