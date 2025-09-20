#!/usr/bin/env python3
import argparse
from .parser import read_input, find_crashes, extract_call_traces
from .symbolicate import Addr2Line
from .reporter import generate_report
from .analyzer import Analyzer


def main():
    parser = argparse.ArgumentParser(prog="crashfixer", description="CrashFixer - analyze Linux kernel crashes")
    parser.add_argument('--log', '-l', default='-', help="Path to kernel log or '-' for stdin")
    parser.add_argument('--vmlinux', '-v', default=None, help='Path to vmlinux with debug info')
    parser.add_argument('--raw-only', action='store_true', help='Do not attempt symbolication')
    parser.add_argument('--output', '-o', default=None, help='Write report to file')
    args = parser.parse_args()

    text = read_input(args.log)
    sections = find_crashes(text)
    if not sections:
        print('No crash sections found. Try providing full dmesg output.')
        return

    sym = None
    if args.vmlinux and not args.raw_only:
        sym = Addr2Line(args.vmlinux)

    analyzer = Analyzer()

    for idx, (_, _, block) in enumerate(sections):
        stacks = extract_call_traces(block)
        report = generate_report(idx, block, stacks, sym, analyzer)
        if args.output:
            with open(args.output, 'a', encoding='utf-8') as f:
                f.write(report + '\n')
        else:
            print(report)


if __name__ == '__main__':
    main()