import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url1 = 'https://www.hostgator.com/vps-hosting'
url2 = 'https://www.vultr.com/products/bare-metal/'

class Crawler(object):
    """Crawler pai"""

    def __init__(self):
        self.df = None
        self.dict_from_list = {}
        self.key_list = ['STORAGE/SSD DISK','CPU/VCPU', 'MEMORY/RAM','BANDWITDH/Dedicated IP','PRICE [$/mo]']
        self.list_price = []
        self.list_all = []
        self.new_list = [[] for i in range(5)]

    def sort_data(self):
        for i in range(len(self.list_all)): #ordenando e fazendo uma lista de lista
            if i%5 == 0:
                self.new_list[i%5].append(self.list_all[i])
            elif i%5 == 1:
                self.new_list[i%5].append(self.list_all[i])
            elif i%5 == 2:
                self.new_list[i%5].append(self.list_all[i])
            elif i%5 == 3:
                self.new_list[i%5].append(self.list_all[i])
            elif i%5 == 4: 
                self.new_list[i%5].append(self.list_all[i])

    def create_df(self):
        self.sort_data()
        self.dict_from_list = dict(zip(self.key_list, self.new_list))
        self.df = pd.DataFrame.from_dict(self.dict_from_list)

    def crawler_run(self):
        pass

    def save_json(self,number):
        self.df.to_json(f'table_data_{number}.json', orient='index')

    def save_csv(self,number):
        self.df.to_csv(f'table_data_{number}.csv', index=False)

    def print(self):
        print(self.df)
        pass

class Crawler1(Crawler):
    """Crawler filho 1"""

    def crawler_run(self):
        response = requests.get(url1)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('section', class_= 'pricing-card-container false undefined')

        i=0
        for price in table.find_all('p', class_ = 'pricing-card-price'):
            self.list_price.append(price.text.strip())

        for item in table.find_all('li', class_= 'pricing-card-list-items'):
            self.list_all.append(item.text.strip()) 
            
            if item.text.count("bandwidth") == 1:
                self.list_all.append(self.list_price[i])
                i+=1

        self.list_all = [re.sub(r'Â|\*', '',x) for x in self.list_all]

        self.create_df()
        


class Crawler2(Crawler):
    """Crawler filho 2"""

    def crawler_run(self):
        response = requests.get(url2)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('div', class_= 'row row--eq-height packages')

        i=0

        for price in table.find_all('span', class_ = 'price__value'):
            self.list_price.append(price.text.strip())

        for item in table.find_all('li', class_= 'package__list-item'):
            if item.text.count("Network") == 0:
                self.list_all.append(item.text.strip()) 
                
            if item.text.count("Bandwidth") == 1:
                self.list_all.append(self.list_price[i])
                i+=1

        self.list_all[15] = self.list_all[15]+' / '+self.list_all[16] #esse campo na tabela contém dois valores
        del(self.list_all[16])

        self.list_all = [re.sub(r'\t|\n', '',x) for x in self.list_all]

        self.create_df()  


def options():
    option = int(input(''' Escolha dentre as opções:
    1. print
    2. salvar como csv
    3. salvar como json 
    4. sair
    Escolha: '''))
    
    if option == 1:
        c1.print()
        c2.print()
    elif option == 2:
        c1.save_csv('1')
        c2.save_csv('2')
    elif option == 3:
        c1.save_json('1')
        c2.save_json('2')
    elif option == 4:
        exit()


if __name__ == "__main__":
    c1 = Crawler1()
    c1.crawler_run()

    c2 = Crawler2()
    c2.crawler_run()
    
    options()