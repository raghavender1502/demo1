"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .ReverseMxMain import ReverseMx


#######################-->FastAPI<--##################################
router = APIRouter()


@router.get('/reversemx')
def GetReverseMx(domain:str):
    data= ReverseMx(domain)
    return data
