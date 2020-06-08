import requests
import json
import re



def get_ladder(limit, offset):
	query_string = 'https://www.pathofexile.com/api/ladders/Delirium?limit={}&offset={}&type=league'.format(limit, offset)
	print(query_string)
	r = requests.get(query_string)
	return r.json()

def get_character(accountName, character):
	query_string = 'https://www.pathofexile.com/character-window/get-items?accountName={}&character={}'.format(accountName, character)
	print(query_string)
	r = requests.get(query_string)
	return r.json()

def main():
	rings_dict = {}
	ladder = get_ladder(200, 0)
	character = get_character('entreri0', 'DarkcloudZS')
	for item in character['items']:
		if item['frameType'] == 3:
			continue
		# if item['name']:
		# 	print('{}: {}'.format(item['inventoryId'], item['name']))
		# else:
		# 	print('{}: {}'.format(item['inventoryId'], item['typeLine']))

		# Check explicit mods
		for mod in item['explicitMods']:
			mod = re.sub(r'[0-9]+', '#', mod)
			if 'Ring' in item['inventoryId']:
				if mod in rings_dict:
					rings_dict[mod] = rings_dict[mod] + 1
				else:
					rings_dict[mod] = 1

		# Check crafted mods
		if 'craftedMods' in item:
			for mod in item['craftedMods']:
				mod = re.sub(r'[0-9]+', '#', mod)
				if 'Ring' in item['inventoryId']:
					if mod in rings_dict:
						rings_dict[mod] = rings_dict[mod] + 1
					else:
						rings_dict[mod] = 1

	for key in rings_dict:
		print('{}: {}'.format(key, rings_dict[key]))
	
	# print('')

if __name__ == '__main__':
	main()