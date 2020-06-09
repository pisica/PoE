import requests
import json
import re


def get_passives(accountName, character):
    query_string = 'https://www.pathofexile.com/character-window/get-passive-skills?accountName={}&character={}&reqData=1'.format(
        accountName, character)
    print(query_string)
    r = requests.get(query_string)
    return r.json()


def get_total_mods_values(accountName, character):
    data = get_passives(accountName, character)
    allocated = data['hashes']

    # This returns ALL nodes of the tree, not just allocated nodes.
    node_keys = data['skillTreeData']['nodes']
    res_dict = {}  # {mod_name: summed_up_stats}

    # Iterate over all nodes
    for n in node_keys:
        if n == "root":
            continue

        node = node_keys[n]
        if 'stats' not in node:
            continue

        if node['skill'] not in allocated:
            continue

        for mod in node['stats']:
            generic = re.sub(r'[0-9]+', '#', mod)
            matches = re.search('([0-9]*\.?[0-9]+)', mod, re.IGNORECASE)  # catches 1 or 1.0
            if matches:
                digits = float(matches.group(1))
                if generic not in res_dict:
                    res_dict.update({generic: digits})
                else:
                    res_dict.update({generic: res_dict[generic] + digits})

    return res_dict


def add_to_total(totals, t1):
    for n in t1.keys():
        if n in totals.keys():
            totals[n] += t1[n]
        else:
            totals[n] = t1[n]

    return totals


def get_averages(totals, num_of_chars, search_term=""):
    sort = sorted(totals, key=totals.get, reverse=True)
    sorted_dict = {}
    for stat in sort:
        sorted_dict.update({stat: totals[stat]})

    search_term = search_term.lower()
    print(f"----{search_term} FILTER----")
    found = {key: value for (key, value) in sorted_dict.items() if search_term in key.lower()}
    for k, v in found.items():
        print(f"{k}: {v / num_of_chars}")


if __name__ == '__main__':
    total_mods_values = {}
    CHARACTERS = [("DinooD", "DiscoDeliriumPerudo"),
                  ('DinooD', 'DiscoBabaYaga'),
                  ('DinooD', 'DiscoMilkoKalaidjiev'),
                  ('DinooD', 'DiscoGopnik'),
                  ('DinooD', 'DiscoGolems'),
                  ]
    for char in CHARACTERS:
        res = get_total_mods_values(char[0], char[1])
        add_to_total(total_mods_values, res)

    get_averages(total_mods_values, len(CHARACTERS), search_term="LIFE")
