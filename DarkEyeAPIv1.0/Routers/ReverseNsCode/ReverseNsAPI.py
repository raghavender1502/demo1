"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .ReverseNsMain import ReverseNs


#######################-->FastAPI<--##################################
router = APIRouter()

@router.get('/reversens')
def GetReverseNs(domain:str):
    data= ReverseNs(domain)
    return data