import json

def get_openai_api_key():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config['openai_api_key']

def get_azure_token():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config['azure_api_key']
