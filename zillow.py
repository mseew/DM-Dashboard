import urllib2

def dl_save(url, target):
	response = urllib2.urlopen(url)
	csv = response.read()

	csvstr = str(csv.strip("b'"))

	lines = csvstr.split("\\n")
	f = open(target, 'w')
	for line in lines:
		f.write(line + "\n")
	f.close()

# Save for-sale inventory (states) csv
dl_save("http://files.zillowstatic.com/research/public/State/InventoryMeasure_SSA_State_Public.csv", "forsaleinventoryssa.csv")

# Save median rent per unit (states) csv
dl_save("http://files.zillowstatic.com/research/public/State/State_MedianRentalPrice_AllHomes.csv", "medianrentstates.csv")

