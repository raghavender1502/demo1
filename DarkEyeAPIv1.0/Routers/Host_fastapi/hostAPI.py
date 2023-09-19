"""
FastAPI implementation.
"""

from fastapi import FastAPI,APIRouter
from .host import get_Host


#######################-->FastAPI<--##################################
#app = FastAPI()
router = APIRouter()
@router.get('/host_ip')
def Get_host(domain:str):
    data= get_Host(domain)
    return data

