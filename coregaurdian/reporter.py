from typing import List, Optional
from .parser import try_extract_addr_from_line


def generate_report(idx: int, section_text: str, stacks: List[List[str]], symbolicator, analyzer):
    lines = []
    lines.append('\n' + '='*80)
    lines.append(f'Crash #{idx+1}')
    header = section_text.splitlines()[0] if section_text.splitlines() else '<no header>'
    lines.append('Header: ' + header)
    symbolicated = []
    for si, stack in enumerate(stacks):
        lines.append(f' Stack #{si+1}:')
        for ln in stack:
            addr = try_extract_addr_from_line(ln)
            sym = None
            if symbolicator and addr:
                sym = symbolicator.symbolicate(addr)
            if not sym:
                sym = ln
            symbolicated.append(sym)
            lines.append('  ' + ln)
            if addr:
                lines.append('    -> addr: ' + addr)
            lines.append('    -> symbol: ' + str(sym))
    analysis = analyzer.analyze(section_text, symbolicated)
    lines.append('\nAnalysis:')
    for s in analysis['suggestions']:
        lines.append(' - ' + s)
    lines.append('='*80 + '\n')
    return '\n'.join(lines)