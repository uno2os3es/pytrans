#!/usr/bin/env python3
import sys
import string


def main():
    fname = sys.argv[1]
    persian_chars = 'چجحخهعفقثصپمنتالبیسشگکودرططغًضَُئِّآءذژظِ۱۲۳۴۵۶۷۸۹۰ز'
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        contents = f.read()
        for char in contents:
            if char not in string.printable:
                if not char in persian_chars:
                    if not ord(char) == 1571:
                        print(f'"{char}" : :{ord(char)}')


if __name__ == '__main__':
    sys.exit(main())
