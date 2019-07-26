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

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def list_from_range(ran):
    startR = int(ran.split('-')[0])
    endR = int(ran.split('-')[1])+1
    return list(range(startR, endR))

def args_parse():
    parser = argparse.ArgumentParser(description="Hashcat masks difficulty sorter. Read file from STDIN and print to STDOUT.", epilog='Example: masksorter -f 1,3-6,9 < input.txt > output.txt')
    parser.add_argument("--no-clear-masks", "-nc", help="Remove 1 difficulty masks (no masks) from output. By default fake masks be removed.", action='store_false', default=True)
    parser.add_argument("--filter-len", "-f", help="Filter masks by length, -f min-max or -f len1,len2", type=str)
    parser.add_argument("--verbose", "-v", help="Verbose output to STDERR", action="store_true")
    args = parser.parse_args()
    args_d = vars(args)
    valid_lenghts = []
    if args.filter_len:
        if "," in args.filter_len:
            for length in args.filter_len.split(','):
                if "-" in length:
                    valid_lenghts += list_from_range(length)
                else:
                    valid_lenghts.append(int(length))
        elif "-" in args.filter_len:
            valid_lenghts += list_from_range(args.filter_len)
        else:
            valid_lenghts.append(int(args.filter_len))
    args_d['valid_lenghts'] = valid_lenghts
    #eprint(valid_lenghts)
    return args
def mask_len(mask):
    #eprint("mask %s, len: %d" %(mask, len(mask.replace('?', ""))))
    return len(mask.replace('?', ""))

def main():
    args = args_parse()
    lines = sys.stdin.read().splitlines()
    # print(lines)
    result = []
    total_difficulty = 0
    for line in lines:
        difficulty=calculate_difficult(line)
        if (not args.no_clear_masks and difficulty == 1) or (args.valid_lenghts and mask_len(line) not in args.valid_lenghts):
            continue
        if args.verbose:
            total_difficulty+=difficulty
            eprint("[i] Mask '%s', difficulty: %d combinations." %(line, difficulty))
        result.append({
            "key": line,
            "value": difficulty
        })
    result.sort(key=lambda x: x["value"])
    for masks_dict in result:
        print(masks_dict['key'])
    if args.verbose:
            eprint("[i] Masks total count: %d\n    Total difficulty: %d combinations" %(len(result), total_difficulty))


if __name__ == '__main__':
    main()
