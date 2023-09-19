"""
FastAPI implementation.
"""

from fastapi import FastAPI, APIRouter
from .sslyzerMain import sslyze_scan


router = APIRouter()
@router.get("/sslyzer")
def GetSSLInfo(domain:str):
    data = sslyze_scan(domain)
    return data
