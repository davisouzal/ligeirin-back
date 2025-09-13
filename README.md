# Projeto Ligeirin - Backend

Este é o backend do projeto **Ligeirin**, uma API REST desenvolvida em Flask, utilizando
SQLAlchemy como ORM e Flask-Migrate para controle de migrações do banco de dados.
Atualmente, a API disponibiliza um endpoint de listagem de produtos dos vendedores.
## Requisitos

-   **Python 3.8 ou superior**
-   **Flask**

## Instruções para Instalação

### 1. Clone o repositório
`git clone https://github.com/davisouzal/ligeirin-back.git`
`cd ligeirin-back` 

### 2. Crie um ambiente virtual (recomendado)

#### No Windows:

`python -m venv venv`
`venv\Scripts\activate` 

#### No Linux:

`python3 -m venv venv`
`source venv/bin/activate` 

### 3. Instale as dependências

Com o ambiente virtual ativado, execute:

`pip install -r requirements.txt` 

> Nota: Certifique-se de que o arquivo `requirements.txt` contenha as bibliotecas necessárias, como Flask e outras.

## Executando a aplicação

Após instalar as dependências, você pode iniciar a aplicação localmente.

#### No Windows:

`set FLASK_APP=run`
`set FLASK_ENV=development`
`flask run`

#### No Linux:
`export FLASK_APP=run`
`export FLASK_ENV=development`
`flask run` 

>Obs: Tabém pode rodar no modo debug:  `flask --app app --debug run`

Isso iniciará o servidor Flask em modo de desenvolvimento na porta `5000`. Acesse a aplicação via navegador no endereço `http://127.0.0.1:5000`.

# Rotas da API

## 1. Obter todos os produtos do catalogo
 - Rota: /products
 - Método: GET
 - Descrição: Retorna todos os produtos cadastrados pelos vendedores,
incluindo informações detalhadas sobre categoria, vendedor e variações do produto.
 - Exemplo de Resposta:
 ```
[
	{
		"careLevel": "BAIXO",
		"description": "Camiseta confortável de algodão",
		"details": {
			"color": "AZUL",
			"id": 1,
			"size": "M",
			"stock": 100
		},
		"id": 1,
		"image": "http://exemplo.com/imagens/camiseta.jpg",
		"price": 60.0,
		"product": {
			"category": {
				"id": 1,
				"name": "Roupas"
			},
			"id": 1,
			"name": "Camiseta"
		},
		"seller": {
			"companyName": "Distribuicão de alimentos divinos",
			"fantasyName": "João da Loja",
			"image": "http://exemplo.com/imagens/mercearia_joao.jpg",
			"sellerId": 1,
			"userId": 1
		},
		"title": "Camiseta Básica Azul"
	}
]
```

## 2. Obter produtos específico do catálogo
 - Rota: /products/<int:id>
 - Método: GET
 - Descrição: Retorna o produtos especifico requisitado,
incluindo informações detalhadas sobre categoria, vendedor e variações do produto.
 - Exemplo de Resposta:
 ```
{
	"careLevel": "BAIXO",
	"description": "Camiseta confortável de algodão",
	"details": [
		{
			"color": "AZUL",
			"id": 1,
			"size": "M",
			"stock": 100
		}
	],
	"id": 1,
	"image": "http://exemplo.com/imagens/camiseta.jpg",
	"price": 60.0,
	"product": {
		"category": {
			"id": 1,
			"name": "Roupas"
		},
		"id": 1,
		"name": "Camiseta"
	},
	"seller": {
		"companyName": "Distribuicão de alimentos divinos",
		"fantasyName": "João da Loja",
		"image": "http://exemplo.com/imagens/mercearia_joao.jpg",
		"sellerId": 1,
		"userId": 1
	},
	"title": "Camiseta Básica Azul"
}
```

## 3. Obter produtos específico do catálogo
 - Rota: /products/category
 - Método: GET
 - Descrição: Retorna todos os produtos cadastrados pelos vendedores agrupados por categorias,
incluindo informações detalhadas sobre categoria, vendedor e variações do produto.
 - Query (opcional): Retorna os produtos da categoria especificada
 - Exemplo de query
  {
  name: 'Roupas'
  }
 - Exemplo de Resposta:
 ```
[
	{
		"id": 1,
		"name": "Roupas",
		"products": [
			{
				"careLevel": "BAIXO",
				"description": "Camiseta confortável de algodão",
				"details": [
					{
						"color": "AZUL",
						"id": 1,
						"size": "M",
						"stock": 100
					}
				],
				"id": 1,
				"image": "http://exemplo.com/imagens/camiseta.jpg",
				"price": 60.0,
				"seller": {
					"companyName": "Distribuicão de alimentos divinos",
					"fantasyName": "João da Loja",
					"image": "http://exemplo.com/imagens/mercearia_joao.jpg",
					"sellerId": 1,
					"userId": 1
				},
				"title": "Camiseta Básica Azul"
			}
		]
	}
]
```

## 4. Obter todos os pedidos de um cliente
 - Rota: /orders/client/<int:id>
 - Método: GET
 - Descrição: Retorna todos os pedidos realizados por um cliente,
incluindo informações detalhadas sobre categoria, vendedor e variações do produto.
 - Exemplo de Resposta:
 ```
[
	{
		"completeDate": "Sat, 13 Sep 2025 12:32:25 GMT",
		"createdAt": "Sat, 13 Sep 2025 15:32:25 GMT",
		"id": 1,
		"paymentMethod": "PIX",
		"products": [
			{
				"careLevel": "BAIXO",
				"description": "Camiseta confortável de algodão",
				"details": [
					{
						"color": "AZUL",
						"id": 1,
						"size": "M",
						"stock": 100
					}
				],
				"id": 1,
				"image": "http://exemplo.com/imagens/camiseta.jpg",
				"price": 60.0,
				"product": {
					"category": {
						"id": 1,
						"name": "Roupas"
					},
					"id": 1,
					"name": "Camiseta"
				},
				"quantity": 2,
				"seller": {
					"companyName": "Distribuicão de alimentos divinos",
					"fantasyName": "João da Loja",
					"image": "http://exemplo.com/imagens/mercearia_joao.jpg",
					"sellerId": 1,
					"userId": 1
				},
				"title": "Camiseta Básica Azul"
			}
		],
		"status": "COMPLETED",
		"totalPrice": 120.0
	}
]
```

## 5. Obter um pedido especifico
 - Rota: /orders/<int:id>
 - Método: GET
 - Descrição: Retorna todas as informacões do pedido em especifico,
incluindo informações detalhadas sobre categoria, vendedor e variações do produto.
 - Exemplo de Resposta:
 ```
{
	"clientId": 1,
	"completeDate": "Sat, 13 Sep 2025 12:32:25 GMT",
	"createdAt": "Sat, 13 Sep 2025 15:32:25 GMT",
	"orderId": 1,
	"products": [
		{
			"brand": "Genérica",
			"details": [
				{
					"color": "AZUL",
					"size": "M",
					"stock": 100
				}
			],
			"id": 1,
			"price": 60.0,
			"quantity": 2,
			"seller": {
				"companyName": "Distribuicão de alimentos divinos",
				"fantasyName": "João da Loja",
				"image": "http://exemplo.com/imagens/mercearia_joao.jpg",
				"sellerId": 1,
				"userId": 1
			},
			"title": "Camiseta Básica Azul"
		}
	]
}
```

## 6. Atualizar o pedido específico
 - Rota: /orders/<int:order_id>
 - Método: PUT
 - Descrição: Atualiza o status e as informações de pagamento um pedido existente.
 - Exemplo de Entrada:
 ```
{
	"status": "ON GOING",
	"paymentMethod": "PIX"
}
 ```
 - Exemplo de Resposta:
 ```
{
	"message": "Pedido atualizado com sucesso",
	"orderId": 2
}
```

## 7. Obter o carrinho de uma pessoa
 - Rota: /cart/client/<int:client_id>
 - Método: GET
 - Descrição: Retorna o carrinho de um cliente com seus produtos,
incluindo informações detalhadas sobre categoria, vendedor e variações do produto.
 - Exemplo de Resposta:
 ```
{
	"clientId": 1,
	"createdAt": "Sat, 13 Sep 2025 18:33:28 GMT",
	"orderId": 2,
	"products": [
		{
			"brand": "Bosch",
			"details": [
				{
					"color": "AMARELO",
					"size": null,
					"stock": 20
				}
			],
			"id": 2,
			"price": 20.0,
			"quantity": 1,
			"seller": {
				"companyName": "Distribuicão de ferramentas pau pra toda obra",
				"fantasyName": "Alexandre das Ferramentas",
				"image": "http://exemplo.com/imagens/ferramentas_alexandre.jpg",
				"sellerId": 2,
				"userId": 2
			},
			"title": "Chave de Fenda Magnética"
		}
	],
	"totalPrice": 20.0,
	"userId": 3
}
```

## 8. Atualizar o carrinho de uma pessoa
 - Rota: /cart/client/<int:client_id>
 - Método: PUT
 - Descrição: Atualiza o carrinho de um cliente com base nos produtos enviados e em caso de não existir ele cria o carrinho.
 - Exemplo de Entrada:
 ```
[
	{
		"seller_product_id": 1, 
		"quantity": 3
	}
]
 ```
 - Exemplo de Resposta:
 ```
{
	"message": "Carrinho atualizado com sucesso",
	"orderId": 3
}
```

## 9. Obter o carrinho de uma pessoa
 - Rota: /cart/<int:order_id>/product/<int:product_id>
 - Método: DELETE
 - Descrição: Retira o produto especificado do carrinho especificado
 - Exemplo de Resposta:
 ```
{
	"message": "Produto removido"
}
```

## 10. Obter um cliente especefico
 - Rota: /client/<int:client_id>
 - Método: GET
 - Descrição: Retorna um cliente específico,
incluindo informações detalhadas sobre cartões cadastrados.
 - Exemplo de Resposta:
 ```
{
	"address": "Rua B, 456",
	"cards": [],
	"clientId": 1,
	"document_path": null,
	"identifier": "98765432100",
	"image": "http://exemplo.com/imagens/maria_compradora.jpg",
	"name": "Maria Compradora",
	"phone": "11988888888",
	"userId": 3
}
```

## 11. Obter todas as categorias
 - Rota: /categories
 - Método: GET
 - Descrição: Retorna todas as categorias cadastadas no sistema
 - Exemplo de Resposta:
 ```
[
	{
		"icon": "http://exemplo.com/icons/roupa.jpg",
		"id": 1,
		"name": "Roupas"
	}
]
```