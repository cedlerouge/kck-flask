# inspired by https://github.com/curityio/example-python-openid-connect-client/

import json

def print_json(map):
    print(json.dumps(map, indent=4, sort_keys=True))