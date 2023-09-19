"""
FastAPI implementation.
"""

from fastapi import FastAPI, APIRouter
from .BannerGrabbing import banner_grabbing


#######################-->FastAPI<--##################################
router = APIRouter()


@router.get('/banner_grabbing')
def Getbanner_grabbing(domain:str):
    data= banner_grabbing(domain)
    return data