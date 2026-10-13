# API de Livros

# GET, POST, PUT, DELETE

# POST - Adicionar novos livros (Create)
# GET - Buscar os dados dos livros (Read)
# PUT - Atualizar informações dos livros (Update)
# DELETE - Deletar informações dos livros (Delete)

# CRUD
# CREATE
# READ
# UPDATE
# DELETE

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import secrets

app = FastAPI(
    title='API de Livros',
    description='API para gerenciar catálogo de livros',
    version='1.0.0',
    contact={
        'name': 'Atilio Hector',
        'email': 'thehacktour@gmail.com'
    }
)

MEU_USUARIO = 'admin'
MINHA_SENHA = 'admin'

security = HTTPBasic()

livros = {}


class Livro(BaseModel):
    nome_livro: str
    autor_livro: str
    ano_livro: int


def autenticar_meu_usuario(
    credentials: HTTPBasicCredentials = Depends(security)
):
    is_username_correct = secrets.compare_digest(
        credentials.username, MEU_USUARIO
    )

    is_password_correct = secrets.compare_digest(
        credentials.password, MINHA_SENHA
    )

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail='Usuário ou senha incorretos',
            headers={'WWW-Authenticate': 'Basic'}
        )


@app.get('/livros')
def get_livros(
    page: int = 1, limit: int = 10, credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page ou Limit estao com valores invalidos!!!")

    if not livros:
        return {'message':'Nao existe nenhum livro!'}

    start = (page - 1) * limit
    end = start + limit

    livros_paginados = [
        {'id': id_livro, 'nome_livro': livro_data['nome_livro'], 'autor_livro': livro_data['autor_livro'], "ano_livro":livro_data['ano_livro']}
        for id_livro, livro_data in list(livros.items())[start:end]
    ]

    return{
        'page': page,
        'limit': limit,
        'total': len(livros),
        'livros': livros_paginados
    }

@app.post('/adiciona')
def post_livros(
    id_livro: int,
    livro: Livro,
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    if id_livro in livros:
        raise HTTPException(
            status_code=400,
            detail='Esse livro já existe!'
        )

    livros[id_livro] = livro.model_dump()

    return {'message': 'O livro foi criado com sucesso!'}


@app.put('/atualiza/{id_livro}')
def put_livros(
    id_livro: int,
    livro: Livro,
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    if id_livro not in livros:
        raise HTTPException(
            status_code=404,
            detail='Esse livro não foi encontrado!'
        )

    livros[id_livro] = livro.model_dump()

    return {
        'message': 'As informações do seu livro foram atualizadas com sucesso!'
    }


@app.delete('/deletar/{id_livro}')
def delete_livro(
    id_livro: int,
    credentials: HTTPBasicCredentials = Depends(autenticar_meu_usuario)
):
    if id_livro not in livros:
        raise HTTPException(
            status_code=404,
            detail='Esse livro não foi encontrado!'
        )

    del livros[id_livro]

    return {'message': 'Seu livro foi deletado com sucesso!'}