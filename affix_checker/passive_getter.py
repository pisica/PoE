import requests
import json
import re


def get_passives(accountName, character):
    query_string = 'https://www.pathofexile.com/character-window/get-passive-skills?accountName={}&character={}&reqData=1'.format(
        accountName, character)
    print(query_string)
    r = requests.get(query_string)
    return r.json()


def passives_test():
    data = get_passives("entreri0", "DarkcloudZS")
    node_keys = data['skillTreeData']['nodes']
    for n in node_keys:
        if n == "root":
            continue
        node = node_keys[n]
        if 'stats' not in node:
            continue
        for s in node['stats']:
            print(f'PASSIVE: {s}')


if __name__ == '__main__':
    passives_test()
