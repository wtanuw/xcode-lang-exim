# A simple tool for moderating localization from xcode project

### Requirement:
- Python 2.7
- xlsxwriter: http://xlsxwriter.readthedocs.io/
- xlrd: https://pypi.python.org/pypi/xlrd

Run: `cd projectpath`

Run: `python export-text.py`

Then, update lang.xlsx as your demand

Run: `python import-text.py` to import it into project

or

Run: `cd projectpath`

Run: `python export-text.py -o filename`

Then, update value of each key in filename as your demand

Run: `python import-text.py -i filename` to import it into project


### Todo
- support multiline 