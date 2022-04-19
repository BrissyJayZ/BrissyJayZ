import urllib2
from selenium import webdriver
#import scrapy
from bs4 import BeautifulSoup
import pandas as pd
import math
import csv

class ypscraper(object):

    def __init__(self, path='c:\\python27\\scraper\\health\\'):
        #Path variable to save the results
        self.path = path
        #Load the chrome driver
        self.driver = webdriver.Chrome("C:\\Python27\\dl\\chromedriver.exe")
        #Dummy variable for counting output files
        self.outcount = 1
        #Initialise postcode
        self.postc = '2000'

    def scrapebypostc(self, postpath='c:\python27\scraper\postcodes.csv'):
        self.postlist=[]
        with open(postpath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile)
            self.postlist=list(spamreader)
        for rlist in self.postlist:
            self.postc = str(rlist[0])
            self.scrapeall('')

    def scrapeall(self, hint):
        letterlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        for i in letterlist:
            self.getnopages(hint + i)
            print "Postcode: " + self.postc + " letter: " + hint + i + " pages: " + str(self.pagestoscrape)
            if self.pagestoscrape > 29:
                self.scrapeall(hint + i)
            else:
                self.scrapeletter(hint + i)

    def scrapeletter(self, letter):
        #Determine how many pages to scrape
        if self.pagestoscrape > 0:
            #Scrape all the other results
            for i in range(1, self.pagestoscrape + 1):
                yp = 'https://www.yellowpages.com.au/search/listings?clue=' + letter + '*&locationClue=' + self.postc + '&pageNumber=' + str(i) + '&referredBy=www.yellowpages.com.au&&eventType=pagination'
                self.scrapepage(yp, self.postc + letter + str(i))
                print str(i) + " out of " + str(self.pagestoscrape)
                
    def scrapehealth(self, pageno):
        yp = 'https://healthengine.com.au/find/text/Australia/Page-' + str(pageno) + '/?search=GP'
        self.scrapepage(yp, 'page' + str(pageno))
        
    def scrapehealthall(self,start,end):
        for pageno in range(start,end+1):
            self.scrapehealth(pageno)

    def getnopages(self, searchterm):
        link = 'https://www.yellowpages.com.au/search/listings?clue=' + searchterm + '*&locationClue=' + self.postc + '&lat=&lon=&selectedViewMode=list'
        self.driver.get(link)
        soup = BeautifulSoup(self.driver.page_source)
        try:
            searchtermresult = soup.find('h1').text.split()[0].lower() #If there are any results
        except:
            searchtermresult = 'none'
        if searchtermresult == searchterm + '*':
            mystr = soup.find('span', class_='emphasise').text
            noresults = [int(s) for s in mystr.split() if s.isdigit()][0]
            self.pagestoscrape = int(math.ceil(noresults/35.0))
        else:
            self.pagestoscrape = 0

    def scrapepage(self, link, outname):
        #Open the webpage
        self.driver.get(link)
        #Throw the source code into beautiful soup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        #Create dataframe to store the data
        #print(soup)
        df=pd.DataFrame(columns=('Business name','Phone','Full Address'))
        #Split the page source result into individual results
        dividers = soup.findAll('div', class_='search-card-overflow')
        #dividers = soup.findAll('div', class_='listing listing-search listing-data')
        
        #dividers2 = dividers[0].findAll('span', class_='search-phone')
        #dividers3 = dividers[0].findAll('div', class_='search-addie')
        #dividers4 = dividers[0].findAll('h2', class_='search-main-title')

        #For each result, capture the data and add into dataframe
        for i in range(0,len(dividers)):
            A=[]
            try:
                A.append(dividers[i].findAll('h2', class_='search-main-title')) #name
            except:
                A.append("")
            try:
                A.append(dividers[i].findAll('span', class_='search-phone')) #phone
            except:
                A.append("")
            try:
                A.append(dividers[i].findAll('div', class_='search-addie')) #Full Address
            except:
                A.append("")

            df.loc[i]=A
            #print(A)
            del A
        #Save the output into a csv
        #print(df)
        print(str(outname))
        df.to_csv(self.path + str(outname) + '.csv', encoding='utf-8')
        #Increment output counter
        self.outcount += 1

myscraper = ypscraper()
#myscraper.scrapebypostc()
#myscraper.scrapehealth(817)
myscraper.scrapehealthall(45,100)

