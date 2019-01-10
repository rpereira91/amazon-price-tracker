from AmazonDB import Base, AmazonProduct, ProductData
from bs4 import BeautifulSoup
import requests
import datetime
class PriceScraper:
    prod_data = ProductData()

    def process_amazon_id(self):
        with open("IDList.csv") as f:
            id_list = f.readlines()
        id_list = [x.strip() for x in id_list]
        for i in id_list:
            url = "https://www.amazon.ca/dp/"+i
            self.insert_amazon_data(url,i)

    def insert_amazon_data(self,url,id):
        page = requests.get(url)
        item_data = BeautifulSoup(page.text,'lxml')
        Title, Price, availability = self.get_title(item_data),self.get_price(item_data),self.get_availability(item_data)
        self.prod_data.insert_data(Title, id, float(Price),availability,url,datetime.date.today())
        
    def get_title(self,item_data):
        return item_data.find("span", {"id" : "productTitle"}).get_text().strip().split(",")[0] if item_data.find("span", {"id" : "productTitle"}).get_text() else ""

    def get_price(self,item_data):
        if item_data.find("span", {"id" : "priceblock_ourprice"}):
            return (item_data.find("span", {"id" : "priceblock_ourprice"}).get_text().strip()[5:])
        elif item_data.find("span", {"id" : "priceblock_dealprice"}):
            return (item_data.find("span", {"id" : "priceblock_dealprice"}).get_text().strip()[5:])
        else:
            return 0.00
    
    def get_availability(self,item_data):
        return item_data.find("div", {"id" : "availability"}).get_text().strip() if item_data.find("div", {"id" : "availability"}).get_text() else ""
    #get all the IDs as a set
    def get_all_id(self):
        prod_id = []
        for i in self.prod_data.view_all():
            prod_id.append(i.product_id)
        return(set(prod_id))

def main():
    price = PriceScraper()
    # price.process_amazon_id()
if __name__ == "__main__":
    main()