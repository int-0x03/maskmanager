import argparse
import sys
import re
import codecs

#  ? | Charset
# ===+=========
#  l | abcdefghijklmnopqrstuvwxyz
#  u | ABCDEFGHIJKLMNOPQRSTUVWXYZ
#  d | 0123456789
#  h | 0123456789abcdef
#  H | 0123456789ABCDEF
#  s |  !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#  a | ?l?u?d?s
#  b | 0x00 - 0xff

MASKS = {
    '?l': len('abcdefghijklmnopqrstuvwxyz'),
    '?u': len('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
    '?d': len('0123456789'),
    '?h': len('0123456789abcdef'),
    '?H': len('0123456789ABCDEF'),
    '?s': len(' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'),
    '?a': 0,                                                                # ?a calculate later :)
    '?b': len(range(0, 256)),
}
MASKS['?a'] = MASKS['?l'] + MASKS['?u'] + MASKS['?d'] + MASKS['?s']         # ?a = ?l?u?d?s

VERBOSE_OUTPUT = False

def calculate_difficult(mask):
    result = 1
    for mask_char, count_chars in MASKS.items():
        count = mask.count(mask_char)
        if count > 0:
            result *= count_chars ** count
    return result

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def list_from_range(ran):
    start_range = int(ran.split('-')[0])
    end_range = int(ran.split('-')[1])+1
    return range(start_range, end_range)

def args_parse():
    global VERBOSE_OUTPUT
    parser = argparse.ArgumentParser(description="Hashcat masks difficulty sorter. Read file from STDIN and print to STDOUT.", \
                                     formatter_class=argparse.RawTextHelpFormatter,                                            \
                                     epilog='Examples:\n\tmaskmanager -f 1,3-6,9 < input.txt > output.txt\n\t'                 \
                                                         'maskmanager * > output.txt\n\t'                                      \
                                                         'maskmanager input.txt input2.txt input3.txt > output.txt')

    parser.add_argument('IN_FILES', nargs='*', type=argparse.FileType('r'),                                                    \
                                    help="Input file(s) for sorting. STDIN will be used by default.",                          \
                                    default=[sys.stdin])
    parser.add_argument("--no-clear-masks", "-nc", help="Remove 1 difficulty masks (no masks) from output. "                   \
                                                        "By default fake masks will be removed.",                              \
                                                   action='store_false',                                                       \
                                                   default=True)
    parser.add_argument("--human-readable", "-hr", help="Resolve $HEX[...] constructions, print as human readable. WARNING: "   \
                                                        "don't pass this output to hashcat, it is not recognize utf-8",        \
                                                  action='store_true')

    parser.add_argument("--filter-len", "-f", help="Filter masks by length, -f min-max or -f len1,len2", type=str)
    parser.add_argument("--verbose", "-v", help="Verbose output to STDERR", action="store_true")

    args = parser.parse_args()
    args_d = vars(args)
    valid_lengths = []
    if args.filter_len:
        if "," in args.filter_len:
            for length in args.filter_len.split(','):
                if "-" in length:
                    valid_lengths += list_from_range(length)
                else:
                    valid_lengths.append(int(length))
        elif "-" in args.filter_len:
            valid_lengths += list_from_range(args.filter_len)
        else:
            valid_lengths.append(int(args.filter_len))
    args_d['valid_lengths'] = valid_lengths
    VERBOSE_OUTPUT = args.verbose
    return args
def mask_len(mask):
    return len(mask.replace('?', ""))


def sort_by_difficult(lines, valid_lengths, no_clear):
    result = []
    for line in lines:
        difficulty = calculate_difficult(line)
        if (not no_clear and difficulty == 1) or (valid_lengths and mask_len(line) not in valid_lengths):
            continue
        result.append({
            "mask": line,
            "difficulty": difficulty
        })
    result.sort(key=lambda x: x["difficulty"])
    return result

def read_lines(fd_list):
    lines = []
    for fd in fd_list:
        lines += fd.read().splitlines()
        fd.close()
    return lines

def resolve_hex_syntax(word):
    result = re.findall(r"\$HEX\[([0-9a-fA-F]+)\]", word)
    if result:
        result = codecs.decode(result[0], "hex").decode('utf-8')
        if VERBOSE_OUTPUT:
            eprint('[i] Word "%s" -> "%s"' %(word, result))
        return result
    else:
        return word

def print_out(masks_dicts, human_readable=False):
    for masks_dict in masks_dicts:
        if human_readable and all(c in masks_dict['mask'] for c in "$HEX[]"):
            masks_dict['mask'] = resolve_hex_syntax(masks_dict['mask'])
        print(masks_dict['mask'])
    if VERBOSE_OUTPUT:
        total_difficulty = 0
        for masks_dict in masks_dicts:
            eprint("[i] Mask '%s', difficulty: %d combinations." %(masks_dict['mask'], masks_dict['difficulty']))
            total_difficulty += masks_dict['difficulty']
        eprint("[i] Masks total count: %d\n    Total difficulty: %d combinations" %(len(masks_dicts), total_difficulty))


def main():
    args = args_parse()
    lines = read_lines(args.IN_FILES)
    lines_dict = sort_by_difficult(lines, args.valid_lengths, args.no_clear_masks)
    print_out(lines_dict, human_readable=args.human_readable)


if __name__ == '__main__':
    main()
