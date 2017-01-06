# py-json2tsv
Create tab-separated documents from a JSON object

This code is written and tested on a Mac. It should work on Linux systems but further testing is required for Windows.

# Parameters
- compulsory
    - '-i', '--input-file': input file name

- optional
    - '``-I``', '``--input-path``' : Input file path (using delimiter /)
    - '``-O``', '``--output-path'``: Output file path (using delimiter /)
    - '``-o``', '``--output-file'``: Output file name
    - '``-k``', '``--main-key'``   : Highest-level key for access the list of records required

# Example Usage
- ```python
python json2tsv.py -i 'test.json' -I '/Users/melaus/repo/personal/py-json2tsv' -o 'test_output.tsv'
```
