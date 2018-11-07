import json
from movies import models as db

with open("imdb.json") as movie_json:
	data = json.load(movie_json)

	for item in data:
		print(item)
		break