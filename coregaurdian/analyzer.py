import re
from typing import List, Tuple, Optional

OOPS_RE = re.compile(r'(?i)\boops\b|\bpanic\b|\bBUG:\b|\bWARNING:\b')
CALL_TRACE_START_RE = re.compile(r'Call Trace:')
STACKLINE_RE = re.compile(r'\[<(?P<addr>[0-9a-fA-F]+)>\]\s+(?P<sym>.*)')
STACKLINE_ADDR_ONLY_RE = re.compile(r'(?P<addr>0x[0-9a-fA-F]+)')
FUNC_WITH_OFFSET_RE = re.compile(r'(?P<func>[^\s+]+)\+0x(?P<off>[0-9a-fA-F]+)')


def read_input(path: Optional[str]) -> str:
    import sys
    if not path or path == '-':
        return sys.stdin.read()
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def find_crashes(text: str) -> List[Tuple[int,int,str]]:
    lines = text.splitlines()
    results = []
    i = 0
    n = len(lines)
    while i < n:
        if OOPS_RE.search(lines[i]):
            start = i
            j = i+1
            while j < n and not OOPS_RE.search(lines[j]):
                j += 1
            results.append((start, j, '\n'.join(lines[start:j])))
            i = j
        else:
            i += 1
    return results


def extract_call_traces(section_text: str) -> List[List[str]]:
    lines = section_text.splitlines()
    stacks = []
    collecting = False
    current = []
    for ln in lines:
        if CALL_TRACE_START_RE.search(ln):
            collecting = True
            current = []
            continue
        if collecting:
            if ln.strip() == '' or re.search(r'Kernel panic|panic - not syncing', ln, re.I):
                if current:
                    stacks.append(current)
                collecting = False
                current = []
                continue
            if STACKLINE_RE.search(ln) or STACKLINE_ADDR_ONLY_RE.search(ln) or FUNC_WITH_OFFSET_RE.search(ln):
                current.append(ln.strip())
            else:
                if '+' in ln or '/' in ln:
                    current.append(ln.strip())
    if collecting and current:
        stacks.append(current)
    return stacks


def try_extract_addr_from_line(line: str) -> Optional[str]:
    m = STACKLINE_RE.search(line)
    if m:
        return '0x' + m.group('addr')
    m2 = STACKLINE_ADDR_ONLY_RE.search(line)
    if m2:
        return m2.group('addr')
    hexm = re.search(r'(0x[0-9a-fA-F]{6,16}|[0-9a-fA-F]{8,16})', line)
    if hexm:
        return hexm.group(1)
    return None