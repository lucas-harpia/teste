from fastapi import Depends, APIRouter
from models.contrato import Contrato
from auth.token import authenticate_token
import base64
import os


router = APIRouter(tags=['contrato'], responses={
                   404: {"description": "Not found"}})


@router.get("/contrato", dependencies=[Depends(authenticate_token)])

async def read_contrato():

    with open(os.getenv("LOGO"), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    contratoLogo = f"data:image/png;base64,{encoded_string}"

    contrato = Contrato(
        versao_protocolo=os.getenv("VERSAO_PROTOCOLO"),
        nome=os.getenv("NOME"),
        referencia=os.getenv("REFERENCIA"),
        tipo=os.getenv("TIPO"),
        logo=contratoLogo,
        descricao=os.getenv("DESCRICAO"),
        consultas=[
            {
                "nome": "Buscar dados de pessoa.",
                "url": "biografia",
                "descricao": "Dados biográficos de Pessoa",
                "filtros": [
                    {
                        "url": "cpf",
                        "instrucao": "Digite um cpf de pessoa que deseja encontrar",
                        "atributos": [
                            {
                                "rotulo": "Cpf",
                                "chave": "cpf",
                                "tipo": "1",
                                "mascara": ""
                            }
                        ]
                    }

                ]
            }
        ]
    )
    return contrato
