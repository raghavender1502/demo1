"""
FastAPI implementation.
"""

from fastapi import FastAPI, APIRouter
from .DnsThreatsCombine import test


router = APIRouter()
@router.get("/dnsthreats")
def GetSSLInfo(domain:str):
    data = test(domain)
    return data
