## Descrição 
Web crawler construído para buscar registros por localidade e faixas de CEP disponíveis no seguinte endereço: https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm

## Funcionamento
O crawler inicialmente faz um GET request e armazena os cookies retornados em uma sessão. A partir da sessão iniciada, ele busca quais UFs estão disponíveis dentro do elemento HTML ``` <select name="UF" class="f1col">...</option> ``` e coloca em uma lista que será iterada para buscar os registros. A tabela retorna 50 registros por vez. Na primeira request o crawler identifica o número total de linhas para trazer os registros de faltam.


![Crawler em funcionamento](https://media.giphy.com/media/qWX19kqpdMbxKd84MM/giphy.gif)


## Critérios utilizados
Para não haver registros duplicados, o critério utilizado foi buscar as faixas de CEP de cada localidade que possuem escrito "Total do município" na coluna **Tipo de Faixa**
###### Exemplo mostrando dados duplicados:
![tabela de exemplo com registros duplicados](https://i.ibb.co/6HBLCjy/Screen-Shot-2022-05-19-at-20-20-28.png)

Na imagem acima, temos a localidade "Arapiraca" repetindo duas vezes. Utilizando o critério de deduplicação de dados, o crawler utilizar o registro da **terceira linha** que contem a faixa de CEP **57300-001 a 57319-999**

## Instalação

## 1 - Clonar repositório
```
git clone https://github.com/codeis4fun/correiosWebCrawler.git
```
## 2 - Criar ambiente virtual
```
python3 -m venv venv
```
## 3 - Acessar ambiente virtual criado
```
source venv/bin/activate
```
## 4 - Instalar bibliotecas necessárias
```
pip install -r requirements.txt
```

## 5 - Buscar registros e armazenar no arquivo final output.jsonl
```
python buscaCEP.py
```

## Testes unitários

```
python -m unittest test_buscaCEP.py
```
