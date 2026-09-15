#!/usr/bin/env python3
"""Build docs.json navigation from DOCS_PLAN.md §4 tables.

Usage: build-nav.py <docs-repo> [--write] [--api-ops ops.txt]
Prints missing page files; with --write, rewrites docs.json keeping site config.
"""
import json, os, re, sys
repo = sys.argv[1]
write = '--write' in sys.argv
ops_file = None
if '--api-ops' in sys.argv:
    ops_file = sys.argv[sys.argv.index('--api-ops') + 1]
plan = open(os.path.join(repo, 'DOCS_PLAN.md'), encoding='utf-8').read()

# Split §4 into tab sections.
sec = plan.split('## 4. Information architecture', 1)[1].split('## 5.', 1)[0]
tabs = re.split(r'\n### Tab: ', sec)[1:]
nav_tabs = []
missing = []
for block in tabs:
    name, body = block.split('\n', 1)
    name = name.strip()
    groups = {}
    order = []
    for line in body.splitlines():
        if not line.startswith('|') or line.startswith('| Group') or line.startswith('| ---'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 3:
            continue
        group, slug = cells[0], cells[1].strip('`')
        if slug == 'openapi.yaml':
            continue
        if group not in groups:
            groups[group] = []
            order.append(group)
        groups[group].append(slug)
        if not os.path.exists(os.path.join(repo, slug + '.mdx')):
            missing.append(slug)
    tab = {'tab': name, 'groups': [{'group': g, 'pages': groups[g]} for g in order]}
    if name == 'API reference':
        tab['openapi'] = 'openapi.yaml'
        if ops_file and os.path.exists(ops_file):
            ops = [l.strip() for l in open(ops_file) if l.strip()]
            # Lines like "## Contacts" start a group; others are "GET /v1/contacts".
            cur = None
            for l in ops:
                if l.startswith('## '):
                    cur = {'group': l[3:].strip(), 'pages': []}
                    tab['groups'].append(cur)
                elif cur is not None:
                    cur['pages'].append(l)
    nav_tabs.append(tab)

print('missing pages:', len(missing))
for m in missing:
    print('  -', m)

if write:
    cfg_path = os.path.join(repo, 'docs.json')
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    glob = cfg.get('navigation', {}).get('global')
    cfg['navigation'] = {'tabs': nav_tabs}
    if glob:
        cfg['navigation']['global'] = glob
    json.dump(cfg, open(cfg_path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    open(cfg_path, 'a').write('\n')
    print('docs.json written')
