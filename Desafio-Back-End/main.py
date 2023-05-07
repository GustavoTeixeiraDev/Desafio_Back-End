import requests
import json
import sqlite3

# Faz a requisição GET à API
response = requests.get('https://dummyjson.com/products')

# Verifica se a requisição foi bem sucedida
if response.status_code == 200:
    # Converte a resposta em JSON
    products = json.loads(response.text)
    
    # Inicializa as variáveis de soma e contagem dos preços de smartphones
    total_price = 0
    count = 0
    
    # Conecta ao banco de dados
    conn = sqlite3.connect('produtos.db')
    c = conn.cursor()
    
    # Cria a tabela de produtos, caso ela ainda não exista
    c.execute('''CREATE TABLE IF NOT EXISTS produtos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  category TEXT,
                  price REAL)''')
    
    # Insere os dados de cada produto na tabela de produtos
    for product in products:
        # Verifica se o produto é um dicionário e contém os campos category e price
        if isinstance(product, dict) and 'category' in product and 'price' in product:
            # Insere os dados do produto na tabela de produtos
            c.execute("INSERT INTO produtos (title, category, price) VALUES (?, ?, ?)",
                      (product.get('title', ''), product.get('category', ''), product.get('price', 0)))
            
            # Verifica se o produto pertence à categoria smartphones
            if product['category'] == 'smartphones':
                # Adiciona o preço do produto à soma total
                total_price += product['price']
                # Incrementa o contador de produtos da categoria smartphones
                count += 1
    
    # Salva as mudanças no banco de dados
    conn.commit()
    
    # Calcula a média dos preços dos smartphones
    if count > 0:
        avg_price = total_price / count
    else:
        avg_price = 0
    
    # Imprime o resultado
    print("Preço médio dos smartphones: $ {:.2f}".format(avg_price))

    # faz a requisição à API de Chuck Norris e armazena a piada em uma variável
    cn_response = requests.get('https://api.chucknorris.io/jokes/random')
    cn_joke = cn_response.json()['value']

    # exibe a piada no terminal
    print("\nAqui vai uma piada sobre Chuck Norris: \n{}".format(cn_joke))

    
    # Fecha a conexão com o banco de dados
    conn.close()
    
else:
    # Imprime uma mensagem de erro caso a requisição tenha falhado
    print("Erro ao acessar a API")
