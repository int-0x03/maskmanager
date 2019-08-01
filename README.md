# Mask manager

Python3 script for sorting, generating, converting and/or filtering hashcat's masks for bruteforce.

## Installation

You can use script directly or install it to system:

```bash
sudo ./install.sh
```
After installation you can run these examples:

```bash
maskmanager -f 1,3-6,9 < input.txt > output.txt
maskmanager input*.txt > output.txt
maskmanager input.txt input2.txt input3.txt > output.txt
```
## Usage

```usage: maskmanager.py [-h] [--no-clear-masks] [--filter-len FILTER_LEN]
                      [--verbose]
                      [IN_FILES [IN_FILES ...]]

Hashcat masks difficulty sorter. Read file from STDIN and print to STDOUT.

positional arguments:
  IN_FILES              Input file(s) for sorting. STDIN will be used by default.

optional arguments:
  -h, --help            show this help message and exit
  --no-clear-masks, -nc
                        Remove 1 difficulty masks (no masks) from output. By default fake masks will be removed.
  --filter-len FILTER_LEN, -f FILTER_LEN
                        Filter masks by length, -f min-max or -f len1,len2
  --verbose, -v         Verbose output to STDERR

Examples:
    maskmanager -f 1,3-6,9 < input.txt > output.txt
    maskmanager * > output.txt
    maskmanager input.txt input2.txt input3.txt > output.txt```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
