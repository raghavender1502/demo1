"""
FastAPI implementation.
"""
from fastapi import  APIRouter
import os
from dotenv import load_dotenv
import shlex
import subprocess

load_dotenv()
openports_process_path = os.getenv("OpenportsMicroServicePath")

router = APIRouter()

@router.get("/openports")
async def root(domain:str, scan_id:int):
    
    cmd = f'python {openports_process_path} {domain} {scan_id}'
    print(cmd)
    cmds = shlex.split(cmd)
    p = subprocess.Popen(cmds, start_new_session=True)

    doc = {
        "domain": domain,
        "status": "inprogress",
        "statusMessage": "The scan is in progress, please be patient until the scan is completed.",
        "statusCode": 202,
        "response":{"response":[],"threats":{}}
    }
    return doc