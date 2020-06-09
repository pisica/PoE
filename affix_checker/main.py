import requests
import json
import re
import sys
import os
import time

LADDER_FILE = 'ladder.txt'
CHARACTER_FILE = 'characters.txt'

def get_ladder(character_count):
	file_path = '{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)), LADDER_FILE)
	print(file_path)
	ladder = {}
	if os.path.exists(file_path):
		f = open(file_path, 'r')
		ladder = json.load(f)
	else:
		f = open(file_path, 'a')
		for x in range(character_count):
			query_string = 'https://www.pathofexile.com/api/ladders/Delirium?limit={}&offset={}&type=league'.format(10, (x*200))
			# print(query_string)
			r = requests.get(query_string)
			json.dump(r.json(), f)
			ladder = dict(ladder, **r.json())

	return ladder
			


def get_characters(ladder):
	file_path = '{}\\{}'.format(os.path.dirname(os.path.abspath(__file__)), CHARACTER_FILE)
	print(file_path)
	# print(account_name + ' ' + character)
	characters = {}
	if os.path.exists(file_path):
		f = open(file_path, 'r')
		characters = json.load(f)
	else:
		f = open(file_path, 'a')
		for character in ladder['entries']:
			time.sleep(1)
			query_string = 'https://www.pathofexile.com/character-window/get-items?accountName={}&character={}'.format(character['account']['name'], character['character']['name'])
			# print(query_string)
			r = requests.get(query_string)
			print(r.json())
			if r.status_code == 403:
				continue
			if 'items' not in r:
				continue
			if not r['items']:
				continue
				# raise Exception('	Failed to get character: 403 Forbidden')
			print('Writing to file: {}'.format(r.json()))
			json.dump(r.json(), f)
			characters = dict(characters, **r.json())

	return characters


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
	return sorted(affixes.items(), key=lambda x: x[1], reverse=True)

def main():
	affixes = {}

	skill_gem = sys.argv[1].lower()
	item_slot = sys.argv[2].lower()
	character_count = int(sys.argv[3])
		
	print('Reading {} characters'.format(character_count*200))

	ladder = get_ladder(character_count)

	characters = get_characters(ladder)

	count = 0
	unique_count = 0
	forbidden_count = 0
	empty_count = 0
	no_skill_count = 0

	for character in characters:
		if check_character_skill_gem(character, skill_gem):
			for item in character['items']:
				if item_slot in item['inventoryId'].lower():
					# Ignore unique items
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
	for affix in sort_affixes(affixes):
		print('	  {}'.format(affix))

	print('')
	print('Skill not present: {}'.format(no_skill_count))
	print('Empty characters: {}'.format(empty_count))
	print('Characters forbidden: {}'.format(forbidden_count))
	print('Uniques: {}'.format(unique_count))
	print('Items checked: {}'.format(count))


if __name__ == '__main__':
	main()