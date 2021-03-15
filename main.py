from csv import reader
from bs4 import BeautifulSoup as bs
import urllib.request
import os
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
os.system("cls")


#start of program

def getTagText(l):
    for i in range(0, len(l)):
        
        
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
    elif(tag == "p"):
        for i in site.p:
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





def swap(ls, i):
    temp = ls[i]
    ls[i] = ls[i+1]
    ls[i+1] = temp

#Bubble sort function takes in list to sort
def sort(ls):
    for i in range(0, len(ls) - 1):

        for k in range(0, len(ls) - 1):

            if ls[k] > ls[k + 1]:
                swap(ls, k)    

#Binary search function, takes in list to search
def bns(ls, search):
    sort(ls)
    #Init min and max. Start at 0 for min and use max index, obtained from records, for max.
    min = 0
    max = len(ls) - 1
    #Calculate midway point
    guess = int((min + max) / 2)
    #As long as min is still less than max, search term can still be found. And if search term was found, break loop.
    while (min < max and search != ls[guess]):
        #If the search term is alphabetically less than current guess index
        if (search < ls[guess]):
            max = guess - 1
        else:
            min = guess + 1
        #New midpoint
        guess = int((min + max) / 2)   
    #Determine if the term was found and print corresponding statement
    if search == ls[guess]:
        #Found
        return 1
    else:
        #Not Found
        return 0
    
    

#Sequential search function, takes list in to search
def seq(ls, search):
    f = -1  #Init index var. -1 means not found
    count = 0
    #Sequential search loop
    for i in range(0, len(ls)):
        if ls[i] == search:
            f = i
            count += 1
            
    #If f is still -1, search term was not found.
    if f == -1:
        return 0

    return count + 1



# 1 - 1/count
def weightingFunc(search):
    bnTags = ['h1', 'title', 'imgAlts']# 4, 4, 2
    seqTags = ['h2', 'h3', 'p', 'strong', 'em']# 1, 1, 1, 1, 1,  
    for site in sites:
        for tag in bnTags:
            if(tag == 'h1' and bns(makeSList(site, tag), search)):
                site.weight+= 2
            elif(tag == 'title' and bns(makeSList(site, tag), search)):
                site.weight+= 2
            elif(tag == 'title' and bns(makeSList(site, tag), search)):
                site.weight+= 2
        for tag in seqTags:
            count = seq(makeSList(site,tag), search)
            if(count != 0):
                site.weight+= 1 - (1 / count)

def resetWeights():
    for site in sites:
        site.weight = 0
    
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
        self.fPtags = []
        self.ptags = self.soup.find_all('p')
        for i in range(0, len(self.ptags)): 
            if i < 5:
                self.fPtags.append(self.ptags[i])
            else:
                i = len(self.ptags)
        self.p = getTagText(self.fPtags)
        self.strong = getTagText(self.soup.find_all('strong'))
        self.em = getTagText(self.soup.find_all('em'))
        self.weight = 0
        # end constructor
        
   

sites = []

with open("link_list.txt") as csvfile:
    file = reader(csvfile)
    for rec in file:
        sites.append(Site(rec[0]))



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1600x900")
        self.master.title("Not Google")
        self.master.resizable(False, False)
        self.grid()
        self.create_widgets()


    def create_widgets(self): #~100px:15ch, width in pixels/6.6 = width in ch
        self.img = Image.open("assets/gogle.png")
        self.img = self.img.resize((350, 134)) #350x134px
        self.tkimage = ImageTk.PhotoImage(self.img)
        tk.Label(self.master, image = self.tkimage).grid()
        
        self.tBox = tk.Entry(text="Search Here", width = 109)
        self.b = tk.Button(self.master, text="Search", width = 12, command = lambda : self.getLinks(self.tBox.get()))
        self.linkButtons = []
        self.tBox.grid(row=2, padx = (400, 0), pady= (25, 50))
        self.b.grid(row=2, column=2, pady= (25, 50))

    
    def getLinks(self, search):
        for b in self.linkButtons:
            b.destroy()
        self.linkButtons = []
        resetWeights()
        for word in search.split():
            weightingFunc(word)
        for i in range(0, len(sites) - 1):
            for k in range(0, len(sites) - 1):
                if sites[k].weight < sites[k + 1].weight:
                    swap(sites, k)
        
        for site in sites:
            self.linkButtons.append(tk.Button(self.master, text = site.title[0], command = lambda aurl = site.url: webbrowser.open_new(aurl)))
        for b in range(0, len(self.linkButtons)):
            self.linkButtons[b].grid(row=b+3)

    def start(self):
        self.master.mainloop()


app = Application(master= tk.Tk())
app.start()

