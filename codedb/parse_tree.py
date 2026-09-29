#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_tree.py  -  Parse Windows `tree /F` output into clean db.json
Features:
- Robust multi-encoding read (UTF-8, GB18030, GBK fallback)
- Auto Mojibake / corruption repairing for well-known actress names
- Removes broken encoding artifacts (\ufffd, ?, etc.)
- Normalizes actress categories & video codes
"""

import re
import json
import sys
import io
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SOURCES = [
    ('haa.txt', 'haa', '16Tdata3'),
    ('qaa.txt', 'qaa', '4000WD'),
]

VIDEO_EXTS = {'.mp4', '.ts', '.mkv', '.avi', '.wmv', '.mov',
              '.flv', '.rmvb', '.m4v', '.iso'}

NON_ACTRESS_DIRS = {
    '#China', '#Foot_fetish', '#Gravure', '#Lesbian', '#Misc', '#OK',
    '#simp', '#ThemePark', '#Uncensored Leaked Misc', '#剧情', '#字幕SRT',
    '#瓜', '#麻豆', '#AIGC', '#HTML', '#Magazine', '#unsorted', '#Hardcore-BG',
    '#Onlyfans-PostHiatus', '#Set', '#Hardcore', '#Vids', '#Cam-Vids',
    '#Girls in Nature', '#Met-Art', '#Femjoy',
    'AIGC', 'close', 'cut', 'mp4', 'photos', 'photo', 'Galleries',
    'Gallery 1', 'Gallery 2', 'Gallery 3', 'Gallery 4', 'backup',
    '69', 'anal', 'blow', 'cowgirl-back', 'cowgirl-front', 'cunni',
    'doggy', 'foot_fetish', 'Sampel', 'Sample', 'bonus', 'Bonus',
    'STOCK', 'wd', 'zsq', 'zsq1', 'Lesbian', 'Strapon', 'Anal',
    'Evolved Fights', 'Foot fetish', 'Lesbian Desires',
}

SITE_SUFFIXES = re.compile(
    r'\s*[-–]\s*(Supjav\.com[^)]*|MissAV[^)]*|Xasiat[^)]*|'
    r'Bunkr[^)]*|Pornhub\.com|XVIDEOS\.COM|XNXX\.COM|'
    r'madouvideo\.org|TOKYO Motion|HdZog[^)]*|'
    r'肉联盟.*|您的私人AV影院|免费高清AV在线看|'
    r'在线看|Free JAV.*|伊莉影片.*|影片台.*)\s*$',
    re.I
)

# 常见日文/繁体乱码女优智能纠偏表
KNOWN_NAME_FIXES = {
    '美@和花': '美園和花 (Misono Waka)',
    '美園和花': '美園和花 (Misono Waka)',
    '小田wB(Asuka Oda)': '小田飛鳥 (Asuka Oda)',
    '小田飛鳥(Asuka Oda)': '小田飛鳥 (Asuka Oda)',
    '中村知{': '中村知恵 (Chie Nakamura)',
    '中村知恵': '中村知恵 (Chie Nakamura)',
    'RION-安Sらら': 'RION / 安齋らら',
    'RION-安齋らら': 'RION / 安齋らら',
    '吉根ゆりあ（吉根柚莉郏': '吉根ゆりあ (吉根柚莉爱)',
    '吉根ゆりあ（吉根柚莉爱）': '吉根ゆりあ (吉根柚莉爱)',
    '竹劝(Ai Takeuchi)': '竹内あい (Ai Takeuchi)',
    '竹内あい(Ai Takeuchi)': '竹内あい (Ai Takeuchi)',
    'm下玲奈': '宮下玲奈 (Reina Miyashita)',
    '宮下玲奈': '宮下玲奈 (Reina Miyashita)',
    'm城りえ': '宮城りえ (Rie Miyagi)',
    '宮城りえ': '宮城りえ (Rie Miyagi)',
    '恋mももな（恋m桃奈）': '恋渕ももな (恋渕桃奈)',
    '恋渕ももな（恋渕桃奈）': '恋渕ももな (恋渕桃奈)',
    '碧しの-碧诗乃-Sめぐみ-S惠美': '碧しの / 安齋めぐみ',
    '佐山': '佐山愛 (Ai Sayama)',
    '佐山愛': '佐山愛 (Ai Sayama)',
    '乃操': '綾乃操 (Misao Ayano)',
    '綾乃操': '綾乃操 (Misao Ayano)',
    '小啾老': '小啾老师',
    '小啾老师': '小啾老师',
    '中文语音': '中文语音包',
    '中文语音包': '中文语音包',
    '双~みれい': '双葉みれい',
    '双葉みれい': '双葉みれい',
    '三颏ん': '三上悠亜',
    '三田悠F': '三田悠貴',
    '京Oなな': '京極なな',
    '伊いお': '伊織いお',
    '原つむぎ（Tsumugi Hara）': '原つむぎ (Tsumugi Hara)',
    '夏来唯（Yui Natsuki）': '夏来唯 (Yui Natsuki)',
    '中山ふみか（Fumika Nakayama）': '中山ふみか (Fumika Nakayama)',
    '吉野千q（ちとせよしの）': '吉野千尋 (ちとせよしの)',
}

_JAV_PAT   = re.compile(r'\b([A-Z]{2,7}-\d{3,5})\b')
_JAV2_PAT  = re.compile(r'\b([A-Z]{2,7}\d{3,5})\b')
_FC2_PAT   = re.compile(r'\bFC2[-\s]?PPV[-\s]?(\d{5,8})\b', re.I)
_CARIB_PAT = re.compile(r'\b(\d{6}[-_]\d{3})[-_](1pon|carib|mura|10mu|kin8)\b', re.I)
_HEYD_PAT  = re.compile(r'\bHeydouga[-\s]+(\d{4}[-\s]\d{2,4})\b', re.I)
_HEYZO_PAT = re.compile(r'\bHEYZO[-\s]+(\d{3,5})\b', re.I)
_1PON_PAT  = re.compile(r'\b1Pondo\s+(\d{6}[-_]\d{3})\b', re.I)
_CARIB2_PAT= re.compile(r'\bCaribbeancom\s+(\d{6}-\d{3})\b', re.I)

_IGNORE_CODES = {
    'EP1', 'EP2', 'EP3', 'EP4', 'EP5', 'EP6', 'EP7', 'EP8', 'EP9',
    'VOL1', 'VOL2', 'MP4', 'AVI', 'MKV', 'XXX', 'JAV', 'BTS',
    'SET1', 'SET2', 'UHD', 'FHD', 'HD', 'DOC', 'TXT', 'ZIP', 'RAR'
}

def extract_primary_code(text: str):
    m = _FC2_PAT.search(text)
    if m:
        return f'FC2PPV-{m.group(1)}', 'fc2'

    m = _CARIB2_PAT.search(text)
    if m:
        return 'CARIB-' + m.group(1).replace('-', ''), 'jav'

    m = _1PON_PAT.search(text)
    if m:
        return '1PON-' + m.group(1).replace('_', '-'), 'jav'

    m = _HEYZO_PAT.search(text)
    if m:
        return 'HEYZO-' + m.group(1), 'jav'

    m = _CARIB_PAT.search(text)
    if m:
        return m.group(1).upper().replace('_', '-'), 'jav'

    m = _HEYD_PAT.search(text)
    if m:
        return 'HEYDOUGA-' + m.group(1).replace(' ', '-'), 'jav'

    for m in _JAV_PAT.finditer(text):
        c = m.group(1).upper()
        if c not in _IGNORE_CODES:
            return c, 'jav'

    for m in _JAV2_PAT.finditer(text):
        c = m.group(1).upper()
        if c not in _IGNORE_CODES and len(c) >= 5:
            inner = re.match(r'^([A-Z]+)(\d+)$', c)
            if inner:
                return inner.group(1) + '-' + inner.group(2), 'jav'

    return None, 'misc'

_CJK_RE = re.compile(r'[\u4e00-\u9fff\u3040-\u30ff\uff00-\uffef]')

def clean_name(raw_name: str) -> str:
    """清洗女优名字，去除乱码符号并进行已知字典修正"""
    if not raw_name:
        return ''
    s = raw_name.strip()

    # 查字典优先命中
    for k, v in KNOWN_NAME_FIXES.items():
        if k in s:
            return v

    # 去除菱形问号与不可打印字符
    s = s.replace('\ufffd', '').replace('', '')

    # 提取括号里的干净英文名（如 Asuka Oda）
    m_en = re.search(r'\(([A-Za-z\s]+)\)', s)
    if m_en and len(m_en.group(1).strip()) > 3:
        # 如果中文部分严重乱码（含畸形字符），优先展示纯英文名
        clean_prefix = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]', '', s[:s.find('(')])
        if len(clean_prefix) >= 2:
            return f"{clean_prefix} ({m_en.group(1).strip()})"
        return m_en.group(1).strip()

    # 清理多余空格与异常符号
    s = re.sub(r'[\?@\{~\^]+', ' ', s).strip()
    return s

def looks_like_actress(name: str) -> bool:
    if not name or name in NON_ACTRESS_DIRS:
        return False
    if name.startswith('#') or name.startswith('@') or name.startswith('['):
        return False
    if name.startswith('20') and len(name) > 6:
        return False
    if re.match(r'^[A-Z]{2,7}[-]?\d{3,5}$', name):
        return False
    if '.' in name and len(name) < 12:
        return False
    if _CJK_RE.search(name):
        return True
    if re.match(r'^[A-Z][a-z]+(?: [A-Z][a-z]+){1,2}$', name):
        return True
    return False

def parse_tree_txt(filepath: str, source_label: str) -> list:
    lines = []
    # 优先使用 UTF-8，回退到 GB18030
    for enc in ['utf-8', 'gb18030', 'gbk']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                lines = f.readlines()
            break
        except UnicodeDecodeError:
            continue

    path_stack = []
    entries = []

    for raw_line in lines:
        line = raw_line.rstrip('\n\r')
        if not line.strip():
            continue

        stripped = line.strip()
        if (stripped.startswith('卷') or
                re.match(r'^[A-Za-z]:[\\./]', stripped) or
                stripped.startswith('卷序列号')):
            continue

        has_branch = '├─' in line or '└─' in line
        depth = 0
        for ch in line:
            if ch == '│':
                depth += 1
            elif ch in '├└':
                depth += 1
                break
            elif ch in (' ', '\t'):
                continue
            else:
                break

        if has_branch:
            name = re.split(r'[├└]─\s?', line, 1)[-1].strip()
            is_dir = True
        else:
            name = re.sub(r'^[│ \t├└─]+', '', line).strip()
            is_dir = False

        if not name:
            continue

        if is_dir:
            while path_stack and path_stack[-1][0] >= depth:
                path_stack.pop()
            path_stack.append([depth, name])
        else:
            if Path(name).suffix.lower() not in VIDEO_EXTS:
                continue

            dir_path = '/'.join(p[1] for p in path_stack)

            actress_hints = []
            for _, dname in path_stack:
                if looks_like_actress(dname):
                    c_name = clean_name(dname)
                    if c_name and len(c_name) >= 2:
                        actress_hints.append(c_name)

            entries.append({
                'filename': name,
                'dir_path': dir_path,
                'actress_hints': actress_hints,
                'source': source_label,
            })

    return entries

def clean_title(raw: str, code: str) -> str:
    t = raw
    t = re.sub(r'\.[a-z0-9]{2,5}$', '', t, flags=re.I)
    t = SITE_SUFFIXES.sub('', t)
    if code:
        safe = re.escape(code).replace(r'\-', '[-]?')
        t = re.sub(r'(?i)' + safe, '', t)
        nodash = re.sub(r'-', '', code)
        t = re.sub(r'(?i)\b' + re.escape(nodash) + r'\b', '', t)
    t = re.sub(r'^FC2[-\s]?PPV[-\s]?\d+\s*', '', t, flags=re.I)
    t = re.sub(r'^\s*[\[\(][^\]\)]{0,40}[\]\)]\s*', '', t).strip()
    t = re.sub(r'\b\d{8,}\b', '', t)
    # 清除乱码问号符号
    t = t.replace('\ufffd', '').replace('', '')
    t = re.sub(r'\s+', ' ', t).strip(' -–_.')
    return t

def build_db(all_entries: list) -> dict:
    coded = {}
    misc = []

    for e in all_entries:
        fname = e['filename']
        dpath = e['dir_path']

        code, ctype = extract_primary_code(fname)
        if not code:
            code, ctype = extract_primary_code(dpath)

        title = clean_title(fname, code)
        actresses = list(e['actress_hints'])

        file_rec = {
            'name': fname.replace('\ufffd', '').replace('', ''),
            'dir':  dpath.replace('\ufffd', '').replace('', ''),
            'vol':  e['source'],
        }

        if code:
            if code not in coded:
                coded[code] = {
                    'id':       code,
                    'type':     ctype,
                    'actresses': actresses,
                    'title':    title,
                    'files':    [file_rec],
                    'vols':     [e['source']],
                }
            else:
                ex = coded[code]
                ex['files'].append(file_rec)
                for a in actresses:
                    if a not in ex['actresses']:
                        ex['actresses'].append(a)
                if e['source'] not in ex['vols']:
                    ex['vols'].append(e['source'])
                if len(title) > len(ex['title']):
                    ex['title'] = title
        else:
            misc.append({
                'id':       None,
                'type':     'misc',
                'actresses': actresses,
                'title':    title or fname,
                'files':    [file_rec],
                'vols':     [e['source']],
            })

    return {
        'version': 1,
        'vol_labels': {'haa': '16Tdata3', 'qaa': '4000WD'},
        'coded':  list(coded.values()),
        'misc':   misc,
    }

if __name__ == '__main__':
    all_entries = []
    for filepath, label, disk_name in SOURCES:
        if not Path(filepath).exists():
            print(f'[SKIP] {filepath} not found')
            continue
        print(f'Parsing {filepath} ({disk_name}) ...', end=' ', flush=True)
        entries = parse_tree_txt(filepath, label)
        print(f'{len(entries)} video files')
        all_entries.extend(entries)

    print(f'\nTotal raw video entries: {len(all_entries)}')
    print('Merging and normalizing by code ...')

    db = build_db(all_entries)

    print(f'  Coded entries : {len(db["coded"])}')
    print(f'  Misc entries  : {len(db["misc"])}')

    out_path = 'db.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    print(f'\n[✓] Saved {out_path}')
