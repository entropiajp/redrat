# redrat
Wrapper script for Drat to recover an entire directory.  
(prefix `re` comes from "recursive")

## Requirement
- Intel Mac
- Python 3

## Preparation
- Download binary of Drat v0.1.3 from https://github.com/jivanpal/drat/releases
- Place binary file in same directory as main.py and rename it to `drat`
- `pip install tqdm`

## Usage
`sudo python main.py <container> <volume ID> <path in volume>`

Example: `sudo python3 main.py /dev/disk2s2 0 "/xxx"`

## Author
[Kenichi Koyama](https://twitter.com/entropiajp)
