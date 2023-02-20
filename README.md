## API Criação de um "Modelo de Banco" para Curso da DIO
### Criei segundo o que eu gostaria.

- Estrutura da API

api/
|---main.py
|---models/
|   |---client.py
|---schemas/
|   |---client.py
|---routers/
|   |---client.py
|---database/
|   |---database.py
|   |---models.py
|---static/
|   |---index.html
|   |---styles.css
|   |---script.js


- O arquivo main.py será o ponto de entrada da aplicação, onde iniciaremos a aplicação FastAPI e definiremos as configurações do servidor.
- O diretório models conterá os modelos de dados utilizados pela aplicação.
- O diretório schemas conterá os esquemas de dados que serão utilizados na API.
- O diretório routers conterá os endpoints da API.
- O diretório database conterá os arquivos relacionados à configuração e acesso ao banco de dados.
- O diretório static conterá os arquivos estáticos utilizados na interface web.

### Como utilizar o Docker

### Subindo o docker

Primeiro monte a imagem da api na sua máquina:
(repita essa etapa se atualizar o requirements.txt)

> docker build -t banco_api ./docker

Para rodar a api "containerizada" (Linux):

> docker run -v $(pwd):/app -p 8000:8000 --rm -it --env-file ./.env --name banco_api banco_api

Para rodar a api "containerizada" (Windows):

> docker run -v C:\2_courses\2_courses\DIO\banco_api:/app -p 8000:8000 --rm -it --name banco_api banco

Configuração de dependências PostgreSQL:

> docker run --name postgresql -e POSTGRES_PASSWORD=root -e POSTGRES_USER=root -e POSTGRES_DB banco_api -p 5432:5432 -v $(pwd)/pgdata:/var/lib/postgresql/data -d postgres

Configuração de dependências PgAdmin:

> docker run --name pgadmin -e PGADMIN_DEFAULT_PASSWORD=root -e PGADMIN_DEFAULT_EMAIL=root@root.com -p 5050:80 --link postgresql:pgsql -d dpage/pgadmin4

Inspect docker

> docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgresql

Note que a configuração do contêiner do PostgreSQL inclui o nome do banco de dados e um volume compartilhado para persistir os dados do banco. Além disso, a configuração do contêiner do PgAdmin inclui um link para o contêiner do PostgreSQL."# banco_api_fastAPI" 
"# banco_api_fastAPI" 


