import requests

def dl_xls(url, target):
	dls = url

	resp = requests.get(dls)
	with open(target, 'wb') as output:
		output.write(resp.content)

dl_xls("http://cra.gmu.edu/pdfs/data/MonthlySales_DC.xls", 'monthlyhomesales_dc.xlsx')
