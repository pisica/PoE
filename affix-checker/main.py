import requests
import json

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
	# print(get_ladder(200, 0))
	character = get_character('entreri0', 'DarkcloudZS')
	# print(character['items'][0]['frameType'])
	for item in character['items']:
		if item['name']:
			print('{}: {}'.format(item['inventoryId'], item['name']))
		else:
			print('{}: {}'.format(item['inventoryId'], item['typeLine']))

		for mod in item['explicitMods']:
			print(mod)
		print('')

if __name__ == '__main__':
	main()