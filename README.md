# Mask Sorter

Python3 script for sorting and/or filtering hashcat's masks for bruteforce.

## Installation

You can use script directly or install it to system:

```bash
sudo ./install.sh
```
After installation you can run:

```bash
masksorter -f 1,3-6,9 < input.txt > output.txt
```
## Usage

```bash
usage: masksorter.py [-h] [--no-clear-masks] [--filter-len FILTER_LEN]

Hashcat masks difficulty sorter. Read file from STDIN and print to STDOUT.

optional arguments:
  -h, --help            show this help message and exit
  --no-clear-masks, -nc
                        Remove 1 difficulty masks (no masks) from output. By
                        default fake masks be removed.
  --filter-len FILTER_LEN, -f FILTER_LEN
                        Filter masks by length, -f min-max or -f len1,len2

Example: masksorter -f 1,3-6,9 < input.txt > output.txt
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
