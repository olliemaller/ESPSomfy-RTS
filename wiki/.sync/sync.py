#!/usr/bin/env python3
"""Keep the English wiki in step with xkain's French wiki.

Usage (run from the English wiki checkout; FR is a checkout of xkain/ESPSomfy-RTS.wiki):
  sync.py status FR            French pages changed, added or deleted since the last sync
  sync.py fix FR Page.md ...   rewrite French link targets in freshly translated English pages
  sync.py check FR             every link points to an English page and an existing heading
  sync.py done FR              record the French pages' current versions as translated

A translated page keeps the French page's links untouched and the same headings, in the same
order and at the same levels. `fix` then maps pages through pages.json and anchors by heading
position.
"""
import json, os, re, subprocess, sys, unicodedata
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
EN = os.path.dirname(HERE)
PAGES = json.load(open(os.path.join(HERE, 'pages.json'), encoding='utf-8'))
STATE = os.path.join(HERE, 'state.json')
NFC = lambda s: unicodedata.normalize('NFC', s)
FR_BY_KEY = {NFC(k).lower(): k for k in PAGES}
EN_FILES = {v[0] for v in PAGES.values()}
WIKI = r'(?:https://github\.com)?/xkain/ESPSomfy-RTS/wiki/'
# Absolute links (HTML href, and wherever the French used one) need the wiki's own path.
BASE = '/olliemaller/ESPSomfy-RTS/wiki/'


def headings(path):
    out, fence = [], False
    for line in open(path, encoding='utf-8'):
        if line.lstrip().startswith('```'):
            fence = not fence
            continue
        m = None if fence else re.match(r'(#{1,6})\s+(.*?)\s*#*\s*$', line)
        if m:
            out.append((len(m.group(1)), m.group(2)))
    return out


def slug(text):
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text).replace('`', '').replace('*', '')
    return re.sub(r'[^\w\- ]', '', text.lower()).replace(' ', '-')


def slugs(path):
    seen, out = {}, []
    for _, h in headings(path):
        s = slug(h)
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.append(s if n == 0 else f'{s}-{n}')
    return out


def fr_key(name):
    name = NFC(unquote(name)).replace(' ', '-')
    return FR_BY_KEY.get(name.lower())


class Fixer:
    def __init__(self, fr, en_dir, page_key):
        self.fr, self.en_dir, self.page, self.problems = fr, en_dir, page_key, []

    def anchor(self, key, a):
        if not a:
            return ''
        a = NFC(unquote(a)).lower()
        fs = slugs(os.path.join(self.fr, key + '.md'))
        es = slugs(os.path.join(self.en_dir, PAGES[key][0] + '.md'))
        if len(fs) != len(es):
            self.problems.append(f'{PAGES[key][0]}: {len(es)} headings, French has {len(fs)}')
            return ''
        if a not in fs:
            self.problems.append(f'{self.page}: #{a} is not a heading on French page {key}')
            return ''
        return '#' + es[fs.index(a)]

    def target(self, t, absolute=False):
        absolute = absolute or bool(re.match(WIKI, t))
        m = re.fullmatch(f'(?:{WIKI})?([^#?]*)(?:#(.*))?', t)
        if not m or t.startswith(('http', 'mailto:')) and not re.match(WIKI, t):
            return t
        name, a = m.group(1), m.group(2)
        key = self.page if name == '' else fr_key(name)
        if key is None:
            return t
        page = '' if name == '' else (BASE if absolute else '') + PAGES[key][0]
        return page + self.anchor(key, a)

    def wikilink(self, m):
        inner = m.group(1)
        label, name = inner.split('|', 1) if '|' in inner else (None, inner)
        key = fr_key(name.strip())
        if key is None:
            return m.group(0)
        f, title = PAGES[key]
        label = label or title
        return f'[[{label}|{f}]]' if label != f else f'[[{f}]]'

    def run(self, text):
        out, fence = [], False
        for line in text.split('\n'):
            if line.lstrip().startswith('```'):
                fence = not fence
            if not fence:
                line = re.sub(r'\[\[([^\]]+)\]\]', self.wikilink, line)
                line = re.sub(r'\]\(([^()\s]*(?:\([^()\s]*\)[^()\s]*)*)\)', lambda m: '](' + self.target(m.group(1)) + ')', line)
                line = re.sub(r'href="([^"]+)"', lambda m: 'href="' + self.target(m.group(1), True) + '"', line)
            out.append(line)
        return '\n'.join(out)


def en_to_fr(en_file):
    for k, v in PAGES.items():
        if v[0] == en_file:
            return k


def fr_versions(fr):
    out = subprocess.run(['git', '-C', fr, 'ls-files', '-s', '-z', '*.md'], capture_output=True, check=True).stdout
    vers = {}
    for rec in out.decode('utf-8').split('\0'):
        if rec:
            meta, path = rec.split('\t', 1)
            vers[NFC(path[:-3])] = meta.split()[1]
    return vers


def main():
    cmd, fr = sys.argv[1], sys.argv[2]
    if cmd == 'status':
        old = json.load(open(STATE)) if os.path.exists(STATE) else {}
        new = fr_versions(fr)
        for p in sorted(new):
            if p not in PAGES:
                print(f'NEW      {p}  (add it to pages.json)')
            elif old.get(p) != new[p]:
                print(f'CHANGED  {p}  -> {PAGES[p][0]}.md')
        for p in sorted(set(PAGES) - set(new)):
            print(f'DELETED  {p}  -> remove {PAGES[p][0]}.md and its pages.json entry')
    elif cmd == 'fix':
        problems = []
        for f in sys.argv[3:]:
            path = os.path.join(EN, os.path.basename(f))
            fx = Fixer(fr, EN, en_to_fr(os.path.basename(f)[:-3]))
            text = open(path, encoding='utf-8').read()
            new = fx.run(text)
            open(path, 'w', encoding='utf-8').write(new)
            problems += fx.problems
        print('\n'.join(problems) or 'fixed')
        sys.exit(1 if problems else 0)
    elif cmd == 'check':
        bad = []
        names = {n.lower() for n in EN_FILES}
        for key, (f, _) in PAGES.items():
            path = os.path.join(EN, f + '.md')
            if not os.path.exists(path):
                bad.append(f'missing page {f}.md')
                continue
            fh, eh = headings(os.path.join(fr, key + '.md')), headings(path)
            if [l for l, _ in fh] != [l for l, _ in eh]:
                bad.append(f'{f}.md: heading levels differ from French {key}')
            for line in Fixer(fr, EN, key).run(open(path, encoding='utf-8').read()).split('\n'):
                if re.search(WIKI + r'|\]\((?:' + '|'.join(re.escape(k) for k in PAGES if PAGES[k][0] != k) + r')[#)]', line):
                    bad.append(f'{f}.md: still links to a French page: {line.strip()[:100]}')
            text = open(path, encoding='utf-8').read()
            for t in re.findall(r'\]\(([^)\s:]+)\)|href="([^":]+)"', text):
                t = t[0] or t[1]
                page, _, a = t.removeprefix(BASE).partition('#')
                target = page or f
                if target.lower() not in names:
                    continue
                if a and a not in slugs(os.path.join(EN, target + '.md')):
                    bad.append(f'{f}.md: link #{a} not found on {target}')
            for w in re.findall(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]', text):
                if w.replace(' ', '-').lower() not in names:
                    bad.append(f'{f}.md: [[{w}]] is not an English page')
        print('\n'.join(bad) or 'all links OK')
        sys.exit(1 if bad else 0)
    elif cmd == 'done':
        json.dump(fr_versions(fr), open(STATE, 'w'), ensure_ascii=False, indent=1, sort_keys=True)
        print('state saved')


if __name__ == '__main__':
    main()
