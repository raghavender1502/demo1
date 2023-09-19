
try:

    import requests
    from truffleHog import truffleHog
    import re
    from json import loads
    
    import json
    from tld import get_tld
    
    def get_Github_api_Remaining_Credit():
        response = requests.get(url='https://api.github.com/rate_limit')
        json = response.json()
        
        print("Remaining Github search API credit are ", json['resources']['search']['remaining'])



    
    github_repo_org = set()

    
    def get_org_repos(orgname, page):
        response = requests.get(url='https://api.github.com/users/' + orgname + '/repos?page={}'.format(page))

        json = response.json()
        
        if not json:
            return None
        if isinstance(json,dict) :
            return None
        for item in json:
            


            if item['fork'] == False:
                github_repo_org.add(item["html_url"])
                
                
            
                
        get_org_repos(orgname, page + 1)


   


    rules = {
        "Slack Token": "(xox[p|b|o|a]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
        "RSA private key": "-----BEGIN RSA PRIVATE KEY-----",
        "SSH (OPENSSH) private key": "-----BEGIN OPENSSH PRIVATE KEY-----",
        "SSH (DSA) private key": "-----BEGIN DSA PRIVATE KEY-----",
        "SSH (EC) private key": "-----BEGIN EC PRIVATE KEY-----",
        "PGP private key block": "-----BEGIN PGP PRIVATE KEY BLOCK-----",
        "Facebook Oauth": "[f|F][a|A][c|C][e|E][b|B][o|O][o|O][k|K].{0,30}['\"\\s][0-9a-f]{32}['\"\\s]",
        "Twitter Oauth": "[t|T][w|W][i|I][t|T][t|T][e|E][r|R].{0,30}['\"\\s][0-9a-zA-Z]{35,44}['\"\\s]",
        "GitHub": "[g|G][i|I][t|T][h|H][u|U][b|B].{0,30}['\"\\s][0-9a-zA-Z]{35,40}['\"\\s]",
        "Google Oauth": "(\"client_secret\":\"[a-zA-Z0-9-_]{24}\")",
        "AWS API Key": "AKIA[0-9A-Z]{16}",
        "Heroku API Key": "[h|H][e|E][r|R][o|O][k|K][u|U].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
        "Generic Secret": "[s|S][e|E][c|C][r|R][e|E][t|T].{0,30}['\"\\s][0-9a-zA-Z]{32,45}['\"\\s]",
        "Generic API Key": "[a|A][p|P][i|I][_]?[k|K][e|E][y|Y].{0,30}['\"\\s][0-9a-zA-Z]{32,45}['\"\\s]",
        "Slack Webhook": "https://hooks.slack.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
        "Google (GCP) Service-account": "\"type\": \"service_account\"",
        "Twilio API Key": "SK[a-z0-9]{32}",
        "Password in URL": "[a-zA-Z]{3,10}://[^/\\s:@]{3,20}:[^/\\s:@]{3,20}@.{1,100}[\"'\\s]",
        "SlackInternal": "slack-corp",
        # "PDF":"[.][P|p][D|d][F|f]"
        # "pdf": ".pdf"
    }

    for key in rules:
        rules[key] = re.compile(rules[key])

    github_repo_by_githubapi = set()
    
    
    ''' findallkeywords will find all repo related to keyword 
        This fun take 3 argument 
        1) keyword: take string for searching
        2) pageno : after we call github api it gives data in pages so we have pass default value 1 so we get data from first page upto remaining pages
        3) limit : here we can set limit for no of github repo we need , max 1000 as github only gives 1000 repo in 1 min . 
    '''
    try:
        def findallkeywords(keyword,pageno,limit):
                response = requests.get(url="https://api.github.com/search/repositories?q="+keyword+"&page="+str(pageno)+"&per_page=100")
                json = response.json()
                if "message" in json:
                    raise Exception('GitApi Credit', 'Exhusted please try after 1 min')
                    return None
                
                
                if len(json["items"])==0:
                    return None
                
                for item in json["items"]:
                
                    if len(github_repo_by_githubapi)>=limit :
                        return None;

                    github_repo_by_githubapi.add(item["html_url"])
                findallkeywords(keyword,pageno+1,limit);
    except:
        print("github api error")

    
    def findSecrets(gitRepo):
        results = truffleHog.find_strings(gitRepo, do_regex=True, custom_regexes=rules, do_entropy=False, max_depth=100)
        
        Issue = []
        for issue in results["foundIssues"]:

            d = loads(open(issue).read())
            d['github_url'] = "{}/blob/{}/{}".format(gitRepo[:len(gitRepo)-4], d['commitHash'], d['path'])
            d['github_commit_url'] = "{}/commit/{}".format(gitRepo[:len(gitRepo)-4], d['commitHash'])
            d['diff'] = d['diff'][0:200]
            d['printDiff'] = d['printDiff'][0:200]
            

            Issue.append(d)
        
        count=0
        count=len(Issue)
        return Issue,count



    
    def getDataFromOrg(orgname):
        github_repo_org.clear()
        get_org_repos(orgname,1)
        data_of_org = []
        
        for repo in github_repo_org:
            repos = {}
            repos["repoName"]=repo
            repos["secret"],repos["Secrets_Found_Count"]=findSecrets(repo+".git")
            
            data_of_org.append(repos)
        data = {}
        data['Org']=orgname
        data['TestResults']=data_of_org
        
        return data

    def getDataFromKeyword(keyword):
        
        domain = keyword
        try:
            res = get_tld("http://"+keyword, as_object=True);
            keyword=res.domain
           
            github_repo_by_bigquery = set()
            
            github_repo_by_githubapi.clear()
            limit = 3
            findallkeywords(keyword,1,limit); 
            
            github_repo_by_both_method = github_repo_by_bigquery.union(github_repo_by_githubapi);
            
            data_of_keyword = [];
            count=0
            for repo in github_repo_by_both_method:
                
                repos={}
                repos["repoName"]=repo
                repos["secret"],repos["Secrets_Found_Count"]=findSecrets(repo+".git")
                
                data_of_keyword.append(repos)
            data = {}
            data["Domain"]=domain
            data["TestResults"]=data_of_keyword
            
            return data
        except:
            data = {}
            data["Domain"]=domain
            data["TestResults"]=[]
            return data


except ConnectionError as e:
    print("Data is currently not available, Apologies for the inconvenience !! ") 
except ImportError as e:
    print("ImportError ", e.args)
except NameError as e:
    print(e.args)
except requests.exceptions.ConnectionError:
    print("connection errorr")
except Exception as e: 
    print(e) 








        