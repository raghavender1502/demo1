"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .httpHeadersMain import function


#######################-->FastAPI<--##################################
router = APIRouter()


@router.get('/httpHeaders')
def GetReverseMx(domain:str):
    data= function(domain)
    return data
