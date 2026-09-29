#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
diff_update.py
用于比对新生成的 tree /F 文本文件与已有数据库的差异，并实现增量更新。

使用方式示例：
    # 当对 16Tdata3 盘重新生成了 haa_new.txt:
    python diff_update.py --vol haa --new haa_new.txt

    # 当对 4000WD 盘重新生成了 qaa_new.txt:
    python diff_update.py --vol qaa --new qaa_new.txt

    # 直接重新全量扫描本地的 haa.txt 与 qaa.txt:
    python diff_update.py --rebuild
"""

import os
import sys
import io
import json
import argparse
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from parse_tree import parse_tree_txt, extract_primary_code, clean_title

DB_PATH = os.path.join(os.path.dirname(__file__), 'db.json')

def load_db():
    if not os.path.exists(DB_PATH):
        print(f"[!] {DB_PATH} 不存在，将通过 parse_tree.py 重新生成...")
        subprocess.run([sys.executable, 'parse_tree.py'], check=True)
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(db):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"[✓] 已更新保存至 {DB_PATH}")

def update_from_new_tree(vol_label, new_tree_file, auto_build=True):
    if not os.path.exists(new_tree_file):
        print(f"[Error] 新树状图文件 {new_tree_file} 不存在！")
        return

    print(f"[*] 正在解析新树状图文件: {new_tree_file} (磁盘代码: {vol_label}) ...")
    new_entries = parse_tree_txt(new_tree_file, vol_label)
    print(f"[*] 新树状图中包含视频文件数量: {len(new_entries)}")

    db = load_db()

    # 建立现有该盘的文件唯一指纹集合: (dir, name)
    existing_fingerprints = set()
    all_recs = []

    for entry in db.get('coded', []):
        for f in entry.get('files', []):
            if f.get('vol') == vol_label:
                existing_fingerprints.add((f.get('dir', ''), f.get('name', '')))

    for entry in db.get('misc', []):
        for f in entry.get('files', []):
            if f.get('vol') == vol_label:
                existing_fingerprints.add((f.get('dir', ''), f.get('name', '')))

    new_fingerprints = set()
    added_entries = []

    for item in new_entries:
        fp = (item['dir_path'], item['filename'])
        new_fingerprints.add(fp)
        if fp not in existing_fingerprints:
            added_entries.append(item)

    removed_count = len(existing_fingerprints - new_fingerprints)

    print("\n" + "="*50)
    print(f"【差异对比结果】 (磁盘: {vol_label})")
    print(f"  - 库中原有文件数: {len(existing_fingerprints)}")
    print(f"  - 新树状图文件数: {len(new_fingerprints)}")
    print(f"  - 新增视频文件: +{len(added_entries)} 个")
    print(f"  - 移除/缺失文件: -{removed_count} 个")
    print("="*50 + "\n")

    if not added_entries and removed_count == 0:
        print("[*] 数据库与新树状图完全一致，无需更新。")
        return

    # 对新增文件进行归类与追加
    coded_dict = {item['id']: item for item in db.get('coded', [])}
    new_codes_added = 0
    merged_into_existing = 0
    added_to_misc = 0

    for e in added_entries:
        fname = e['filename']
        dpath = e['dir_path']
        code, ctype = extract_primary_code(fname)
        if not code:
            code, ctype = extract_primary_code(dpath)

        title = clean_title(fname, code)
        actresses = list(e.get('actress_hints', []))
        file_rec = {
            'name': fname,
            'dir': dpath,
            'vol': vol_label
        }

        if code:
            if code in coded_dict:
                item = coded_dict[code]
                item['files'].append(file_rec)
                if vol_label not in item['vols']:
                    item['vols'].append(vol_label)
                for a in actresses:
                    if a not in item['actresses']:
                        item['actresses'].append(a)
                if len(title) > len(item.get('title', '')):
                    item['title'] = title
                merged_into_existing += 1
            else:
                new_item = {
                    'id': code,
                    'type': ctype,
                    'actresses': actresses,
                    'title': title,
                    'files': [file_rec],
                    'vols': [vol_label]
                }
                coded_dict[code] = new_item
                db['coded'].append(new_item)
                new_codes_added += 1
        else:
            misc_item = {
                'id': None,
                'type': 'misc',
                'actresses': actresses,
                'title': title or fname,
                'files': [file_rec],
                'vols': [vol_label]
            }
            db['misc'].append(misc_item)
            added_to_misc += 1

    print(f"[*] 增量写入统计:")
    print(f"  - 新建番号条目: {new_codes_added}")
    print(f"  - 合并至已有番号条目: {merged_into_existing}")
    print(f"  - 追加至未分类(Misc): {added_to_misc}")

    save_db(db)

    if auto_build:
        print("\n[*] 正在自动重新编译静态页面 index.html ...")
        subprocess.run([sys.executable, 'build_site.py'], check=True)
        print("[*] 正在同步数据至 Vercel KV ...")
        subprocess.run([sys.executable, 'sync_kv.py'], check=True)
        print("[✓] 网站与在线数据库已同步更新！")

def main():
    parser = argparse.ArgumentParser(description="Diff and update AV database from new tree file.")
    parser.add_argument('--vol', choices=['haa', 'qaa'], help="磁盘代码 (haa 对应 16Tdata3, qaa 对应 4000WD)")
    parser.add_argument('--new', help="新生成的 tree /F 文本文件路径")
    parser.add_argument('--rebuild', action='store_true', help="重新执行全量解析并重新构建网站")

    args = parser.parse_args()

    if args.rebuild:
        print("[*] 执行全量重新解析与构建...")
        subprocess.run([sys.executable, 'parse_tree.py'], check=True)
        subprocess.run([sys.executable, 'build_site.py'], check=True)
        return

    if not args.vol or not args.new:
        parser.print_help()
        sys.exit(1)

    update_from_new_tree(args.vol, args.new)

if __name__ == '__main__':
    main()
