import requests
import csv
from bs4 import BeautifulSoup
m=[]
visited=[]
dicti={}
number=0
def extract():
	soup=BeautifulSoup(k.text)
	number=0
#print(soup)
	t=soup.find_all("div",{"class":"title"})
#print(t)
	for i in t:
		if(i.a==None):
			continue
		if(i.a['href']==None):
			continue
		m.append(i.a['href'])
	for el in m:
		if(el in visited):
			continue
		link="http://www.imdb.com"	+el
		visited.append(el)
		next=requests.get(link)
		soup=BeautifulSoup(next.text)
		v=soup.find_all("div",{"class":"rec_item"})
		for item in v:
			if(item.a!=None):
				if(item.a['href']!=None):
					m.append(item.a['href'])
		rating=soup.find("span",{"itemprop":"ratingValue"})
		if(rating==None):
			continue
		if(float(rating.text)>6.6 and float(rating.text)<8.6):
			name=soup.find("h1",{"itemprop":"name"}).text
			#print(name.text)
			director=[]
			director2=[]
			di=soup.find_all("span",{"itemprop":"director"})
			for d1 in di:
				if(d1 in director2):
					continue
				d2=d1.find("span",{"class":"itemprop"})
				if(d2==None):
					continue
				director.append(d2.text)
				director2.append(d1)
			obj={}
			obj['rating']=rating.text
			obj['directors']=director
			dicti[name]=obj
			number=number+1
			print(number,name,obj)
			#writefn(name)
			if(number>=200):
				break
	writefn()			
def writefn():
	csvfile = open('imdbcrawler.csv', 'w',newline='')
	csvwriter = csv.writer(csvfile)
	for name in dicti:
		wp="name "+name+" rating "+dicti[name]['rating']+" directors "
		for item in dicti[name]['directors']:
			wp=wp+" "+item
		csvwriter.writerow(wp)	
	csvfile.close()



k=requests.get("http://www.imdb.com")
extract()
#print(dicti)
#print(len(m))
#print(Pull_req)
