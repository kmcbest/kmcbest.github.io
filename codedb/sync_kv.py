#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_kv.py
同步本地 db.json 数据至 Vercel KV / Upstash Redis 在线数据库。
"""

import os
import sys
import io
import json
import time
import urllib.request
import urllib.error

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

KV_REST_API_URL = "https://deciding-bulldog-136761.upstash.io"
KV_REST_API_TOKEN = "gQAAAAAAAhY5AAIgcDEyZGMwZDRhNzRlZGQ0MDI2YWM2YmI3ZDExNTc3ZjZmNA"
KV_REST_API_READ_ONLY_TOKEN = "ggAAAAAAAhY5AAIgcDG7a511dMnvUap5JjML7kdCMH0hQAG95-3BtwD6YEaFeQ"

DB_PATH = os.path.join(os.path.dirname(__file__), 'db.json')

def push_to_kv():
    if not os.path.exists(DB_PATH):
        print(f"[!] 找不到 {DB_PATH}")
        return False

    print(f"[*] 正在读取本地 {DB_PATH} ...")
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db_obj = json.load(f)

    compact_json = json.dumps(db_obj, ensure_ascii=False, separators=(',', ':'))
    meta_info = {
        'updated_at': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        'coded_count': len(db_obj.get('coded', [])),
        'misc_count': len(db_obj.get('misc', [])),
        'total_videos': len(db_obj.get('coded', [])) + len(db_obj.get('misc', [])),
        'vols': list(db_obj.get('vol_labels', {}).values())
    }

    print(f"[*] 正在向 Vercel KV ({KV_REST_API_URL}) 同步写入数据...")

    def upstash_cmd(cmd_list):
        data_bytes = json.dumps(cmd_list).encode('utf-8')
        req = urllib.request.Request(
            KV_REST_API_URL,
            data=data_bytes,
            headers={
                'Authorization': f'Bearer {KV_REST_API_TOKEN}',
                'Content-Type': 'application/json'
            }
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    # 1. 写入主数据表 codedb:all
    res_all = upstash_cmd(['SET', 'codedb:all', compact_json])
    print(f"  - [codedb:all] 写入状态: {res_all.get('result')}")

    # 2. 写入元数据表 codedb:meta
    res_meta = upstash_cmd(['SET', 'codedb:meta', json.dumps(meta_info)])
    print(f"  - [codedb:meta] 写入状态: {res_meta.get('result')} (更新时间: {meta_info['updated_at']})")

    print("[✓] 数据库同步成功！")
    return True

if __name__ == '__main__':
    push_to_kv()
