import requests
import urllib2
import pandas as pd 
import xlsxwriter

#Define the file name to save. 
filename = 'Housing-Units-Auth_State'

datalist=[]

# Need to make a for loop over all the text files I want on the census' website...
for x in range(10,17):
	for y in range(1,13):
		url = 'http://www2.census.gov/econ/bps/State/st'+str(x)+str(y).zfill(2)+'c.txt'
		#print url
		#Read the text at that url
		
		try:
			text = urllib2.urlopen(url)
		
		except urllib2.URLError, e:
			print(str(x)+str(y).zfill(2)+"not available yet")
			continue

		#Census neglected to put a comma at the end of the last line, which throws off the number of columns. This code adds a comma. #ThanksObama
		lines = text.readlines()
		lines[0] = lines[0][:-2]
		lineedit = lines[0] + ",\n"
		lines[0]=lineedit

		#Make the text data a list of lists
		raw = []
		for line in lines:
			points = line.split(",")
			row = []
			for point in points:
				row.append(point)
			raw.append(row)

		for row in raw[3:]:
			datalist.append(row)

#Define column names in a list. Original data has col names in 2 rows ugh
colnames = ["Date", "State Fips", "Region", "Division", "State", "1-unit Bldgs", "1-unit Units", "1-unit Value", "2-unit Bldgs", "2-unit Units", "2-unit Value", "3-4-unit Bldgs", "3-4-unit Units", "3-4-unit Value", "5+-unit Bldgs", "5+-unit Units", "5+-unit Value","1-unit rep Bldgs", "1-unit rep Units", "1-unit rep Value", "2-unit rep Bldgs", "2-unit rep Units", "2-unit rep Value", "3-4-unit rep Bldgs", "3-4-unit rep Units", "3-4-unit rep Value", "5+-unit rep Bldgs", "5+-unit rep Units", "5+-unit rep Value"]

#Read the list of lists into a data frame
data = pd.DataFrame(datalist, columns=colnames)

		#Drop those two column label rows plus a random blank row Census left in there #ugh
		#data = data.drop(data.index[[0,1,2]])
		#datax = pd.concat([data0, data], axis=2)

#Keep only the columns we care about (i.e. not rehab data)
data2 = data[["Date", "State", "1-unit Units", "2-unit Units", "3-4-unit Units", "5+-unit Units"]]

data3 = pd.melt(data2, id_vars=["Date", "State"], value_vars=["1-unit Units", "2-unit Units", "3-4-unit Units","5+-unit Units"])

units = data3['variable'].apply(lambda x:pd.Series(x.split(" ")))
units.columns = ["units", 'valtype']

data4 = pd.concat([data3, units], axis=1)
data4 = data4.drop('variable', 1)
#print data4

output = pd.ExcelWriter(filename+".xlsx", engine='xlsxwriter')
data4.to_excel(output, 'ForTableau')
output.save()



