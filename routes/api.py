from fastapi import APIRouter
from endpoints import contrato

router = APIRouter()
router.include_router(contrato.router)
