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

# 常见平台与番号正则表达式
_FC2_PAT   = re.compile(r'\bFC2(?:[-_\s]?PPV)?[-_\s]?(\d{5,8})\b', re.I)
_1PON_PAT  = re.compile(r'\b(?:1Pondo|1pon)[-_\s]+(\d{6}[-_]\d{2,4})\b', re.I)
_CARIB_PAT = re.compile(r'\b(?:Caribbeancom|Carib)[-_\s]+(\d{6}[-_]\d{2,4})\b', re.I)
_PACO_PAT  = re.compile(r'\b(?:Pacopacomama|paco)[-_\s]+(\d{6}[-_]\d{2,4})\b', re.I)
_10MU_PAT  = re.compile(r'\b(?:10musume|10mu)[-_\s]+(\d{6}[-_]\d{2,4})\b', re.I)
_HEYZO_PAT = re.compile(r'\bHEYZO(?:_hd|_lt)?[-_\s]+(\d{3,5})\b', re.I)
_HEYD_PAT  = re.compile(r'\bHeydouga[-_\s]+(\d{4}[-_\s]\d{2,4})\b', re.I)
_SUFFIX_BRAND_PAT = re.compile(r'\b(\d{6}[-_]\d{2,4})[-_]?(carib|1pon|10mu|paco)\b', re.I)

# 增强的标准与变体 JAV 番号正则：
# 匹配各种带连字符、下划线、空格、或紧密连接的番号，例如：
# SPRD-1233C, SPRD1233C, SPRD 1233C, SPRD-1233-RM-C, nacr-282, xrw-642, ABP-001, MD0190, PM086 等
_JAV_ENHANCED = re.compile(
    r'(?<![A-Za-z0-9])([A-Za-z]{2,7})[-_\s]?(\d{2,5})([A-Za-z]?)(?:[-_](?:c|ch|rm|uc|sub|cd\d|part\d|uncensored|4k|fhd))?',
    re.I
)

# 排除常见误判的前缀
_IGNORE_PREFIXES = {
    'MP4', 'MKV', 'AVI', 'WMV', 'MOV', 'TS', 'FLV', 'ISO',
    'UHD', 'FHD', '1080P', '720P', 'H264', 'H265', 'X264', 'HEVC',
    'AAC', 'AC3', 'DTS', 'FLAC', 'HDR', 'SDR',
    'DISC', 'PART', 'VOL', 'EP', 'SET', 'FILE', 'CLIP', 'SAMPLE', 'PREVIEW',
    'FLASH', 'PHOTO', 'BOOK', 'CHAT', 'LIVE', 'DATE', 'EXTRA', 'BONUS',
    'GIRL', 'MISS', 'ASIA', 'TOKYO', 'GOOD', 'LOVE', 'BABY', 'HOT',
    'DOC', 'TXT', 'ZIP', 'RAR', 'VID', 'HTTP', 'WWW', 'COM', 'NET', 'ORG'
}

def extract_primary_code(text: str):
    """
    返回: (disp_code, base_code, ctype, is_sub, is_rm) 或 (None, None, 'misc', False, False)
    """
    if not text:
        return None, None, 'misc', False, False

    # 1. FC2
    m = _FC2_PAT.search(text)
    if m:
        code_str = f'FC2PPV-{m.group(1)}'
        return code_str, code_str, 'fc2', False, False

    # 2. 1Pondo
    m = _1PON_PAT.search(text)
    if m:
        num = m.group(1).replace('_', '-')
        code_str = f'1PON-{num}'
        return code_str, code_str, 'jav', False, False

    # 3. Caribbeancom
    m = _CARIB_PAT.search(text)
    if m:
        num = m.group(1).replace('_', '-')
        code_str = f'CARIB-{num}'
        return code_str, code_str, 'jav', False, False

    # 4. Pacopacomama
    m = _PACO_PAT.search(text)
    if m:
        num = m.group(1).replace('_', '-')
        code_str = f'PACO-{num}'
        return code_str, code_str, 'jav', False, False

    # 5. 10musume
    m = _10MU_PAT.search(text)
    if m:
        num = m.group(1).replace('_', '-')
        code_str = f'10MU-{num}'
        return code_str, code_str, 'jav', False, False

    # 6. 后缀平台形式，如 013120-001-carib
    m = _SUFFIX_BRAND_PAT.search(text)
    if m:
        num = m.group(1).replace('_', '-')
        brand_map = {'carib': 'CARIB', '1pon': '1PON', '10mu': '10MU', 'paco': 'PACO'}
        brand = brand_map.get(m.group(2).lower(), 'CARIB')
        code_str = f'{brand}-{num}'
        return code_str, code_str, 'jav', False, False

    # 7. HEYZO
    m = _HEYZO_PAT.search(text)
    if m:
        code_str = f'HEYZO-{m.group(1)}'
        return code_str, code_str, 'jav', False, False

    # 8. Heydouga
    m = _HEYD_PAT.search(text)
    if m:
        num_clean = re.sub(r'[-_\s]+', '-', m.group(1))
        code_str = f'HEYDOUGA-{num_clean}'
        return code_str, code_str, 'jav', False, False

    # 9. 增强型 JAV 匹配 (支持大小写、带C字幕尾缀、空格分隔等)
    for m in _JAV_ENHANCED.finditer(text):
        pre = m.group(1).upper()
        if pre in _IGNORE_PREFIXES:
            continue

        num = m.group(2)
        tail = m.group(3).upper() if m.group(3) else ''

        # 核心基准番号（用于去重主键，如 SPRD-1233）
        base_code = f'{pre}-{num}'

        # 判断是否中文字幕/破解
        matched_str = m.group(0)
        is_sub = (tail == 'C') or bool(re.search(r'[-_](?:c|ch|sub)\b', matched_str, re.I)) or ('中文字幕' in text) or ('中文' in text)
        is_rm = bool(re.search(r'[-_](?:rm|uc|uncensored)\b', matched_str, re.I)) or ('破解' in text) or ('无码' in text) or ('流出' in text)

        # 展示番号：若检测为中文字幕，优先展示带 C 后缀，如 SPRD-1233C
        if is_sub and not tail:
            disp_code = f'{pre}-{num}C'
        elif tail:
            disp_code = f'{pre}-{num}{tail}'
        else:
            disp_code = base_code

        return disp_code, base_code, 'jav', is_sub, is_rm

    return None, None, 'misc', False, False

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

def clean_title(raw: str, disp_code: str, base_code: str = None) -> str:
    t = raw
    t = re.sub(r'\.[a-z0-9]{2,5}$', '', t, flags=re.I)
    t = SITE_SUFFIXES.sub('', t)

    # 移除番号代码与常见前缀
    for c in [disp_code, base_code]:
        if c:
            safe = re.escape(c).replace(r'\-', r'[-_\s]?')
            t = re.sub(r'(?i)' + safe, '', t)
            nodash = re.sub(r'[-_]', '', c)
            t = re.sub(r'(?i)\b' + re.escape(nodash) + r'\b', '', t)

    # 移除常见的修饰后缀
    t = re.sub(r'(?i)[-_]?(?:Tagged_by_[A-Za-z0-9]+|RM|UC|uncensored|4k|fhd|cd\d|part\d)', '', t)
    t = re.sub(r'^FC2[-\s]?PPV[-\s]?\d+\s*', '', t, flags=re.I)
    t = re.sub(r'^\s*[\[\(][^\]\)]{0,40}[\]\)]\s*', '', t).strip()
    t = re.sub(r'\b\d{8,}\b', '', t)
    t = t.replace('\ufffd', '').replace('', '')
    t = re.sub(r'\s+', ' ', t).strip(' -–_.')
    return t

def build_db(all_entries: list) -> dict:
    coded = {}
    misc = []

    for e in all_entries:
        fname = e['filename']
        dpath = e['dir_path']

        disp_code, base_code, ctype, is_sub, is_rm = extract_primary_code(fname)
        if not base_code:
            disp_code, base_code, ctype, is_sub, is_rm = extract_primary_code(dpath)

        title = clean_title(fname, disp_code, base_code)
        actresses = list(e['actress_hints'])

        file_rec = {
            'name': fname.replace('\ufffd', '').replace('', ''),
            'dir':  dpath.replace('\ufffd', '').replace('', ''),
            'vol':  e['source'],
        }

        if base_code:
            if base_code not in coded:
                coded[base_code] = {
                    'id':        disp_code,
                    'base_code': base_code,
                    'type':      ctype,
                    'is_sub':    is_sub,
                    'is_rm':     is_rm,
                    'actresses': actresses,
                    'title':     title,
                    'files':     [file_rec],
                    'vols':      [e['source']],
                }
            else:
                ex = coded[base_code]
                ex['files'].append(file_rec)
                for a in actresses:
                    if a not in ex['actresses']:
                        ex['actresses'].append(a)
                if e['source'] not in ex['vols']:
                    ex['vols'].append(e['source'])
                # 如果新切片带有中文字幕标记，提升主卡片显示番号为带 C 版本
                if is_sub:
                    ex['is_sub'] = True
                    if not ex['id'].endswith('C'):
                        ex['id'] = f"{base_code}C"
                if is_rm:
                    ex['is_rm'] = True
                # 保留更详实丰富的标题
                if len(title) > len(ex['title']):
                    ex['title'] = title
        else:
            misc.append({
                'id':        None,
                'base_code': None,
                'type':      'misc',
                'is_sub':    False,
                'is_rm':     False,
                'actresses': actresses,
                'title':     title or fname,
                'files':     [file_rec],
                'vols':      [e['source']],
            })

    return {
        'version': 2,
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
