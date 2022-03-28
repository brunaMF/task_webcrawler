# Task WebCrawler

Dadas as opções de máquinas nas páginas-alvo, o crawler deve extrair os seguintes
atributos de cada opção de máquina:

- CPU / VCPU
- MEMORY
- STORAGE / SSD DISK
- BANDWIDTH / TRANSFER
- PRICE [ $/mo ]

Páginas-alvo:

1. https://www.hostgator.com/vps-hosting (Apenas tabela hardware)
2. https://www.vultr.com/products/bare-metal/ (Tabela Bare Metal)

Ao executar um crawler, devem ser disponíveis as seguintes opções independentes entre si:

- print: Imprime resultados na tela
- save_csv: Salva dados em arquivo csv
- save_json: Salva dados em arquivo json

# Como executar

``` shell
python3 script_crawler.py
```

Após a execução, deverá ser escolhido dentre as duas urls apresentadas e em seguida a opção que se deseja.

