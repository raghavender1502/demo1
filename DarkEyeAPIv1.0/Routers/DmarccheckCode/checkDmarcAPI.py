"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .checkDmarcMain import get_dmarc_records


#######################-->FastAPI<--##################################
router = APIRouter()


@router.get('/checkDMARC')
def GetDmarcRecords(domain:str):
    data= get_dmarc_records(domain)
    return data
