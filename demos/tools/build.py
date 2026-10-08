"""One-command build for the playable demo.

    python3 demos/tools/build.py

1. bundle.py crops the room/plaza art, builds scene backgrounds and packs every
   sprite sheet, palette and credit line into build/assets.json.
2. The JSON is injected into game.template.html, producing demos/study-cafe-demo.html,
   a single self-contained file you can open in any browser.
"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(HERE, 'bundle.py')], check=True)
tpl = open(os.path.join(HERE, 'game.template.html'), encoding='utf-8').read()
data = open(os.path.join(HERE, 'build', 'assets.json'), encoding='utf-8').read()
assert '</script' not in data
page = tpl.replace('/*ASSETS*/', data, 1)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       '<style>html,body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n' + page + '\n</body>\n</html>\n')
out = os.path.join(HERE, '..', 'study-cafe-demo.html')
open(out, 'w', encoding='utf-8').write(doc)
print('wrote', os.path.normpath(out), len(doc) // 1024, 'KB')
