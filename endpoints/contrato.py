from fastapi import Depends, APIRouter
from models.contrato import Contrato
from auth.token import authenticate_token
import base64
import os


router = APIRouter(tags=['contrato'], responses={
                   404: {"description": "Not found"}})


@router.get("/contrato/cnpj", dependencies=[Depends(authenticate_token)])

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
                "nome": "Buscar dados de um Estabelecimento.",
                "url": "busca",
                "descricao": "Dados biográficos de um Estabelecimentdo.",
                "filtros": [
                    {
                        "url": "estabelecimento",
                        "instrucao": "Digite o CNPJ do estabelecimento que deseja encontrar",
                        "atributos": [
                            {
                                "rotulo": "CNPJ",
                                "chave": "cnpj",
                                "tipo": "3",
                                "mascara": ""
                            }
                        ]
                    },
                    {
                        "url": "nomefantasia",
                        "instrucao": "Digite o Nome Fantasia do Estabelecimento que deseja encontrar",
                        "atributos": [
                            {
                                "rotulo": "Nome Fantasia",
                                "chave": "nme_fan",
                                "tipo": "2",
                                "mascara": ""
                            }
                        ]
                    }
                ]
            },
            {
                "nome": "Buscar dados de uma Empresa.",
                "url": "busca",
                "descricao": "Dados biográficos de uma Empresa.",
                "filtros": [
                    {
                        "url": "empresa",
                        "instrucao": "Digite o CNPJ da empresa que deseja encontrar",
                        "atributos": [
                            {
                                "rotulo": "CNPJ",
                                "chave": "cnpj",
                                "tipo": "3",
                                "mascara": ""
                            }
                        ]
                    },
                    {
                        "url": "razao",
                        "instrucao": "Digite a Razão Social da empresa que deseja encontrar",
                        "atributos": [
                            {
                                "rotulo": "Razão Social",
                                "chave": "rzao",
                                "tipo": "2",
                                "mascara": ""
                            }
                        ]
                    }
                ]
            },
            {
                "nome": "Buscar dados de uma Pessoa(Sócio).",
                "url": "busca",
                "descricao": "Dados biográficos de uma Pessoa(Sócio).",
                "filtros": [
                    {
                        "url": "socio",
                        "instrucao": "Digite o CNPJ da pessoa que deseja encontrar",
                        "atributos": [
                            {
                                "rotulo": "CNPJ",
                                "chave": "cnpj",
                                "tipo": "3",
                                "mascara": ""
                            }
                        ]
                    },
                    {
                        "url": "nome",
                        "instrucao": "Digite o Nome da Pessoa que deseja encontrar",
                        "atributos": [
                            {
                                "rotulo": "Nome",
                                "chave": "nme",
                                "tipo": "2",
                                "mascara": ""
                            }
                        ]
                    }
                ]
            }
        ]
    )
    return contrato
