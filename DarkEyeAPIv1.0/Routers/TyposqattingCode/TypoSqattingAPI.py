"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .TypoSqattingDB import TyposqattinChecks


#######################-->FastAPI<--##################################
router = APIRouter()

@router.get('/typosquatting')
def GetTyposqatting(domain:str):
    #Getting the data from the mxblacklistchecker script
    data= TyposqattinChecks(domain)
    #print(data)
    return data
