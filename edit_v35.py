"""
v35 — Remove all Vivosun PENDING markers. Data not available = not in the table.
"""

import re, subprocess

SRC = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v34.md'
OUT_MD = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v35.md'
OUT_DOCX = r'C:\repos\eDNA-20270420\output\MBTS_eDNA_Report_v35.docx'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove all 5 Vivosun PENDING markers (with trailing newline)
text = re.sub(
    r'<!-- PENDING: Add Vivosun field pH/temp measurements for [^>]+ -->\n\n',
    '\n',
    text
)
# Also catch any without double newline
text = re.sub(
    r'<!-- PENDING: Add Vivosun field pH/temp measurements for [^>]+ -->\n',
    '',
    text
)

with open(OUT_MD, 'w', encoding='utf-8') as f:
    f.write(text)

n_lines = text.count('\n')
n_words = len(text.split())
print(f'Written: {OUT_MD}  ({n_lines} lines, {n_words} words)')

result = subprocess.run(
    ['pandoc', OUT_MD, '-o', OUT_DOCX, '--from', 'markdown', '--to', 'docx'],
    capture_output=True, text=True
)
if result.returncode == 0:
    import os
    size = os.path.getsize(OUT_DOCX)
    print(f'Written: {OUT_DOCX}  ({size//1024}KB)')
else:
    print(f'pandoc error: {result.stderr}')
