import requests
import xlsxwriter
import xlrd
from datetime import datetime

# Define funtion for pulling in GMU excel file.
def dl_xls(url, target):
	dls = url

	resp = requests.get(dls)
	with open(target, 'wb') as output:
		output.write(resp.content)

# Run function to import file
dl_xls("http://cra.gmu.edu/pdfs/data/MonthlySales_DC.xls", 'MonthlySales_DC-raw.xls')

# Read the file
book = xlrd.open_workbook('MonthlySales_DC-raw.xls')

# The sheet with the data is called DC
DC = book.sheet_by_index(0)

# Define a list to hold the values
value_list = DC.col_values(2,4,)

# This is the length of the list of values
date_len = len(value_list)
print date_len

# Create a new workbook with sheet for Tableau
workbook = xlsxwriter.Workbook('MonthlySales_DC.xls')
ForTableau = workbook.add_worksheet('ForTableau')

date_format = workbook.add_format({'num_format': 'mm/dd/yyyy'})

# Write the column headers
ForTableau.write('A1', 'Date')
ForTableau.write('B1', 'Sales')

# We want to start at 01/01/2009
start_date = 39814.00

# Write the start date
ForTableau.write('A2', start_date, date_format)

# Loop write the rest of the rows with a +1 month formula (EDATE)
for row in range(2, date_len):
	ForTableau.write(row, 0, "=EDATE(A"+str(row)+", 1)", date_format)

# Loop write the list of values in column 2
val_row = 1
for value in value_list:
	ForTableau.write(val_row, 1, value)
	val_row += 1

workbook.close()







