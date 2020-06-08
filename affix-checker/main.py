import requests

def getLadder(limit, offset):
	queryString = 'https://www.pathofexile.com/api/ladders/Delirium?limit={}&offset={}&type=league'.format(limit, offset)
	print(queryString)
	r = requests.get(queryString)
	return r.text

def getCharacter(accountName, character):
	queryString = 'https://www.pathofexile.com/character-window/get-items?accountName={}&character={}'.format(accountName, character)
	print(queryString)
	r = requests.get(queryString)
	return r.text

def main():
	print(getLadder(200, 0))
	print(getCharacter('entreri0', 'DarkcloudZS'))

if __name__ == '__main__':
	main()