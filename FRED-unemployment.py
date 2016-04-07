import ConfigParser
import pandas as pd 
import xlsxwriter
from fredapi import Fred

#API Key stored locally in config file
parser = ConfigParser.ConfigParser()
#Change the .ini file to where your API key is stored
parser.read("C:\\apikeys.ini")
#APIkeys is section header, FRED is variable.
#See https://roboticape.wordpress.com/2014/01/03/hiding-secrets-from-github-or-using-configparser/ for method
key = parser.get('APIkeys', 'FRED')

#My personal FRED API key
fred = Fred(api_key=key)

#Create the empty data frame that all of the FRED Series will be merged into
df = pd.DataFrame()

#Function for pulling and appending FRED series observations
def fredgetappend(dataseries, startdate, seriesname):
	data = fred.get_series(dataseries, observation_start=startdate)
	global df 

	#The first series replaces the data frame
	if df.empty:
		df = pd.DataFrame(data/100)
		df.reset_index(level=0, inplace=True)
		df.columns = ['Date', seriesname]

	#All subsequent series instead merge into the data frame
	else:
		frame = pd.DataFrame(data/100)
		frame.reset_index(level=0, inplace=True)
		frame.columns = ['Date', seriesname]
		df = pd.merge(df, frame, on='Date', how='outer')

#Set the start date. Note the merge is an outer join so there could be multiple different ones.
startdate = '2010-01-01'

#Get & append all the relevant series for unemployment.
fredgetappend('DCDIST5URN', startdate, 'DC (NSA)')
fredgetappend('DCUR', startdate, 'DC (SA)')
fredgetappend('WASH911URN', startdate, 'DC Metro (NSA)')
fredgetappend('UNRATENSA', startdate, 'US (NSA)')
fredgetappend('UNRATE', startdate, 'US (SA)')

#Write to file.
output = pd.ExcelWriter("DC-MSA-Natl unemployment rates 2013-present.xlsx", engine='xlsxwriter')
df.to_excel(output, 'ForTableau')
output.save()





