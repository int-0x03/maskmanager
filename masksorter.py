#!/usr/bin/python3
import argparse
import sys

"""
  ? | Charset
 ===+=========
  l | abcdefghijklmnopqrstuvwxyz
  u | ABCDEFGHIJKLMNOPQRSTUVWXYZ
  d | 0123456789
  h | 0123456789abcdef
  H | 0123456789ABCDEF
  s |  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
  a | ?l?u?d?s
  b | 0x00 - 0xff
"""
masks = {
    '?l': len('abcdefghijklmnopqrstuvwxyz'),
    '?u': len('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
    '?d': len('0123456789'),
    '?h': len('0123456789abcdef'),
    '?H': len('0123456789ABCDEF'),
    '?s': len(' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
    '?a': 0,                                                    # ?a calculate later :)
    '?b': len(range(0, 256)),
}
masks['?a'] = masks['?l'] + masks['?u'] + masks['?d'] + masks['?s']       # ?a = ?l?u?d?s


def calculate_difficult(mask):
    result = 0
    for mask_char, count_chars in masks.items():
        if mask.count(mask_char) > 0:
            result += count_chars ** mask.count(mask_char)
    return 1 if result == 0 else result


def args_parse():
    parser = argparse.ArgumentParser(description="Hashcat masks difficulty sorter.\nOutput to STDOUT.")
    parser.add_argument("INPUT_FILE", type=argparse.FileType('r'), help="Input file", default=sys.stdin)
    parser.add_argument("--clear-masks", "-c", help="Remove 1 difficulty masks (no masks) from output", action='store_true', default=False)
    return parser.parse_args()


def main():
    args = args_parse()
    lines = args.INPUT_FILE.read().splitlines()
    # print(lines)
    result = []
    for line in lines:
        difficulty=calculate_difficult(line)
        if args.clear_masks and difficulty == 1:
            continue
        result.append({
            "key": line,
            "value": difficulty
        })
    result.sort(key=lambda x: x["value"])
    for masks_dict in result:
        print(masks_dict['key'])


if __name__ == '__main__':
    main()
