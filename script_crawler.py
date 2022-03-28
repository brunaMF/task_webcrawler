import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url1 = 'https://www.hostgator.com/vps-hosting'
url2 = 'https://www.vultr.com/products/bare-metal/'

class Crawler(object):

    def __init__(self,url):
        self.df = None
        self.dict_from_list = {}
        self.key_list = ['STORAGE/SSD DISK','CPU/VCPU', 'MEMORY/RAM','BANDWITDH/Dedicated IP','PRICE [$/mo]']
        self.list_price = []
        self.list_all = []
        self.new_list = [[] for i in range(5)]
        self.url = url

    def sort_data(self):
        [self.new_list[i%5].append(self.list_all[i]) for i in range(len(self.list_all))]

    def create_df(self):
        self.sort_data()
        self.dict_from_list = dict(zip(self.key_list, self.new_list))
        self.df = pd.DataFrame.from_dict(self.dict_from_list)

    def crawler_run(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find(re.compile("(section|div)"), class_= re.compile("(pricing-card-container false undefined|row row--eq-height packages)"))

        i=0
        
        [self.list_price.append(price.text.strip()) for price in table.find_all(re.compile("(p|span)"), class_ = re.compile("price"))]

        for item in table.find_all('li', class_= re.compile("(pricing-card-list-items|package__list-item)")):
            if item.text.count("Network") == 0:
                self.list_all.append(item.text.strip()) 
                
            if item.text.lower().count("bandwidth") == 1:
                self.list_all.append(self.list_price[i])
                i+=1

            if self.url.count('vps-hosting') and item.text.count('SSD') == 1: #é feita uma troca para a ordenação ser a mesma nos dois crawlers
                posicao = max(idx for idx, val in enumerate(self.list_all))
                aux = self.list_all[posicao]
                self.list_all[posicao] = self.list_all[posicao-2] 
                self.list_all[posicao-2] = aux

        if self.url.count('bare-metal'):
            self.list_all[15] = self.list_all[15]+' / '+self.list_all[16] #esse campo na tabela da url2 contém dois valores, por isso será unido os dois valores 
            del(self.list_all[16])

        self.list_all = [re.sub(r'\t|\n|Â|\*', '',x) for x in self.list_all] #elimando caracteres indesejados

        self.create_df()  

    def save_json(self,number):
        self.df.to_json(f'table_data_{number}.json', orient='index')

    def save_csv(self,number):
        self.df.to_csv(f'table_data_{number}.csv', index=False)

    def print(self):
        print(self.df)
        pass

def options(option_url):
    option = int(input(''' Escolha dentre as opções:
    1. print
    2. salvar como csv
    3. salvar como json 
    4. sair
    Opção: '''))
    
    if option == 1 and option_url==1:
        c1.print()
    elif option == 1 and option_url==2:
        c2.print()
    elif option == 2 and option_url==1:
        c1.save_csv('1')
    elif option == 2 and option_url==2:
        c2.save_csv('2')
    elif option == 3 and option_url==1:
        c1.save_json('1')
    elif option == 3 and option_url==2:
        c2.save_json('2')
    elif option == 4:
        exit()


if __name__ == "__main__":
    option_url = int(input(f''' Escolha dentre as opções:
    1. url 1: {url1} 
    2. url 2: {url2}
    Opção: '''))

    if option_url == 1:
        c1 = Crawler(url1)
        c1.crawler_run()
    elif option_url == 2:
        c2 = Crawler(url2)
        c2.crawler_run()
    
    options(option_url)