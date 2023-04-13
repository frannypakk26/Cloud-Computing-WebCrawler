#Francine Dela Cruz and Sienna Nguyen
#Distributed and Cloud Computing Spring 2023
#Webcrawler/Webscraping Azure

# a webcrawler consists of three parts: 
# webcrawler- the part of the code that's going to jump from link to link or website to website
#resource extraction- getting the raw information off of the web: html pdf etc
#information cleaning- having the data be structured
#all three parts should be treated independently

#types of URLS:
#absolute URL: URL with protocol name, root URL, document name
#relative URL: URL without root URL and protocol name


#step1: implement all the libraries used for the crawl
import multiprocessing
#BeautifulStoneSoup is a package for parsing HTML and XML documents 
#it creates a parse tree for parsed pages that can be used to extract data from HTML
from bs4 import BeautifulSoup 
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import requests



#step3: this MultithreadWebcrawler class is used to initialize all the variables in the constructor, 
# assigning a base URL and then format the base URL into absolute URL, using schemes as HTTPS and net location
#this creates a queue to store all the URLs of crawl frontier and put the first item in as a seed URL

class MultiThreadedWebCrawler:
    def __init__(self, seed_url):
        self.seed_url = seed_url
        self.root_url = '{}://{}'.format(urlparse(self.seed_url).scheme, urlparse(self.seed_url).netloc)

        self.pool = ThreadPoolExecutor(max_workers=5)
        self.scrapedPages = set([])
        self.crawlerQueue = Queue()
        self.crawlerQueue.put(self.seed_url)

#step7: this method uses the BeautifulStoneSoup operator to extract all the anchor tags that are in the HRML document
#Soup.find_all('a', href=True) returns a list of all the items that contain all the anchor tags present in the webpage
#then it stores all the tags in a list
#runs a for loop for every tag present, it retrieves the value associated with the href in the tag using the link['href']
#for each retrieved URL check whether it is any of te absolute URL or relative URL

    def parseLinks(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        AnchorTags = soup.find_all('a', href=True)
        for link in AnchorTags:
            url = link['href']
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                if url not in self.scrapedPages:
                    self.crawlerQueue.put(url)


#step6: this method has the webpage data pass into the BeautifulStoneSoup operator to organize and formal the messy webdata by fixing bad HTML and present an
#an easily-traversable structure

    def scrapeInfo(self, html):
        soup = BeautifulSoup(html, "html5lib")
        webpageContent = soup('p')
        text = ''

        for paragraph in webpageContent:
            if not ('https:' in str(paragraph.text)):
                text = text + str(paragraph.text).strip()
        print(f"\nThe text present in the Webpage is: \n", text, '\n')
        return


    def afterScrape_callback(self, res):
        result = res.result()
        if result and result.status_code == 200:
            self.parseLinks(result.text) #for extracting all the links and pass the result
            self.scrapeInfo(result.text) #for extracting the content and pass the result

#step5: this method uses the handshaking method to place the request and set the default time as 3 and maximum as 30
#ince the request is successfu return the result set
#handshaking mthod: an automated process of negotiation that dynamically sets parameters of a communications chanell established between
#two entities before normal communication over the channel begins

    def scrapePage(self, url):
        try:
            result = requests.get(url, timeout=(3,30))
            return result
        except requests.RequestException:
            return
    
#step4: this method is used an an infinite loop to add a link to the frontier and extracting information anf to display the name of the current executing process
#this gets a url from the crawl frontier ans is assigned a timeout for 60 seconds
#this crecks if the website has already been visited or not and if it hasnt, the URL will be added to the scrapedPages method to store in the history of the visited pages
#and choose from a poo; ;pf threads amd pass the scrape page and target URl

    def runWebCrawler(self):
        while True:
            try:
                print("Name of the current running process is: ", multiprocessing.current_process().name, '\n')
                targetURL = self.crawlerQueue.get(timeout=60)
                if targetURL not in self.scrapedPages:
                    print("Current Scraping URL: {}".format(targetURL))
                    se;f.currentScraping_url = "{}".format(targetURL)
                    self.scrapedPages.add(targetURL)
                    job = self.pool.submit(self.scraped.page, targetURL)
                    job.add_done_callback(self.postScrapeCallBack)
            except Empty:
                return
            except Exception as e:
                print(e)
                continue

    def info(self):
        print('\n Seed URL is: ', self.seed_url, '\n')
        print('Scraped pages are: ', self.scrapedPages, '\n')
        
#step2: create a main program
if __name__ == '__main__' :
    cc = MultiThreadedWebCrawler("https://www.geeksforgeeks.org/");
    cc.runWebCrawler()
    cc.info()
