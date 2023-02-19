from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from routers.client import router as client_router

app = FastAPI()

app.include_router(client_router, prefix="/clients", tags=["clients"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
        <html>
            <head>
                <title>API do Banco XYZ</title>
                <link rel="stylesheet" href="/static/styles.css">
            </head>
            <body>
                <h1>Bem-vindo(a) à API do Banco XYZ!</h1>
                <p>Para começar, acesse <a href="/docs">/docs</a> para ver a documentação da API.</p>
                <p>Também é possível acessar a interface da API em <a href="/static/index.html">/static/index.html</a>.</p>
                <script src="/static/script.js"></script>
            </body>
        </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

