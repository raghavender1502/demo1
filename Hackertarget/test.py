import requests

def analyticslookup(domain):
    res = requests.get('https://api.hackertarget.com/analyticslookup/?q=' + domain)
    response1 = res.text.splitlines()

    # domains = []
    # user_agents = []

    # for line in response:
    #     domain, user_agent = line.split(',')
    #     domains.append(domain.strip())
    #     user_agents.append(user_agent.strip())

    payload = {
        "Domain": domain,
        "results": response1
        # "DomainsList": domains,
        # "UserAgentsList": user_agents
    }
    return payload

# Example usage:
print(analyticslookup('elch.org'))
