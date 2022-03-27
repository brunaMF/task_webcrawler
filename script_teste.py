import requests
import numpy as np
from bs4 import BeautifulSoup


site1 = 'https://www.vultr.com/pricing/#cloud-compute'
site2 = 'https://www.vultr.com/products/bare-metal/'

response = requests.get(site2)

#print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('div', attrs={'class': 'row row--eq-height packages'})

for item in table.find_all('li', attrs={'class': 'package__list-item'}):
    print(item.text.strip())