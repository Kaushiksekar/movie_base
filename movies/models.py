from django.db import models

class Movies(models.Model):
    popularity = models.FloatField(default=0.0)
    director = models.CharField(max_length=200)
    imdb_score = models.FloatField(default=0.0)
    name = models.CharField(max_length=200)

class Genres(models.Model):
    genre = models.CharField(max_length=200)

class MoviesWithGenres(models.Model):
    genre_id = models.ForeignKey(Genres, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE)
