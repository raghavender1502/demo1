"""
FastAPI implementation.
"""

from fastapi import FastAPI, APIRouter
from .ssllist import newScan


router = APIRouter()
@router.get("/ssl_old")
def GetSSLInfo(domain:str):
    data = newScan(domain)
    return data
