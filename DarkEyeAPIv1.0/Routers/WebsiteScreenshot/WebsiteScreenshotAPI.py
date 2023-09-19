import imp
from fastapi import FastAPI, Path, APIRouter
from fastapi.responses import HTMLResponse

from fastapi.responses import FileResponse

from PIL import Image
import datetime
import requests
from dotenv import load_dotenv
from pathlib import Path
import os

#get apikey
load_dotenv()
#env_path= Path(".")/"."
#load_dotenv(dotenv_path=env_path)
apikey=os.getenv("WhoisAPI")

screenshotdir = os.getenv("ScreenshotDir")
router = APIRouter()

@router.get("/websitescreenshot/", response_class=HTMLResponse)
def read_items(target):
    img = Image.open(requests.get('https://website-screenshot.whoisxmlapi.com/api/v1?apiKey='+apikey+'&url='+target+'&credits=DRS&width=1920&height=1080&scale8.0&delay=1500', stream=True).raw)
    x = target.split('.')[0]

    now = datetime.datetime.now()
    screenshot = f"{x}"+str(now.strftime("%Y-%m-%d-%H-%M-%S"))+'.jpg'
    Img=img.save(screenshotdir+screenshot)

    return FileResponse(screenshotdir+screenshot)
