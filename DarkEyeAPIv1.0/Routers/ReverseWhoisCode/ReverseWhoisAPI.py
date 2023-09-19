"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .ReverseWhoisScript import GetReverseWhoIsData


#######################-->FastAPI<--##################################
router = APIRouter()


@router.get('/reversewhois')
def GetReverseMx(domain:str):
    data= GetReverseWhoIsData(domain)
    return data
