# RadiocarbonDatingCardProject

This collection of scripts is meant to take old radiocarbon dating cards dated from 1959-1972 and collect the data off of them using OCR, then organize that data into a spreadsheet so it could be uploaded to the CARD database, which can be found here https://www.canadianarchaeology.ca/

All of these were written in python.

Further explanation of certain aspects of the project can be found in this link https://arcc-collab.atlassian.net/l/cp/Sm4uaXbf

List of packages used:
- pdfminer.six
  - used as OCR for the card PDFS*
- openPyXl
  - used to translate data from text files to an excel spreadsheet
- pyTesseract
  - used as OCR for extra scripts, such as getLocation.py
  
\* The PDFs of the cards already had OCR run on them via ABBYY. This package conveniently "copy and pasted" the text from that OCR into a text file, with all of the items conveniently separated into their own lines.
  
The order these scripts ran in goes as follows
1) multicard_read.py
2) organize_text.py
3) compareOldNewOutput.py
4) compareLocations.py
5) translate_to_spreadsheet.py
6) check_spreadsheet.py
