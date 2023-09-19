"""
FastAPI implementation.
"""

from asyncio import run_coroutine_threadsafe
from fastapi import FastAPI,APIRouter
#from .AssetInventryThreatsDB import AssetInventryChecks
from .AssetInvThreatsMain import assetsInventory

#######################-->FastAPI<--##################################
router = APIRouter()

@router.get('/assetinventorythreats')
def GetAssetInventryThreats(domain:str):
    data= assetsInventory(domain)
    return data
