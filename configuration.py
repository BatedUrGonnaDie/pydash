import json
import webbrowser

def open_file():

    try:
        with open("config.json", 'r') as config_file:
            user_config = json.load(config_file, encoding = 'utf-8')
    except:
        new_file = True
        user_config = {"channel" : "", "oauth" : "", "auth" : ""}
        with open('config.json', 'w') as config_file:
            json.dump(user_config, config_file, sort_keys = True, indent = 4, ensure_ascii=False, encoding = 'utf-8')
        url = "http://google.com"
        webbrowser.open(url, new = 2)

    return user_config

def set_param(param, info):
    pass

open_file()
