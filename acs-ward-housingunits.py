from census import Census
from us import states
import pandas as pd 
import json
import urllib2
import xlsxwriter

apikey = "0d38b8e9fa869342198c6b033f02c2cdffb4b84c"

# Customize start and end year for quarterly data series
year = 2014

# State FIPS values for DC
state = 11

df = pd.DataFrame(columns=['Description', 'Value', 'DCCode', 'Ward', 'Year', 'Series'])

def acsgetmerge(seriesid, seriesname):
	url = "http://api.census.gov/data/{0}/acs5?get=NAME,{1}&for=state+legislative+district+(upper+chamber):*&in=state:{2}&key={3}".format(year, seriesid, state, apikey)

	response = urllib2.urlopen(url)
	data = json.loads(response.read())

	for row in data:
		row.append(year)
		row.append(seriesname)

	global df

	loopdf = pd.DataFrame(data[1:9], columns=['Description', 'Value', 'DCCode', 'Ward', 'Year', 'Series'])

	df = df.append(loopdf)

acsgetmerge('B25024_002E', '1 unit, detached')
acsgetmerge('B25024_003E', '1 unit, attached')
acsgetmerge('B25024_004E', '2 unit')
acsgetmerge('B25024_005E', '3-4 unit')
acsgetmerge('B25024_006E', '5-9 unit')
acsgetmerge('B25024_007E', '10-19 unit')
acsgetmerge('B25024_008E', '20-49 unit')
acsgetmerge('B25024_009E', '50-plus unit')
acsgetmerge('B25024_010E', 'Mobile home')
acsgetmerge('B25024_011E', 'RV/boat/van')
acsgetmerge('B25002_002E', 'Total Occupied')

output = pd.ExcelWriter("ACS-ward-housingunits.xlsx", engine='xlsxwriter')
df.to_excel(output, 'ForTableau')
output.save()
