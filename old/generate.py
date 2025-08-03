#!/usr/bin/env python3

import sys

def clean_quote_wrapping(line: str) -> str:
    line = line.strip()
    if (line.startswith('"') and line.endswith('"')) or \
       (line.startswith("'") and line.endswith("'")):
        line = line[1:-1]
    return line.strip()

def read_and_format():
    lines = [clean_quote_wrapping(line) for line in sys.stdin if line.strip()]
    print("ideas = [")
    for line in lines:
        escaped = line.replace('"', r'\"')
        print(f'    "{escaped}",')
    print("]")

if __name__ == "__main__":
    read_and_format()
