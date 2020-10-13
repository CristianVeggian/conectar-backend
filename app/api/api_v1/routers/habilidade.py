from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.habilidade.crud import (
    get_habilidades,
    create_habilidades,
    get_habilidades_by_id,
    edit_habilidades,
    delete_habilidades,
    get_habilidade_by_name
)
from app.db.habilidade.schemas import (
    HabilidadesCreate,
    Habilidades,
    HabilidadesEdit
)
from app.core.auth import (
    get_current_active_pessoa,
    get_current_active_superuser,
)

habilidades_router = r = APIRouter()

@r.get(
    "/habilidades/",
    response_model=t.List[Habilidades],
    response_model_exclude_none=True,
)
async def habilidades_list(
    response: Response,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all habilidades
    """
    habilidades = get_habilidades(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(habilidades)}"
    return habilidades

@r.get(
    "/habilidade/name/{habilidades_name}",
    response_model=Habilidades,
    response_model_exclude_none=True,
)
async def habilidades_details_name(
    request: Request,
    habilidades_name: str,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any habilidades details by its name
    """
    habilidades = await get_habilidade_by_name(db, habilidades_name)
    return habilidades 

@r.post(
    "/habilidade/pessoa",
    response_model=Habilidades,
    response_model_exclude_none=True,
)
async def habilidades_create(
    request: Request,
    habilidades: HabilidadesCreate,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Create a new habilidade 
    """
    return create_habilidades(db, habilidades, current_pessoa.id)

@r.put(
    "/habilidades/pessoa/{habilidade_id}",
    response_model=Habilidades,
    response_model_exclude_none=True,
)
async def habilidade_edit(
    request: Request,
    habilidades_id: int,
    habilidades: Habilidades,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Update existing habilidade
    """
    return edit_habilidades(db, habilidades_id, habilidades)

@r.delete(
    "/habilidade/pessoa/{habilidade_id}",
    response_model=Habilidades,
    response_model_exclude_none=True,
)
async def habilidade_pessoa_delete(
    request: Request,
    habilidade_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
        Delete existing habilidade
    """
    return delete_habilidades(db, habilidade_id)


    