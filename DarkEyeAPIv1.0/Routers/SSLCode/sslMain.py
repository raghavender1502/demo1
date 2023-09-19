from fastapi import  APIRouter
import os
from dotenv import load_dotenv
import shlex
import subprocess

load_dotenv()
ssl_process_path = os.getenv("SSLMicroServicePath")

router = APIRouter()

@router.get("/ssl")
async def root(domain:str, scan_id:int):
    
    cmd = f'python {ssl_process_path} {domain} {scan_id}'
    print(cmd)
    cmds = shlex.split(cmd)
    p = subprocess.Popen(cmds, start_new_session=True)

    doc = {
        "domain": domain,
        "status": "inprogress",
        "ssl_lists":[],
        "ssl_threats":[],
        "statusMessage": "The scan is in progress, please be patient until the scan is completed.",
        "statusCode": 202,
    }
    return doc
