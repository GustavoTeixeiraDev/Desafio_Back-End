#Importando as bibliotecas
import pandas as pd
import requests
import sqlite3

#Criando o bd
conn = sqlite3.connect('produtos.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS produtos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  category TEXT,
                  price REAL)''')

#Coletando os dados e fazendo um DataFrame com os dados 
url = 'https://dummyjson.com/products'
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data["products"])

#Filtrando os dados "Smartphones"
smartphones = df[df['category'] == 'smartphones']

#Insere os dados dos produtos no Banco de Dados
for index, row in df.iterrows():
    title = row['title']
    category = row['category']
    price = row['price']
    
    c.execute("INSERT INTO produtos (title, category, price) VALUES (?, ?, ?)", (title, category, price))

conn.commit()

#Calculda preço médio
preco_medio_smartphones = smartphones['price'].mean()

#Imprime a mensagem no terminal e arredonda para 2 casas decimais
mensagem = "## Resultado da coleta de dados ##\nPreço médio dos smartphones: $ {:.2f}.".format(preco_medio_smartphones)
print(mensagem)

#Faz a requisição à API de Chuck Norris e armazena a piada em uma variável
cn_response = requests.get('https://api.chucknorris.io/jokes/random')
cn_joke = cn_response.json()['value']

#Imprime a piada no terminal
print("\nAqui vai uma piada sobre Chuck Norris: \n{}".format(cn_joke))

    
#Fecha a conexão com o banco de dados
conn.close()
