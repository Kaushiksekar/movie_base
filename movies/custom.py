import json
from . import models as db

def load_json_to_db():
    db.Movies.objects.all().delete()
    db.Genres.objects.all().delete()
    db.MoviesWithGenres.objects.all().delete()
    with open("imdb.json") as movie_json:
    	data = json.load(movie_json)

    	for item in data:
            movie = db.Movies(popularity=item['99popularity'], director=item['director'],\
                    imdb_score = item['imdb_score'], name = item['name'])
            movie.save()

            for genre_item in item['genre']:
                try:
                    genre_db_item = db.Genres.objects.get(genre=genre_item.strip())
                    genre_db_item_id = genre_db_item.id
                    print("Genre item id inside try")
                    print(genre_db_item_id)
                    movies_with_genres = db.MoviesWithGenres(genre_id=genre_db_item, movie_id=movie)
                    movies_with_genres.save()
                except:
                    genre = db.Genres(genre=genre_item.strip())
                    genre.save()
                    genre_db_item_id = genre.id
                    print("Genre item id inside except")
                    print(genre_db_item_id)
                    movies_with_genres = db.MoviesWithGenres(genre_id=genre, movie_id=movie)
                    movies_with_genres.save()
