#!/usr/bin/env python3
"""Encode Sol agent + oracle-film screenshots into dossier-qa galleries.

Thumbs ~560 JPEG q88 4:4:4; lightbox ~1280 JPEG q92 4:4:4.
Writes galleries.json consumed by _build.py.
"""
from __future__ import annotations

import json
import re
import shutil
import tarfile
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent
RAW = OUT / "_raw"
ASSETS = OUT / "assets"
TRAJ_ROOT = Path("/Users/maroonferrari/Deccan/browser-gym-seed-to-cua-gym/trajectories")

THUMB_W = 560
THUMB_Q = 88
FULL_MAX_W = 1280
FULL_Q = 92

# Latest episodes for the live dossier-qa pages.
TASKS = {
    "m431": {
        "episode": "ff9024e6",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/m431_ambiguous_aster_lamp_return__0__ff9024e6.jsonl",
        "tar": RAW / "sol_screens/prompt_review/m431_ambiguous_aster_lamp_return__0__ff9024e6_screens.tar.gz",
    },
    "fb2b": {
        "episode": "0c4b89d8",
        "traj": TRAJ_ROOT / "m432_m444_feedback_sol_seed0_gcp/trajs/fb2b_nadia_birthday_list__0__0c4b89d8.jsonl",
        "tar": RAW / "sol_screens/m432_m444/fb2b_nadia_birthday_list__0__0c4b89d8_screens.tar.gz",
    },
    "n446": {
        "episode": "2f4f2cd2",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/n446_redirect_shipped_throw_missing_cushion__0__2f4f2cd2.jsonl",
        "tar": RAW / "sol_screens/prompt_review/n446_redirect_shipped_throw_missing_cushion__0__2f4f2cd2_screens.tar.gz",
    },
    "n447": {
        "episode": "aedcc099",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/n447_expense_claim_failed_cancel__0__aedcc099.jsonl",
        "tar": RAW / "sol_screens/prompt_review/n447_expense_claim_failed_cancel__0__aedcc099_screens.tar.gz",
    },
    "n448": {
        "episode": "e1703a80",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/n448_allergy_safe_friday_lunch_nine__0__e1703a80.jsonl",
        "tar": RAW / "sol_screens/prompt_review/n448_allergy_safe_friday_lunch_nine__0__e1703a80_screens.tar.gz",
    },
    "n449": {
        "episode": "975c9a01",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/n449_graduation_gifts_prior_spend__0__975c9a01.jsonl",
        "tar": RAW / "sol_screens/prompt_review/n449_graduation_gifts_prior_spend__0__975c9a01_screens.tar.gz",
    },
    "fb4": {
        "episode": "42c725e5",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/fb4_home_office_claim_omit_cancelled_chair__0__42c725e5.jsonl",
        "tar": RAW / "sol_screens/prompt_review/fb4_home_office_claim_omit_cancelled_chair__0__42c725e5_screens.tar.gz",
    },
    "m444": {
        "episode": "bb3869ea",
        "traj": TRAJ_ROOT / "m432_m444_feedback_sol_seed0_gcp/trajs/m444_larkfield_studio15_90w_adapter__0__bb3869ea.jsonl",
        "tar": RAW / "sol_screens/m432_m444/m444_larkfield_studio15_90w_adapter__0__bb3869ea_screens.tar.gz",
    },
    "fb5": {
        "episode": "3b2a3431",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/fb5_jason_desk_kit_samantha_cap__0__3b2a3431.jsonl",
        "tar": RAW / "sol_screens/prompt_review/fb5_jason_desk_kit_samantha_cap__0__3b2a3431_screens.tar.gz",
    },
    "n445": {
        "episode": "802ded05",
        "traj": TRAJ_ROOT / "prompt_review_sol_seed0_gcp/trajs/n445_ravi_desk_kit_under_95__0__802ded05.jsonl",
        "tar": RAW / "sol_screens/prompt_review/n445_ravi_desk_kit_under_95__0__802ded05_screens.tar.gz",
    },
}


def ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_thumb(im: Image.Image, dest: Path) -> None:
    ensure_dir(dest.parent)
    rgb = im.convert("RGB")
    w, h = rgb.size
    if w > THUMB_W:
        nh = max(1, int(h * (THUMB_W / w)))
        rgb = rgb.resize((THUMB_W, nh), Image.Resampling.LANCZOS)
    rgb.save(dest, "JPEG", quality=THUMB_Q, optimize=True, subsampling=0)


def save_full(im: Image.Image, dest: Path) -> None:
    ensure_dir(dest.parent)
    rgb = im.convert("RGB")
    w, h = rgb.size
    if w > FULL_MAX_W:
        nh = max(1, int(h * (FULL_MAX_W / w)))
        rgb = rgb.resize((FULL_MAX_W, nh), Image.Resampling.LANCZOS)
    rgb.save(dest, "JPEG", quality=FULL_Q, optimize=True, subsampling=0)


def process_one(src: Path, thumb: Path, full: Path) -> None:
    with Image.open(src) as im:
        save_thumb(im, thumb)
        save_full(im, full)


def format_action(step: dict) -> str:
    kind = step.get("action_kind") or step.get("action") or ""
    args = step.get("action_args") or {}
    if isinstance(args, str):
        return f"{kind}: {args}".strip(": ")
    name = args.get("name") or args.get("text") or args.get("value") or args.get("url")
    role = args.get("role")
    parts = [str(kind)] if kind else []
    if role:
        parts.append(str(role))
    if name:
        nm = " ".join(str(name).split())
        if len(nm) > 120:
            nm = nm[:117] + "…"
        parts.append(nm)
    elif args:
        compact = {k: args[k] for k in list(args)[:4] if k not in ("coord",)}
        parts.append(json.dumps(compact, ensure_ascii=False)[:140])
    return " · ".join(parts) if parts else ""


def infer_app(step: dict) -> str:
    tab = str(step.get("active_tab") or "").lower()
    url = str(step.get("url_after") or "").lower()
    blob = f"{tab} {url}"
    if any(x in blob for x in ("gmail", "mail", "#/inbox", "#/sent", "#/compose", "shopmail")):
        return "mail"
    if "calendar" in blob:
        return "calendar"
    if any(x in blob for x in ("ebay", "valuemart", "market")):
        return "market"
    if any(x in blob for x in ("uber", "eats", "food", "gymeats")):
        return "food"
    return "shop"


def step_reasoning(st: dict) -> str:
    reasoning = (st.get("reasoning") or "").strip()
    raw = (st.get("raw_model_output") or "").strip()
    if reasoning:
        return reasoning
    for line in raw.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line[:400]
    return ""


def extract_tar(tar_path: Path, dest: Path) -> Path | None:
    if dest.exists():
        shutil.rmtree(dest)
    ensure_dir(dest)
    if not tar_path.is_file():
        print(f"MISSING tar {tar_path}")
        return None
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(dest)
    cands = list(dest.rglob("step_000.png"))
    if not cands:
        pngs = sorted(dest.rglob("*.png"))
        print(f"WARN no step_000 in {tar_path.name} pngs={len(pngs)}")
        return dest if pngs else None
    return cands[0].parent


def collect_pngs(src_dir: Path) -> list[tuple[int, Path]]:
    steps: list[tuple[int, Path]] = []
    for p in src_dir.rglob("*.png"):
        m = re.match(r"step_(\d+)\.png$", p.name)
        if m:
            steps.append((int(m.group(1)), p))
    steps.sort()
    return steps


def encode_kind(src_dir: Path, dest_dir: Path) -> list[str]:
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    thumbs = ensure_dir(dest_dir / "thumbs")
    full = ensure_dir(dest_dir / "full")
    names = []
    for i, p in collect_pngs(src_dir):
        tname = f"step_{i:03d}.jpg"
        process_one(p, thumbs / tname, full / tname)
        names.append(tname)
    return names


def agent_frames(key: str, spec: dict, png_dir: Path | None) -> dict:
    traj = json.loads(spec["traj"].read_text()) if spec["traj"].is_file() else {}
    steps = traj.get("steps") or []
    ann = {int(st.get("step_idx", i)): st for i, st in enumerate(steps)}
    dest = ASSETS / key / "agent"
    names = encode_kind(png_dir, dest) if png_dir else []
    frames = []
    n = max(len(names), max(ann) + 1 if ann else 0)
    for i in range(n):
        tname = f"step_{i:03d}.jpg"
        st = ann.get(i) or {}
        why = step_reasoning(st)
        act = format_action(st)
        has = (dest / "thumbs" / tname).is_file()
        frames.append(
            {
                "step": i,
                "app": infer_app(st),
                "what": act or f"step {i}",
                "why": why or "no reasoning recorded",
                "act": act,
                "thumb": f"assets/{key}/agent/thumbs/{tname}" if has else "",
                "full": f"assets/{key}/agent/full/{tname}" if has else "",
            }
        )
    with_r = sum(1 for f in frames if f["why"] and f["why"] != "no reasoning recorded")
    with_s = sum(1 for f in frames if f["thumb"])
    return {
        "episode": spec["episode"],
        "frames": frames,
        "n": len(frames),
        "with_reasoning": with_r,
        "with_screenshot": with_s,
        "source": str(spec["traj"]),
    }


def oracle_frames(key: str) -> dict:
    raw = RAW / "oracle_ui" / key
    meta_path = raw / "steps.json"
    if not meta_path.is_file():
        return {"available": False, "frames": [], "n": 0, "note": "no oracle film"}
    meta = json.loads(meta_path.read_text())
    dest = ASSETS / key / "oracle"
    encode_kind(raw, dest)
    frames = []
    for st in meta.get("steps") or []:
        i = int(st.get("step", len(frames)))
        tname = f"step_{i:03d}.jpg"
        has = (dest / "thumbs" / tname).is_file()
        frames.append(
            {
                "step": i,
                "app": st.get("app") or "shop",
                "what": (st.get("action") or "").replace("navigate · ", "").replace("oracle-gold · ", ""),
                "why": st.get("reasoning") or "",
                "act": st.get("action") or "",
                "thumb": f"assets/{key}/oracle/thumbs/{tname}" if has else "",
                "full": f"assets/{key}/oracle/full/{tname}" if has else "",
            }
        )
    return {
        "available": True,
        "kind": meta.get("kind"),
        "note": meta.get("note"),
        "score": meta.get("score"),
        "success": meta.get("success"),
        "frames": frames,
        "n": len(frames),
        "with_screenshot": sum(1 for f in frames if f["thumb"]),
    }


def main() -> None:
    galleries = {
        "quality": {
            "thumb_w": THUMB_W,
            "thumb_jpeg_q": THUMB_Q,
            "full_max_w": FULL_MAX_W,
            "full_jpeg_q": FULL_Q,
            "subsampling": "4:4:4",
        },
        "tasks": {},
    }
    for key, spec in TASKS.items():
        print(f"== {key} ==")
        extracted = RAW / "sol_extracted" / key
        png_dir = extract_tar(spec["tar"], extracted)
        agent = agent_frames(key, spec, png_dir)
        oracle = oracle_frames(key)
        galleries["tasks"][key] = {"agent": agent, "oracle": oracle}
        print(
            f"  agent {agent['with_screenshot']}/{agent['n']} shots "
            f"reason {agent['with_reasoning']}/{agent['n']}  "
            f"oracle {oracle.get('with_screenshot', 0)}/{oracle.get('n', 0)} "
            f"gold={oracle.get('success')}"
        )
    (OUT / "galleries.json").write_text(json.dumps(galleries, indent=2) + "\n")
    print("wrote galleries.json")


if __name__ == "__main__":
    main()
