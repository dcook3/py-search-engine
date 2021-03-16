from csv import reader
from bs4 import BeautifulSoup as bs
import urllib.request
import os
import tkinter as tk
import webbrowser
from PIL import Image, ImageTk
os.system("cls")


#start of program

#Functions----------------------------------------------------------------------------------------------

#This function converts a tag list so that it has all of its words inside a single unnested list
def makeSList(ls, tag):
    l = [] 
    if(tag == "h1"):
        for i in ls:
            for t in i:
                l.append(t)
    elif(tag == "h2"):
        for i in ls:
            for t in i:
                l.append(t)
    elif(tag == "h3"):
        for i in ls:
            for t in i:
                l.append(t)  
    elif(tag == "title"):
        for i in ls:
            for t in i:
                l.append(t)           
    elif(tag == "p"):
        for i in ls:
            for t in i:
                l.append(t)
    elif(tag == "strong"):
        for i in ls:
            for t in i:
                l.append(t)
    elif(tag == "em"):
        for i in ls:
            for t in i:
                l.append(t)            
    return l



#This function will take all text inside a tag and split the words into a list. It should also take out all irrelevent nested tags as well.
def getTagText(l, t):
    
    
    for i in range(0, len(l)):
        tlist = ['a', 'abbr', 'acronym', 'b', 'bdo', 'br', 'button', 'cite', 'code', 'dfn', 'em', 'i', 'img', 'input', 'kbd', 'label', 'map', 'object', 'output', 'q', 'samp', 'script', 'select', 'small', 'span', 'strong', 'sub', 'sup', 'textarea', 'time', 'tt', 'var']
        for tag in tlist:
            for match in l[i].find_all(tag):
                match.unwrap()
        l[i] = l[i].get_text().split()    
    return makeSList(l, t)
    

#Swap function
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



#Binary search function, takes in list and search term as parameters
def bns(ls, search):
    if len(ls) != 0 and search != "of" and search != "and" and search != 'the':
        sort(ls)
        min = 0
        max = len(ls) - 1
        guess = int((min + max) / 2)

        while (min < max and search != removeChars(ls[guess])):
            if (search < removeChars(ls[guess])):
                max = guess - 1
            else:
                min = guess + 1
            guess = int((min + max) / 2)   
        if search == removeChars(ls[guess]):
            #Found
            return True
        else:
            #Not Found
            return False
    else:
        return False
    
    
def removeChars(s):
    if type(s) == str:
        for char in '''()"{]}[.?/';:\\,''':
            s.replace(char, '')
        return s.lower()

#Sequential search function, takes list and search term as parameters
def seq(ls, search):
    if search != "of" and search != "and" and search != 'the':
        count = 0
        #Sequential search loop
        for i in range(0, len(ls)):
            if removeChars(ls[i]) == search:
                count += 1

        return count
    else:
        return 0


#Site weighting function.
def weightingFunc(search):
    #This function will use both binary and sequential search. The tags the are to be sequentially searched are seperate from tags that are to be binary serached.
    bnTags = ['h1', 'imgAlts']#Weights: 4, 4, 2
    seqTags = ['h2', 'h3', 'p', 'strong', 'title', 'em']#Weights: 1, 1, 1, 1, 1
    #Take global sites list and set weight based on search success. Higher success of search means higher weight.
    for site in sites:
        for tag in bnTags:
            if(tag == 'h1' and bns(site.h1s, search)):
                site.weight += 2
            
            elif(tag == 'imgAlts' and bns(site.imageAlts, search)):
                site.weight += 2
        for tag in seqTags:
            if(tag == 'h2'):
                count = seq(site.h2s, search)
                site.weight += count
            elif(tag == 'h3'):
                count = seq(site.h3s, search)
                site.weight += count
            elif(tag == 'p'):
                count = seq(site.p, search)
                site.weight += count
            elif(tag == 'strong'):
                count = seq(site.strong, search)
                site.weight += count
            elif(tag == 'title'):
                count = seq(site.title, search)
                site.weight += count * 2
            else:
                count = seq(site.em, search)
                site.weight += count



#Reset all weights
def resetWeights():
    for site in sites:
        site.weight = 0


#Site class. Has properties for many site characteristics such as html, url, and tag lists. Each real site will be initalized as a new site object.
class Site:
    def __init__(self, url):
        #Inital site properties
        self.url = url
        self.html = urllib.request.urlopen(url).read()            #Unparsed HTML
        self.soup = bs(self.html, 'html.parser')                  #Use beautiful soup to parse into readable HTML data
        

        #Img tag processing----------------------------------------------------
        self.images = self.soup.find_all('img')
        #Parse out everything but 'alt' attribute. Store into imageAlts list.
        self.imageAlts = []
        for image in self.images:
            self.imageAlts.append(image.attrs['alt'])
        #----------------------------------------------------------------------


        #p tag processing------------------------------------------------------
        self.fPtags = []
        self.ptags = self.soup.find_all('p')
        #Taking in first 5 p tags, append them to fPtags list.
        for i in range(0, len(self.ptags)): 
            if i < 5:
                self.fPtags.append(self.ptags[i])
            else:
                i = len(self.ptags)
        #Now take first five p tags and parse out text inside.
        self.p = getTagText(self.fPtags, 'p')
        #----------------------------------------------------------------------


        #All other relevant tags
        self.title = getTagText(self.soup.find_all('title'), 'title')
        self.h1s = getTagText(self.soup.find_all('h1'), 'h1')
        self.h2s = getTagText(self.soup.find_all('h2'), 'h2')
        self.h3s = getTagText(self.soup.find_all('h3'), 'h3')
        self.strong = getTagText(self.soup.find_all('strong'), 'strong')
        self.em = getTagText(self.soup.find_all('em'), 'em')
        #Set site-specific weight property
        self.weight = 0



#tkinter GUI class

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1600x900")
        self.master.title("Not Google")
        self.master.config(bg="white")
        self.master.resizable(False, False)
        self.grid()
        self.create_widgets()


    def create_widgets(self): #~100px:15ch, width in pixels/6.6 = width in ch
        self.img = Image.open("assets/gogle.png")
        self.img = self.img.resize((350, 134)) #350x134px
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.imageLabel = tk.Label(self.master, bg="white", image = self.tkimage)
        self.tBox = tk.Entry(text="Search Here", width = 109)
        self.b = tk.Button(self.master, text="Search", width = 12, command = lambda : self.getLinks(self.tBox.get().lower()))
        self.canvas = tk.Canvas(self.master, width = 95, height = 600, bg="white", bd=0)
        self.vbar = tk.Scrollbar(self.canvas, orient = tk.VERTICAL)
        
        self.vbar.config(command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.vbar.set)
        
        self.linkButtons = []
        self.imageLabel.grid(row = 1, column = 1, padx = (500, 0), pady = (20, 0))
        self.tBox.grid(row=2, column = 1, padx = (400, 0), pady= (25, 50))
        self.b.grid(row=2, column=2, pady= (25, 50))
        

    
    def getLinks(self, search):
        for b in self.linkButtons:
            b.destroy()
        self.linkButtons = []
        resetWeights()
        print(search.split())
        for word in search.split():
            
            weightingFunc(word)
        for i in range(0, len(sites) - 1):
            for k in range(0, len(sites) - 1):
                if sites[k].weight < sites[k + 1].weight:
                    swap(sites, k)
        
        for site in sites:
            self.linkButtons.append(tk.Button(self.canvas, text = " ".join(site.title), bd = 0, bg="white", anchor = "w", activebackground = "grey", width = 90 ,command = lambda aurl = site.url: webbrowser.open_new(aurl)))
            
        for b in range(0, len(self.linkButtons)):
            self.linkButtons[b].grid(row=b+1, column = 1, padx = (400, 0), pady= (0, 10))
        self.canvas.grid(row = 3, column = 1)
        self.vbar.grid(row = 1, column = 2, rowspan = len(self.linkButtons), sticky = "NS")
            

    def start(self):
        self.master.mainloop()


#Main program-------------------------------------------------------------------------------------------
sites = []

with open("link_list.txt") as csvfile:
    file = reader(csvfile)
    for rec in file:
        sites.append(Site(rec[0]))

# app = Application(master= tk.Tk())
# app.start()

search = input("Enter search query: ").lower()
for word in search.split():
        weightingFunc(word)
for i in range(0, len(sites) - 1):
        for k in range(0, len(sites) - 1):
            if sites[k].weight < sites[k + 1].weight:
                swap(sites, k)

print("\nResults: ")
for site in sites:
    print(site.title)

