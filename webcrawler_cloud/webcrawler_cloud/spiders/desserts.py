import scrapy
from bs4 import BeautifulSoup



class DessertsSpider(scrapy.Spider):
    name = "desserts"
    #allowed_domains = ["https://www.allrecipes.com/recipes/79/desserts"]
    #start_urls = ["http://www.allrecipes.com/recipes/79/desserts/"]

    def start_requests(self):
        url = 'https://cooking.nytimes.com/tag/dessert?ds_c=71700000052595478&gclid=CjwKCAjw0N6hBhAUEiwAXab-TTaC37YWlUOeH77MhtcKsQvMdz_MtbiQcKS1pWY_hL4Opk1URRH2ORoC5OEQAvD_BwE&gclsrc=aw.ds'
        request = scrapy.Request(url=url, callback = self.parse)
        yield request
    
    def parse(self, response):
        parse_obj = BeautifulSoup(response.text, "html") 
        
        #create a file object where we save our results
        filename = "foodrecipe-dessert.txt"
        textfile = open(filename, "w")
        
        # recipes with images
        recipes_nytimes = parse_obj.find_all('h3', {"class": "name"})
        
        
        for n in recipes_nytimes:
            recipe_name = n.get_text()
            print(recipe_name)
            textfile.write(recipe_name + "\n")
            
        
        
        textfile.close()
        print("File successfully saved")
        
        pass
