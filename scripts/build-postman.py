#!/usr/bin/env python3
"""Generate a Postman v2.1 collection from openapi.yaml. Usage: build-postman.py <docs-repo>"""
import json, os, sys, re, uuid
import yaml
repo = sys.argv[1]
spec = yaml.safe_load(open(os.path.join(repo, 'openapi.yaml'), encoding='utf-8'))

def resolve(node):
    if isinstance(node, dict) and '$ref' in node:
        parts = node['$ref'].lstrip('#/').split('/')
        cur = spec
        for p in parts:
            cur = cur[p]
        return resolve(cur)
    return node

def example_of(schema, depth=0):
    schema = resolve(schema)
    if not isinstance(schema, dict) or depth > 6:
        return None
    if 'example' in schema:
        return schema['example']
    if 'examples' in schema and isinstance(schema['examples'], list) and schema['examples']:
        return schema['examples'][0]
    if 'default' in schema:
        return schema['default']
    if 'enum' in schema:
        return schema['enum'][0]
    for key in ('oneOf', 'anyOf', 'allOf'):
        if key in schema:
            merged = {}
            for sub in schema[key]:
                v = example_of(sub, depth + 1)
                if isinstance(v, dict):
                    merged.update(v)
                elif v is not None and key != 'allOf':
                    return v
            return merged or None
    t = schema.get('type')
    if t == 'object' or 'properties' in schema:
        return {k: example_of(v, depth + 1) for k, v in (schema.get('properties') or {}).items()}
    if t == 'array':
        v = example_of(schema.get('items', {}), depth + 1)
        return [v] if v is not None else []
    if t == 'string':
        f = schema.get('format')
        return {'date-time': '2026-09-15T10:00:00Z', 'uuid': '00000000-0000-0000-0000-000000000000', 'uri': 'https://example.com'}.get(f, 'string')
    if t == 'integer':
        return 1
    if t == 'number':
        return 1.0
    if t == 'boolean':
        return True
    return None

def body_example(op):
    rb = resolve(op.get('requestBody') or {})
    content = (rb.get('content') or {}).get('application/json') or {}
    if 'example' in content:
        return content['example']
    exs = content.get('examples') or {}
    if exs:
        first = resolve(next(iter(exs.values())))
        if 'value' in first:
            return first['value']
    if 'schema' in content:
        return example_of(content['schema'])
    return None

def response_examples(op):
    out = []
    for code, resp in (op.get('responses') or {}).items():
        resp = resolve(resp)
        content = (resp.get('content') or {}).get('application/json') or {}
        val = None
        if 'example' in content:
            val = content['example']
        elif content.get('examples'):
            first = resolve(next(iter(content['examples'].values())))
            val = first.get('value')
        elif 'schema' in content and str(code).startswith('2'):
            val = example_of(content['schema'])
        if val is None:
            continue
        out.append({'name': f"{code} {resp.get('description', '')}".strip(), 'code': int(code) if str(code).isdigit() else 200,
                    'status': resp.get('description', ''), 'header': [{'key': 'Content-Type', 'value': 'application/json'}],
                    'body': json.dumps(val, indent=2), '_postman_previewlanguage': 'json'})
    return out

server = (spec.get('servers') or [{}])[0].get('url', 'https://api.watx.in/v1')
tags_order = [t['name'] for t in spec.get('tags', [])]
folders = {}
for path, methods in spec['paths'].items():
    for method, op in methods.items():
        if method.lower() not in ('get', 'post', 'put', 'patch', 'delete'):
            continue
        tag = (op.get('tags') or ['Other'])[0]
        folders.setdefault(tag, [])
        pm_path = re.sub(r'\{(\w+)\}', r':\1', path)
        segments = [s for s in pm_path.split('/') if s]
        query = []
        variables = []
        for prm in op.get('parameters', []) + methods.get('parameters', []):
            prm = resolve(prm)
            ex = prm.get('example')
            if ex is None and 'schema' in prm:
                ex = example_of(prm['schema'])
            if prm.get('in') == 'query':
                query.append({'key': prm['name'], 'value': '' if ex is None else str(ex), 'description': prm.get('description', ''), 'disabled': not prm.get('required', False)})
            elif prm.get('in') == 'path':
                variables.append({'key': prm['name'], 'value': '' if ex is None else str(ex), 'description': prm.get('description', '')})
        req = {
            'method': method.upper(),
            'header': [{'key': 'Accept', 'value': 'application/json'}],
            'url': {'raw': '{{baseUrl}}' + pm_path, 'host': ['{{baseUrl}}'], 'path': segments, 'query': query, 'variable': variables},
            'description': (op.get('description') or '') + (f"\n\nRequired scope: `{op['x-required-scope']}`" if op.get('x-required-scope') else ''),
        }
        body = body_example(op)
        if body is not None and method.lower() in ('post', 'put', 'patch'):
            req['header'].append({'key': 'Content-Type', 'value': 'application/json'})
            req['body'] = {'mode': 'raw', 'raw': json.dumps(body, indent=2), 'options': {'raw': {'language': 'json'}}}
        item = {'name': op.get('summary') or f"{method.upper()} {path}", 'request': req, 'response': []}
        for ex in response_examples(op):
            ex['originalRequest'] = {'method': req['method'], 'header': req['header'], 'url': req['url']}
            item['response'].append(ex)
        folders[tag].append(item)

ordered = [t for t in tags_order if t in folders] + [t for t in folders if t not in tags_order]
collection = {
    'info': {
        '_postman_id': str(uuid.uuid5(uuid.NAMESPACE_URL, 'https://api.watx.in/v1/postman')),
        'name': 'Watx API',
        'description': 'Public REST API for Watx (https://app.watx.in). Set `apiKey` to a key from Settings → API keys; `baseUrl` defaults to the production API. Generated from the OpenAPI document published with the docs.',
        'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
    },
    'auth': {'type': 'bearer', 'bearer': [{'key': 'token', 'value': '{{apiKey}}', 'type': 'string'}]},
    'variable': [
        {'key': 'baseUrl', 'value': server, 'type': 'string'},
        {'key': 'apiKey', 'value': '', 'type': 'string', 'description': 'Create one in Settings → API keys'},
    ],
    'item': [{'name': t, 'description': next((x.get('description', '') for x in spec.get('tags', []) if x['name'] == t), ''), 'item': folders[t]} for t in ordered],
}
out = os.path.join(repo, 'postman', 'watx-api.postman_collection.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(collection, open(out, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
n = sum(len(folders[t]) for t in folders)
print(f'wrote {out}: {len(ordered)} folders, {n} requests')
