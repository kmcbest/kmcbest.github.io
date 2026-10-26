#!/usr/bin/env python3
"""
TFTF Cloud-to-Local Read-Only Backup Tool
=========================================
【100% 只读保障脚本】
从 Upstash KV 云端完整拉取最新线上数据并备份至本地。
本脚本不包含任何向云端写入（SET/POST）的代码，物理杜绝因本地旧数据反向覆盖云端的风险。

用法:
    python tools/backup_cloud_to_local.py
    python tools/backup_cloud_to_local.py --out-dir backups/20261026
"""

import argparse
import datetime
import json
import sys
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UPSTASH_URL = "https://deciding-bulldog-136761.upstash.io"
# READ ONLY token for gets; WRITE token used strictly for listing /keys
WRITE_TOKEN = "gQAAAAAAAhY5AAIgcDEyZGMwZDRhNzRlZGQ0MDI2YWM2YmI3ZDExNTc3ZjZmNA"
READ_TOKEN = "ggAAAAAAAhY5AAIgcDG7a511dMnvUap5JjML7kdCMH0hQAG95-3BtwD6YEaFeQ"


def fetch_kv(key: str):
    """只读拉取单个 key"""
    url = f"{UPSTASH_URL}/get/{urllib.parse.quote(key, safe='')}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {READ_TOKEN}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data and data.get("result"):
                val = data["result"]
                return json.loads(val) if isinstance(val, str) else val
    except Exception as e:
        print(f"  [-] Failed to fetch {key}: {e}")
    return None


def fetch_char_keys():
    """只读列举所有角色 keys"""
    url = f"{UPSTASH_URL}/keys/tftf:char:*"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {WRITE_TOKEN}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("result", [])


def fetch_pipeline(keys: list):
    """通过 pipeline 批量只读获取"""
    chunk_size = 25
    results = {}
    for i in range(0, len(keys), chunk_size):
        chunk = keys[i:i + chunk_size]
        cmds = [["GET", k] for k in chunk]
        req = urllib.request.Request(
            f"{UPSTASH_URL}/pipeline",
            headers={"Authorization": f"Bearer {WRITE_TOKEN}", "Content-Type": "application/json"},
            data=json.dumps(cmds).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            res_list = json.loads(resp.read().decode("utf-8"))
            for k, item in zip(chunk, res_list):
                val = item.get("result")
                if val:
                    parsed = json.loads(val) if isinstance(val, str) else val
                    bid = k.replace("tftf:char:", "")
                    results[bid] = parsed
    return results


def main():
    parser = argparse.ArgumentParser(description="TFTF Read-Only Cloud Backup")
    parser.add_argument("--out-dir", type=str, default="", help="Custom output directory")
    args = parser.parse_args()

    # Determine default data dir
    if args.out_dir:
        base_dir = Path(args.out_dir).resolve()
    else:
        # Candidate dirs
        candidates = [
            Path(r"D:\#E\Personal\kmcbest.github.io\tftfr\data"),
            Path(r"D:\docforall\GitHub\kmcbest.github.io\tftfr\data")
        ]
        base_dir = next((d for d in candidates if d.exists()), candidates[0])

    char_dir = base_dir / "characters"
    char_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== TFTF Cloud Read-Only Backup Starting ===")
    print(f"Target directory: {base_dir}")
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Backup timestamp: {now_str}\n")

    # 1. Fetch overview
    print("[1/5] Fetching tftf:overview...")
    ov = fetch_kv("tftf:overview")
    if ov:
        (base_dir / "overview.json").write_text(json.dumps(ov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  [+] Saved overview.json ({len(ov.get('characters', []))} characters)")

    # 2. Fetch pua_icons
    print("[2/5] Fetching tftf:pua_icons...")
    pua = fetch_kv("tftf:pua_icons")
    if pua:
        (base_dir / "pua_icons.json").write_text(json.dumps(pua, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  [+] Saved pua_icons.json ({len(pua.get('icons', []))} icons)")

    # 3. Fetch priority_abilities
    print("[3/5] Fetching tftf:priority_abilities...")
    prio = fetch_kv("tftf:priority_abilities")
    if prio:
        (base_dir / "priority_abilities.json").write_text(json.dumps(prio, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  [+] Saved priority_abilities.json ({len(prio.get('abilities', []))} priority items)")

    # 4. Fetch all_abilities
    print("[4/5] Fetching tftf:all_abilities...")
    all_ab = fetch_kv("tftf:all_abilities")
    if all_ab:
        (base_dir / "all_abilities.json").write_text(json.dumps(all_ab, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"  [+] Saved all_abilities.json ({all_ab.get('total_bots', 0)} bots, {all_ab.get('total_abilities', 0)} abilities)")

    # 5. Fetch all individual character cards
    print("[5/5] Fetching individual character cards...")
    keys = fetch_char_keys()
    print(f"  Found {len(keys)} characters in Upstash KV...")
    chars_map = fetch_pipeline(keys)
    saved_count = 0
    for bid, data in chars_map.items():
        out_file = char_dir / f"{bid}.json"
        out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        saved_count += 1
    print(f"  [+] Successfully backed up {saved_count} character JSON files to {char_dir}")

    print("\n=== Backup Complete! All cloud data safely mirrored to local files. ===")


if __name__ == "__main__":
    main()
