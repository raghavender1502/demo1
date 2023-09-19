
from fastapi import FastAPI, APIRouter
from .GitHubSecretDBORG import GitHubSecretOrgChecks
from .GitHubSecretDBDomain import GitHubSecretDomainChecks
router= APIRouter()

@router.get("/githubsecret/organization")
def Get_Secret_Organization(org:str):
    data= GitHubSecretOrgChecks(org)
    return data
@router.get("/githubsecret/domain")
def Get_Secret_Organization(domain:str):
    data = GitHubSecretDomainChecks(domain)
    #get_Github_api_Remaining_Credit()
    return data