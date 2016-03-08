from census import Census
from us import states
import pandas as pd 
import json
import urllib2

apikey = "0d38b8e9fa869342198c6b033f02c2cdffb4b84c"

# Customize start and end year for quarterly data series
year = 2014

# State FIPS values for DC
state = 11

#Create the empty data frame that all of the Series will be merged into
df = pd.DataFrame(index=range(0,1), columns=['State', 'Ward', 'Name', 'Label', 'Value'])

#testing output format
url = "http://api.census.gov/data/{0}/acs5?get=NAME,{1}&for=state+legislative+district+(upper+chamber):*&in=state:{2}&key={3}".format(year, 'B01003_001E', state, apikey)

# Gets data from URL
response = urllib2.urlopen(url)
data = json.loads(response.read())

for x in data:
	print x
	print '\n'

values = [data[1][0], data[0][1], data[1][1]]
print values

#Function for pulling and appending series observations
#def acsgetappend(datapoint, label):
#	url = "http://api.census.gov/data/{0}/acs5?get=NAME,{1}&for=state+legislative+district+(upper+chamber):*&in=state:{2}&key={3}".format(year, datapoint, state, apikey)

	# Gets data from URL
#	response = urllib2.urlopen(url)
#	data = json.loads(response.read())

#	global df 

	#The first series replaces the data frame
#	values = [data[1][0], data[0][1], label, data[1][1]]
#	df=df.append({'State':data[1][0],'Name':data[0][1],'Label':label, 'Value':data[1][1]}, ignore_index=True)


#Get & append all the relevant series.
#acsgetappend("B01003_001E", 'Total Population')
#acsgetappend("B25002_002E", 'Occupied Housing Units')
#acsgetappend("B25003_002E", 'Owner-occupied Units')
#acsgetappend("B25003_003E", 'Renter-occupied units')

#Write to file!
#output = pd.ExcelWriter("ACS-housing-2014-5yr.xlsx", engine='xlsxwriter')
#df.to_excel(output, 'ForTableau')
#output.save()

