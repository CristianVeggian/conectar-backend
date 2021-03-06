from fastapi import HTTPException
from sqlalchemy.orm import Session
import typing as t

from app.db import models
from app.db.pessoa import schemas

def get_pessoa_by_name(
    db: Session,
    pessoa_name: str,
    area_id: int
    ) -> t.List[schemas.Pessoa]:

    '''
        Busca todas as Pessoas cujo nome contenha a string buscada

        Entrada: string

        Saída: Lista de Esquemas da Pessoa correspondente

        Exceções: Não existe Pessoa correspondente à string inserida
    '''

    if not area_id:
        pessoa = db.query(models.Pessoa)\
            .filter(models.Pessoa.nome.ilike(f'%{pessoa_name}%'))\
            .all()
    else:
        pessoa = db.query(models.Pessoa)\
            .join(models.Area, models.Pessoa.areas)\
            .filter(models.Pessoa.nome.ilike(f'%{pessoa_name}%'))\
            .filter(models.Area.id == area_id)\
            .all()

    return pessoa

def get_pessoa_by_username(
    db: Session,
    pessoa_usuario: str
    ) -> t.List[schemas.Pessoa]:

    '''
        Busca todas as Pessoas cujo usuario contenha a string buscada

        Entrada: string

        Saída: Lista de Esquemas da Pessoa correspondente

        Exceções: Não existe Pessoa correspondente à string inserida
    '''

    pessoa = db.query(models.Pessoa)\
        .filter(models.Pessoa.usuario.ilike(f'%{pessoa_usuario}%'))\
        .all()

    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")

    return pessoa


def get_pessoa_by_area(
    db: Session,
    pessoa_area: str
    ) -> t.List[schemas.Pessoa]:
    
    '''
        Busca todas as Pessoas que contenham uma área com a string buscada

        Entrada: string

        Saída: Lista de Esquemas da Pessoa correspondente

        Exceções: Não existe Pessoa correspondente à string inserida
    '''
    
    pessoa = db.query(models.Pessoa)\
        .join(models.Area, models.Pessoa.areas)\
        .filter(models.Area.descricao.ilike(f'%{pessoa_area}%'))\
        .all()
    
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")

    return pessoa

def get_pessoa_by_habilidade(
    db: Session,
    pessoa_habilidade: str
    ) -> t.List[schemas.Pessoa]:

    '''
        Busca todas as Pessoas que contenham uma habilidade com a string buscada

        Entrada: string

        Saída: Lista de Esquemas da Pessoa correspondente

        Exceções: Não existe Pessoa correspondente à string inserida
    '''

    pessoa = db.query(models.Pessoa)\
        .join(models.Habilidades, models.Pessoa.habilidades)\
        .filter(models.Habilidades.nome.ilike(f'%{pessoa_habilidade}%'))\
        .all()
    
    if not pessoa:
        raise HTTPException(status_code=404, detail="pessoa não encontrado")

    return pessoa
