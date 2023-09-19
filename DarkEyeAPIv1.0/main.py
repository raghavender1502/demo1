from Routers.KnownSubdomainsCode import knownsubdomainsapi
from Routers.TyposqattingCode import TypoSqattingAPI
from Routers.AssetInventryThreatsCode import AssetInventryAPI
#from Routers.GitHubSecretCode import GitHubSecretAPI
from Routers.DoppelgangerCode import doppelgangerAPI
from Routers.ReverseMxCode import ReverseMxAPI
from Routers.ReverseNsCode import ReverseNsAPI
from Routers.WebsiteScreenshot import WebsiteScreenshotAPI
from Routers.SSLCode_old import ssl_API
from Routers.SSLyzerCode import sslyzerAPI
from Routers.OpenportsCode import openPortsMain
from Routers.BannerGrabbingCode import BannerAPI
from Routers.HttpHeadersCode import httpHeardersAPI
from Routers.DmarccheckCode import checkDmarcAPI
from Routers.DNSThreatsCode import DnsThreatsAPI
from Routers.ConnectedDomainsCode import connectedDomainsAPI
from Routers.SSLCode import sslMain
from Routers.ReverseWhoisCode import ReverseWhoisAPI
from Routers .Host_fastapi import hostAPI
from fastapi import FastAPI,APIRouter

app = FastAPI()

app.include_router(knownsubdomainsapi.router)
app.include_router(TypoSqattingAPI.router)
app.include_router(AssetInventryAPI.router)
app.include_router(DnsThreatsAPI.router)
app.include_router(connectedDomainsAPI.router)
#app.include_router(GitHubSecretAPI.router)
app.include_router(ReverseMxAPI.router)
app.include_router(doppelgangerAPI.router)
app.include_router(ReverseNsAPI.router)
app.include_router(WebsiteScreenshotAPI.router)
app.include_router(ssl_API.router)
app.include_router(sslyzerAPI.router)
app.include_router(openPortsMain.router)
app.include_router(BannerAPI.router)
app.include_router(httpHeardersAPI.router)
app.include_router(checkDmarcAPI.router)
app.include_router(ReverseWhoisAPI.router)
app.include_router(sslMain.router)
app.include_router(hostAPI.router)
@app.get("/")
async def root():
    return {"message": "Welcome to DarkEye API "}
