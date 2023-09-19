"""
FastAPI implementation.
"""

from asyncio import run_coroutine_threadsafe
from fastapi import FastAPI,APIRouter
from .KnownSubdomains import KnownSubdomainsChecks


#######################-->FastAPI<--##################################
router = APIRouter()

@router.get('/knownsubdomains')
def GetKnownSubDomains(domain:str):
    #Getting the data from the mxblacklistchecker script
    data= KnownSubdomainsChecks(domain)
    return data
