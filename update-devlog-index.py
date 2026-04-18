#!/usr/bin/env python3
"""
devlog/ 폴더를 스캔하여 devlog/index.json + devlog/index.js 를 생성한다.

실행:
    cd ~/Desktop/Projects/masterboard
    python3 update-devlog-index.py

devlog 파일 규칙:
    파일명: YYYY-MM-DD-{project}[-N].md   (예: 2026-04-18-masterboard.md, 2026-04-17-nudge-2.md)
    첫 줄:  # [project] YYYY-MM-DD — 한 줄 요약

출력:
    devlog/index.json — 기존 포맷 유지(사람/외부 툴용)
    devlog/index.js   — window.DEVLOG_INDEX = [...]  (project.html 등 브라우저용)
"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEVLOG_DIR = os.path.join(ROOT, 'devlog')

FN_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})-([a-z]+)(?:-(\d+))?\.md$')
DATE_RE = re.compile(r'\d{4}-\d{2}-\d{2}')

def clean_title(first_line, project):
    """h1 라인에서 # / [project] / project / 날짜 / 구분자(—–-)를 벗겨 실제 title만 남긴다."""
    t = first_line.strip()
    t = re.sub(r'^#+\s*', '', t)                    # leading #
    t = re.sub(r'^\[[^\]]+\]\s*', '', t)            # [project]
    # 'project ' prefix (대소문자 무관)
    t = re.sub(rf'^{re.escape(project)}\b\s*', '', t, flags=re.IGNORECASE)
    t = DATE_RE.sub('', t, count=1)                 # 날짜 1회
    t = t.strip().lstrip('—–-').strip()
    return t

def extract(path):
    fname = os.path.basename(path)
    if fname.startswith('_'):  # _TEMPLATE.md 등
        return None
    m = FN_RE.match(fname)
    if not m:
        return None
    date, project, _ = m.groups()
    title = ''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith('#'):
                    continue
                title = clean_title(line, project)
                break
    except Exception as e:
        print(f'WARN: {fname} 읽기 실패: {e}', file=sys.stderr)
    return {'file': fname, 'date': date, 'project': project, 'title': title}

def main():
    if not os.path.isdir(DEVLOG_DIR):
        print(f'ERR: {DEVLOG_DIR} 없음', file=sys.stderr); sys.exit(1)

    entries = []
    for fname in os.listdir(DEVLOG_DIR):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(DEVLOG_DIR, fname)
        e = extract(path)
        if e:
            entries.append(e)

    # 날짜 내림차순 + 같은 날짜면 세션 번호 내림차순(2차 세션이 1차보다 위),
    # 같은 세션 번호면 project 이름 알파벳 순
    def sort_key(e):
        m = FN_RE.match(e['file'])
        sess = int(m.group(3)) if m and m.group(3) else 1
        return (e['date'], sess, e['project'])
    entries.sort(key=sort_key, reverse=True)

    # index.json
    with open(os.path.join(DEVLOG_DIR, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
        f.write('\n')

    # index.js (브라우저 로드용)
    with open(os.path.join(DEVLOG_DIR, 'index.js'), 'w', encoding='utf-8') as f:
        f.write('window.DEVLOG_INDEX = ')
        json.dump(entries, f, ensure_ascii=False, indent=2)
        f.write(';\n')

    # 요약
    from collections import Counter
    by_proj = Counter(e['project'] for e in entries)
    print(f'✅ devlog 인덱스 갱신 완료 — 총 {len(entries)}개')
    for p, c in sorted(by_proj.items(), key=lambda x: -x[1]):
        print(f'   {p:14} {c}')

if __name__ == '__main__':
    main()
