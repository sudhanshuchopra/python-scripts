import os
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import sys
def cssandhtmlimages(url):
	domain = url.split('//')[-1].split('/')[0]
	os.makedirs(domain)
	k=requests.get(url)
	soup=BeautifulSoup(k.text)
	styletags=soup.find_all('style')
	image_urls=set()
	for item in styletags:
		v=re.findall(r'url\(([^)]+)\)',item.string)
		for item2 in v:
			if(item2[0]=="'"):
				item3=item2.split("'")[1]
			elif(item2[0]=='\"'):
				item3=item2.split('"')[1]
			else:
				item3=item2
			image_urls.add(urljoin(url,item3).split("\\")[0])
	links=soup.find_all('link')
	linktags=set()
	for item4 in links:
		linktags.add(item4['href'])
	for item5 in linktags:
		item6=requests.get(urljoin(url,item5))
		v2=re.findall(r'url\(([^)]+)\)',item6.text)
		for item7 in v2:
			if(item7[0]=="'"):
				item8=item7.split("'")[1]
			elif(item7[0]=='"')	:
				item8=item7.split('"')[1]
			else:
				item8=item7
			item9=urljoin(item5,item8)
			image_urls.add(urljoin(url,item9).split("\\")[0])
	i=0
	for item0 in image_urls:
		try:
			pe=requests.get(item0)	
		except:
			continue
		i=i+1
		filename = str(i) + "." + item0.split('.')[-1]
		f = open(domain+'/'+filename, 'wb')
		f.write(pe.content)	
		f.close()
if(__name__=='__main__'):
	if len(sys.argv) < 2:
		print("Enter a website url to fetch images")
		url=input(url)
		cssandhtmlimages(url)
	else:
		cssandhtmlimages(sys.argv[1])				


				

