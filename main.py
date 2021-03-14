from csv import reader
from bs4 import BeautifulSoup as bs
import urllib.request
import os

os.system("cls")


#start of program

def getTagText(l):
    for i in range(0, len(l)):
        # We would like to add more tags but     
        
        tlist = ['a', 'abbr', 'acronym', 'b', 'bdo', 'br', 'button', 'cite', 'code', 'dfn', 'em', 'i', 'img', 'input', 'kbd', 'label', 'map', 'object', 'output', 'q', 'samp', 'script', 'select', 'small', 'span', 'strong', 'sub', 'sup', 'textarea', 'time', 'tt', 'var']
        for tag in tlist:
            for match in l[i].find_all(tag):
                match.unwrap()
        l[i] = l[i].get_text().split()
    return(l)   

def makeSList(site, tag):   
    l = [] 
    if(tag == "h1"):
        for i in site.h1s:
            for t in i:
                l.append(t)
    elif(tag == "h2"):
        for i in site.h2s:
            for t in i:
                l.append(t)
    elif(tag == "h3"):
        for i in site.h3s:
            for t in i:
                l.append(t)  
    elif(tag == "title"):
        for i in site.title:
            for t in i:
                l.append(t)           
    elif(tag == "firstP"):
        for i in site.firstP:
            for t in i:
                l.append(t)
    elif(tag == "strong"):
        for i in site.strong:
            for t in i:
                l.append(t)
    elif(tag == "em"):
        for i in site.em:
            for t in i:
                l.append(t)            
    return l




class Site:
    def __init__(self, url):
        # constructor
        self.url = url
        self.html = urllib.request.urlopen(url).read()
        self.soup = bs(self.html, 'html.parser')
        self.h1s = getTagText(self.soup.find_all('h1'))
        self.h2s = getTagText(self.soup.find_all('h2'))
        self.h3s = getTagText(self.soup.find_all('h3'))
        self.images = self.soup.find_all('img')
        self.imageAlts = []
        for image in self.images:
            self.imageAlts.append(image.attrs['alt'])
        self.title = getTagText(self.soup.find_all('title'))
        self.firstP = getTagText([self.soup.find('p')])
        self.strong = getTagText(self.soup.find_all('strong'))
        self.em = getTagText(self.soup.find_all('em'))
        self.weight = 0
        # end constructor
        
    def setWeight(self, weight):
        self.weight = weight



sites = []



with open("link_list.txt") as csvfile:
    file = reader(csvfile)
    for rec in file:
        sites.append(Site(rec[0]))


print(makeSList(sites[0], 'h1'))



