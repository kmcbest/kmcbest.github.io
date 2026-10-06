#!/usr/bin/env python3
"""
TFTF Upstash KV to Local Synchronizer
====================================
同步线上站点（Upstash KV）编辑的角色能力与属性数据至本地：
1. 更新 d:\\docforall\\GitHub\\kmcbest.github.io\\tftfr\\data\\characters\\{bot_id}.json
2. 更新 Server/tftf_database.db (character_abilities 与 characters 表)
3. 保持智能体、本地客户端与在线技能中枢数据 100% 同步

用法:
    python tools/sync_from_upstash.py                  # 扫描并同步所有变更金刚
    python tools/sync_from_upstash.py --bot motormaster_gs_voyager2015  # 单独同步指定金刚
"""

import argparse
import json
import os
import sqlite3
import sys
import urllib.request
from pathlib import Path

UPSTASH_URL = "https://deciding-bulldog-136761.upstash.io"
WRITE_TOKEN = "gQAAAAAAAhY5AAIgcDEyZGMwZDRhNzRlZGQ0MDI2YWM2YmI3ZDExNTc3ZjZmNA"
CHAR_DIR = Path(r"d:\docforall\GitHub\kmcbest.github.io\tftfr\data\characters")
DB_PATH = Path(__file__).resolve().parent.parent / "Server" / "tftf_database.db"


def fetch_bot_from_upstash(bot_id: str):
    """从 Upstash KV 读取单机体完整数据字典。"""
    req = urllib.request.Request(
        f"{UPSTASH_URL}/get/tftf:char:{bot_id}",
        headers={"Authorization": f"Bearer {WRITE_TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if res.get("result"):
            val = res["result"]
            return json.loads(val) if isinstance(val, str) else val
    return None


def fetch_all_keys():
    """获取 Upstash 中所有角色 key。"""
    req = urllib.request.Request(
        f"{UPSTASH_URL}/keys/tftf:char:*",
        headers={"Authorization": f"Bearer {WRITE_TOKEN}"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res.get("result", [])


def fetch_pipeline_batch(keys: list):
    """批量通过 pipeline 拉取数据。"""
    chunk_size = 25
    all_data = {}
    for i in range(0, len(keys), chunk_size):
        chunk = keys[i:i + chunk_size]
        cmds = [["GET", k] for k in chunk]
        req = urllib.request.Request(
            f"{UPSTASH_URL}/pipeline",
            headers={"Authorization": f"Bearer {WRITE_TOKEN}", "Content-Type": "application/json"},
            data=json.dumps(cmds).encode("utf-8")
        )
        with urllib.request.urlopen(req) as resp:
            res_list = json.loads(resp.read().decode("utf-8"))
            for k, item in zip(chunk, res_list):
                val = item.get("result")
                if val:
                    bid = k.replace("tftf:char:", "")
                    all_data[bid] = json.loads(val) if isinstance(val, str) else val
    return all_data


def sync_bot_to_local_json(bot_id: str, up_data: dict) -> bool:
    """写入本地 JSON 文件。"""
    if not CHAR_DIR.exists():
        print(f"[WARN] Local characters directory not found: {CHAR_DIR}")
        return False
    target = CHAR_DIR / f"{bot_id}.json"
    formatted = json.dumps(up_data, ensure_ascii=False, indent=2) + "\n"
    target.write_text(formatted, encoding="utf-8")
    print(f"  [+] Updated local JSON: {target.name}")
    return True


def sync_bot_to_sqlite(bot_id: str, up_data: dict) -> int:
    """将机体能力同步写入 Server/tftf_database.db。"""
    if not DB_PATH.exists():
        print(f"[WARN] Local SQLite database not found: {DB_PATH}")
        return 0

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # 1. 同步角色属性
    attrs = ["crit_chance", "crit_damage", "crit_chance_ranged", "crit_chance_melee", "block_proficiency", "pua_faction_icon"]
    set_clauses = []
    vals = []
    for a in attrs:
        if a in up_data and up_data[a] is not None:
            set_clauses.append(f"{a}=?")
            vals.append(up_data[a])
    if set_clauses:
        vals.append(bot_id)
        cur.execute(f"UPDATE characters SET {', '.join(set_clauses)} WHERE bot_id=?", vals)

    # 2. 同步技能列表
    abilities = up_data.get("abilities", [])
    valid_ids = []
    changes = 0

    for ab in abilities:
        aid = ab.get("id")
        if aid is None:
            continue
        try:
            aid = int(aid)
        except Exception:
            pass
        valid_ids.append(aid)

        cat = ab.get("category", "basic")
        tzh = ab.get("title_zh", "")
        ten = ab.get("title_en", "")
        dzh = ab.get("desc_zh", "")
        den = ab.get("desc_en", "")
        pua = ab.get("pua_icon", "")
        raw = ab.get("raw_data_json", "")
        order = ab.get("sort_order", 0)
        syn = json.dumps(ab.get("synergy_bots", [])) if isinstance(ab.get("synergy_bots"), list) else str(ab.get("synergy_bots") or "[]")
        status = ab.get("status", "unimplemented")

        # 检查是否存在
        cur.execute("SELECT id FROM character_abilities WHERE id=?", (aid,))
        row = cur.fetchone()
        if row:
            cur.execute(
                """
                UPDATE character_abilities
                SET bot_id=?, category=?, title_zh=?, title_en=?, desc_zh=?, desc_en=?,
                    pua_icon=?, raw_data_json=?, sort_order=?, synergy_bots=?, status=?
                WHERE id=?
                """,
                (bot_id, cat, tzh, ten, dzh, den, pua, raw, order, syn, status, aid)
            )
        else:
            cur.execute(
                """
                INSERT INTO character_abilities
                (id, bot_id, category, title_zh, title_en, desc_zh, desc_en, pua_icon, raw_data_json, sort_order, synergy_bots, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (aid, bot_id, cat, tzh, ten, dzh, den, pua, raw, order, syn, status)
            )
        changes += 1

    # 3. 删除线上已删除的能力 (如果本地能力多于线上)
    if valid_ids:
        cur.execute(
            f"DELETE FROM character_abilities WHERE bot_id=? AND id NOT IN ({','.join(['?']*len(valid_ids))})",
            [bot_id] + valid_ids
        )

    conn.commit()
    conn.close()
    print(f"  [+] Synced {changes} abilities into SQLite character_abilities for {bot_id}")
    return changes


def main():
    parser = argparse.ArgumentParser(description="Sync character abilities from Upstash KV to local.")
    parser.add_argument("--bot", type=str, default="", help="Specific bot_id to sync.")
    args = parser.parse_args()

    print("=== TFTF Upstash KV -> Local Synchronizer ===")

    if args.bot:
        bid = args.bot.strip()
        print(f"Fetching {bid} from Upstash...")
        data = fetch_bot_from_upstash(bid)
        if not data:
            print(f"[!] Bot {bid} not found in Upstash KV!")
            sys.exit(1)
        sync_bot_to_local_json(bid, data)
        sync_bot_to_sqlite(bid, data)
        print("\n[OK] Sync completed successfully for " + bid)
        return

    # 全量扫描检测
    keys = fetch_all_keys()
    print(f"Found {len(keys)} bots in Upstash KV. Fetching data in batch...")
    all_data = fetch_pipeline_batch(keys)

    synced_count = 0
    for bot_id, up_data in all_data.items():
        loc_path = CHAR_DIR / f"{bot_id}.json"
        if not loc_path.exists():
            continue
        try:
            loc_data = json.loads(loc_path.read_text(encoding="utf-8"))
        except Exception:
            loc_data = {}

        # 比较是否有实质更新
        up_str = json.dumps(up_data, sort_keys=True, ensure_ascii=False)
        loc_str = json.dumps(loc_data, sort_keys=True, ensure_ascii=False)
        if up_str != loc_str:
            print(f"\n[*] Found differences for [{bot_id}]:")
            sync_bot_to_local_json(bot_id, up_data)
            sync_bot_to_sqlite(bot_id, up_data)
            synced_count += 1

    if synced_count == 0:
        print("\n[OK] All local JSON files and SQLite are already up to date with Upstash KV!")
    else:
        print(f"\n[OK] Successfully synchronized {synced_count} bots from Upstash KV to local!")


if __name__ == "__main__":
    main()
