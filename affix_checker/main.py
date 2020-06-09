import requests
import json
import re
import sys


def get_ladder(limit, offset):
	query_string = 'https://www.pathofexile.com/api/ladders/Delirium?limit={}&offset={}&type=league'.format(limit, offset)
	# print(query_string)
	r = requests.get(query_string)
	return r.json()


def get_character(account_name, character):
	# print(account_name + ' ' + character)
	query_string = 'https://www.pathofexile.com/character-window/get-items?accountName={}&character={}'.format(account_name, character)
	# print(query_string)
	r = requests.get(query_string)
	if r.status_code == 403:
		raise Exception('	Failed to get character: 403 Forbidden')
	return r.json()


def check_character_skill_gem(character, skill_gem):
	for item in character['items']:
		if item['inventoryId'] == 'Weapon':
			if 'socketedItems' in item:
				for socket in item['socketedItems']:
					# print('		weapon sockets: ' + socket['typeLine'].lower())
					if skill_gem in socket['typeLine'].lower():
						return True
					else:
						continue
		elif item['inventoryId'] == 'BodyArmour':
			if 'socketedItems' in item:
				for socket in item['socketedItems']:
					# print('		bodyarmour sockets: ' + socket['typeLine'].lower())
					if skill_gem in socket['typeLine'].lower():
						return True
					else:
						continue
	return False


def get_affixes(item, affixes):

	# Check implicit mods
	if 'implicitMods' in item:
		for mod in item['implicitMods']:
			mod = re.sub(r'[0-9]+', '#', mod)
			if mod in affixes:
				affixes[mod] = affixes[mod] + 1
			else:
				affixes[mod] = 1

	# Check explicit mods
	if 'explicitMods' in item:
		for mod in item['explicitMods']:
			mod = re.sub(r'[0-9]+', '#', mod)
			if mod in affixes:
				affixes[mod] = affixes[mod] + 1
			else:
				affixes[mod] = 1

	# Check crafted mods
	if 'craftedMods' in item:
		for mod in item['craftedMods']:
			mod = re.sub(r'[0-9]+', '#', mod)
			if mod in affixes:
				affixes[mod] = affixes[mod] + 1
			else:
				affixes[mod] = 1

	return affixes

def sort_affixes(affixes):
	return affixes

def main():
	affixes = {}

	skill_gem = sys.argv[1].lower()
	item_slot = sys.argv[2].lower()

	ladder = get_ladder(20, 0)
	count = 0
	unique_count = 0
	forbidden_count = 0
	empty_count = 0
	no_skill_count = 0
	for character in ladder['entries']:
		try:
			character = get_character(character['account']['name'], character['character']['name'])
		except Exception as e:
			forbidden_count += 1
			print(e)
			continue

		if not character['items']:
			empty_count += 1
			continue

		if check_character_skill_gem(character, skill_gem):
			for item in character['items']:
				# Ignore unique items

				if item_slot in item['inventoryId'].lower():
					if item['frameType'] == 3:
						unique_count += 1
						continue
					affixes = get_affixes(item, affixes)
					count += 1
		else:
			no_skill_count += 1

		# if item['name']:
		# 	print('{}: {}'.format(item['inventoryId'], item['name']))
		# else:
		# 	print('{}: {}'.format(item['inventoryId'], item['typeLine']))

	print('')
	print('AFFIXES:')
	for key in sort_affixes(affixes):
		print('		{}: {}'.format(key, affixes[key]))

	print('')
	print('Total characters no skill: {}'.format(no_skill_count))
	print('Total characters empty: {}'.format(empty_count))
	print('Total characters forbidden: {}'.format(forbidden_count))
	print('Total items uniques: {}'.format(unique_count))
	print('Total items checked: {}'.format(count))


if __name__ == '__main__':
	main()