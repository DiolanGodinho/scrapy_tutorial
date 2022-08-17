# Projeto Inicial de Scrapy

Projeto para obter citações de pessoas famosas registradas no endereço http://quotes.toscrape.com/.

São obtidos as citações, seus autores e as *tags* associadas.

As informações são armazenadas automaticamente em um banco de dados do *postgres* por meio da biblioteca ```psycopg2```.

Para ter acesso ao postgres é necessário criar o arquivo ```database.ini``` contendo as credenciais de acesso:

```
[postgres]

host=your_host
database=database_name
user=postgres_user
password=user_password
```
