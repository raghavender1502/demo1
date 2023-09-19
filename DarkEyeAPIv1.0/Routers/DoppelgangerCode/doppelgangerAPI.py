"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .doppelgangerSimple import getDoppelgangerDomains

#######################-->FastAPI<--##################################
router = APIRouter()

@router.get('/doppelgangerdomains')
def GetDoppelgangerDomains(domain:str):
    data = getDoppelgangerDomains(domain)
    return data