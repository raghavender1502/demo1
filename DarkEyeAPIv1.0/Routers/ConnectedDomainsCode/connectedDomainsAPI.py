"""
FastAPI implementation.
"""

from fastapi import FastAPI, APIRouter
from .connectedDomainsMain import extract


router = APIRouter()
@router.get("/connecteddomains")
def GetConnectedDomains(domain:str):
    data = extract(domain)
    return data
