import requests
                                                # in flask REPL (shell)
                                                # import weather.api
                                                # >>> <Response>
# make get request to api, store response in 'response'
# response = requests.get('https://api.github.com/events')
# dict within list within dict

# response.text = ?
# response = response.json()
# print(response.text['consolidated weather']) 

# >>> string object without .json()

def make_query(endpoint='https://api.github.com/events'):
    return requests.get(endpoint).json()