import requests
import numpy as np
from bs4 import BeautifulSoup
import csv
import pandas as pd


site1 = 'https://www.vultr.com/pricing/#cloud-compute'
site2 = 'https://www.vultr.com/products/bare-metal/'

response = requests.get(site2)

#print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('div', attrs={'class': 'row row--eq-height packages'})

key_list = ['STORAGE/SSD DISK','CPU/VCPU', 'MEMORY/RAM','BANDWITDH/Dedicated IP','PRICE [$/mo]']
key_list2 = ['intel1', 'intel2', 'intel3', 'intel4']
i=0

list_price = []
list_all = []

for price in table.find_all('span', class_ = 'price__value'):
    list_price.append(price.text.strip())

for item in table.find_all('li', attrs={'class': 'package__list-item'}):
    if item.text.count("Network") == 0:
        list_all.append(item.text.strip()) 
        
    if item.text.count("Bandwidth") == 1:
        list_all.append(list_price[i])
        i+=1
    
    #print(item.text.strip())

list_all[15] = list_all[15]+' / '+list_all[16] #esse campo na tabela contém dois valores
del(list_all[16])

list_all = [x.replace('\t', '') for x in list_all]
list_all = [x.replace('\n','') for x in list_all]

nova_lista = [[] for i in range(5)]

for i in range(len(list_all)): #ordenando e fazendo uma lista de lista
    if i%5 == 0:
        nova_lista[i%5].append(list_all[i])
    elif i%5 == 1:
        nova_lista[i%5].append(list_all[i])
    elif i%5 == 2:
        nova_lista[i%5].append(list_all[i])
    elif i%5 == 3:
        nova_lista[i%5].append(list_all[i])
    elif i%5 == 4: 
        nova_lista[i%5].append(list_all[i])

dict_from_list = dict(zip(key_list, nova_lista))

df = pd.DataFrame.from_dict(dict_from_list)
df.to_csv('table_data.csv', index=False)
df.to_json('table_data.json', orient='index')


