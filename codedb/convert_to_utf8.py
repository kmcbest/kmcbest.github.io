#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_to_utf8.py
将 GB18030/GBK 编码的 tree 文件无损转换为标准的 UTF-8 文件。
同时备份原文件为 .bak。
"""

import os
import sys
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

FILES = ['haa.txt', 'qaa.txt']

def convert():
    for fname in FILES:
        if not os.path.exists(fname):
            continue

        bak_name = fname + '.gbk.bak'
        src_file = fname
        if os.path.exists(bak_name):
            src_file = bak_name
        else:
            shutil.copyfile(fname, bak_name)
            print(f"[*] 已备份原始文件至 {bak_name}")

        print(f"[*] 正在读取 {src_file} (使用 GB18030 解码全量汉字/日文字符)...")
        with open(src_file, 'r', encoding='gb18030', errors='replace') as f:
            content = f.read()

        print(f"[*] 正在将 {fname} 写入为标准 UTF-8 编码...")
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[✓] {fname} 转换完成！")

if __name__ == '__main__':
    convert()
