#!/usr/bin/env python3
"""Lint Mintlify pages: frontmatter, no body H1, no images, internal links resolve, no internal leakage."""
import os, re, sys, json
repo = sys.argv[1]
pages = []
for root, dirs, files in os.walk(repo):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', 'images', 'logo', 'drafts')]
    for f in files:
        if f.endswith('.mdx'):
            pages.append(os.path.relpath(os.path.join(root, f), repo))
pages.sort()
slugs = {p[:-4] for p in pages}
problems = []
leak = re.compile(r'apps/(api|web|admin-panel)/|CLAUDE\.md|supabase/migrations|migration \d{3}|\bPrisma\b|\bRLS\b|⚠️')
for p in pages:
    text = open(os.path.join(repo, p), encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        problems.append((p, 'no frontmatter')); continue
    fm = m.group(1)
    for key in ('title', 'description'):
        if not re.search(rf'^{key}:\s*\S', fm, re.M):
            problems.append((p, f'frontmatter missing {key}'))
    body = text[m.end():]
    prose = re.sub(r'```.*?```', '', body, flags=re.S)  # ignore fenced code
    if re.search(r'^# ', prose, re.M):
        problems.append((p, 'H1 in body'))
    if re.search(r'!\[|<img\b|<Frame\b', body):
        problems.append((p, 'image or Frame reference'))
    for lm in leak.finditer(prose):
        problems.append((p, f'internal leak: "{lm.group(0)}"')); break
    for link in re.findall(r'\]\((/[^)\s#]*)(?:#[^)]*)?\)|href="(/[^"#]*)', body):
        href = link[0] or link[1]
        if not href or href.startswith('//'):
            continue
        target = href.strip('/')
        if target == '':
            target = 'index'
        if target not in slugs and not os.path.exists(os.path.join(repo, target)):
            problems.append((p, f'broken link {href}'))
print(f'{len(pages)} pages, {len(problems)} problems')
for p, why in problems:
    print(f'  {p}: {why}')
sys.exit(1 if problems else 0)
