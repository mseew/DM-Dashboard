from census import Census
from us import states
import pandas as pd 
import urllib2
import json
import ConfigParser

#API Key stored locally in config file
parser = ConfigParser.ConfigParser()
#Change the .ini file to where your API key is stored
parser.read("C:\\apikeys.ini")
#APIkeys is section header, CENSUS is variable.
#See https://roboticape.wordpress.com/2014/01/03/hiding-secrets-from-github-or-using-configparser/ for method
apikey = parser.get('APIkeys', 'CENSUS')

# Customize start and end year for quarterly data series
year = 2014

# State FIPS values for DC
state = 11

#Create the empty data frame that all of the Series will be merged into
df = pd.DataFrame(index=range(0,1), columns=['State', 'Name', 'Label', 'Value'])

#Function for pulling and appending series observations
def acsgetappend(datapoint, label):
	url = "http://api.census.gov/data/{0}/acs5?get=NAME,{1}&for=state:{2}&key={3}".format(year, datapoint, state, apikey)

	# Gets data from URL
	response = urllib2.urlopen(url)
	data = json.loads(response.read())

	global df 

	#The first series replaces the data frame
	values = [data[1][0], data[0][1], label, data[1][1]]
	df=df.append({'State':data[1][0],'Name':data[0][1],'Label':label, 'Value':data[1][1]}, ignore_index=True)

#Get & append all the relevant series.
acsgetappend("B25002_002E", 'Occupied Housing Units')
acsgetappend("B25003_002E", 'Owner-occupied Units')
acsgetappend("B25003_003E", 'Renter-occupied units')

#Write to file!
output = pd.ExcelWriter("ACS-housing-2014-5yr.xlsx", engine='xlsxwriter')
df.to_excel(output, 'ForTableau')
output.save()


