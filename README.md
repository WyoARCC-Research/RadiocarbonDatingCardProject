# RadiocarbonDatingCardProject

This collection of scripts is meant to take old radiocarbon dating cards dated from 1959-1972 and collect the data off of them using OCR, then organize that data into a spreadsheet so it could be uploaded to the CARD database, which can be found here https://www.canadianarchaeology.ca/

All of these were written in python.

List of packages used:
- pdfminer.six
  - used as OCR for the card PDFS*
- openPyXl
  - used to translate data from text files to an excel spreadsheet
  
The order these scripts ran in goes as follows
1) multicard_read.py
2) organize_text.py
3) compareOldNewOutput.py
4) translate_to_spreadsheet.py
5) check_spreadsheet.py

