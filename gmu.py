import requests
import xlsxwriter
import xlrd
from datetime import datetime
from pandas import date_range

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
workbook = xlsxwriter.Workbook('MonthlySales_DC.xlsx')
ForTableau = workbook.add_worksheet('ForTableau')

date_format = workbook.add_format({'num_format': 'm/d/yyyy'})

# Write the column headers
ForTableau.write('A1', 'Date')
ForTableau.write('B1', 'Sales')

# We want to start at 01/01/2009
start_date = '01/31/2009'

# Convert to datetime object
start_datetime = datetime.strptime(start_date, "%m/%d/%Y")

# Create list of dates
dates = date_range(start_date, periods=date_len, freq='M')

#Loop write the list of dates in the first row. 
row = 1

for date in dates:
	ForTableau.write(row, 0, date)
	row += 1

# Loop write the list of values in column 2
val_row = 1
for value in value_list:
	ForTableau.write(val_row, 1, value)
	val_row += 1

workbook.close()






