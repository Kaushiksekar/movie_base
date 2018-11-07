from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .custom import load_json_to_db
from . import models as db

@api_view()
def call_json_to_db(request):
    load_json_to_db()
    return Response(
    data = {
        "message": "JSON loaded to DB"
    },
    status=status.HTTP_200_OK
    )

@api_view()
def get_all_movies(request):
    movie_list = []
    movies_list = db.Movies.objects.all()
    for item in movies_list:
        temp_dict = {}
        temp_dict["popularity"] = item.popularity
        temp_dict["director"] = item.director
        temp_dict["imdb_score"] = item.imdb_score
        temp_dict["name"] = item.name
        temp_dict["genre"] = []
        movies_with_genres = db.MoviesWithGenres.objects.filter(movie_id=item)
        try:
            for mwg_item in movies_with_genres:
                temp_dict["genre"].append(mwg_item.genre_id.genre)
        except:
            temp_dict["genre"].append(movies_with_genres.genre_id.genre)
        movie_list.append(temp_dict)
    return Response(
    data = {
        "movies": movie_list
    },
    status=status.HTTP_200_OK
    )

@api_view(['POST'])
def add_movie(request):
    current_user = request.user
    try:
        user_obj = User.objects.get(username=current_user)
        if not user_obj.is_staff:
            return Response(
            data = {
                "message": "Only admin users can add a movie" + current_user
            },
            status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            name = request.data.get("name", "")
            director = request.data.get("director", "")
            popularity = request.data.get("popularity", "")
            imdb_score = request.data.get("imdb_score", "")
            genre = request.data.get("genre", [])
            try:
                if type(genre) is not list:
                    return Response(
                    data = {
                        "message": "Genre must be a list and all others must be a string"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                    )
                movie = db.Movies(name=name, director=director, popularity=float(popularity), imdb_score=float(imdb_score))
                movie.save()
                for item in genre:
                    try:
                        genre = db.Genres.objects.get(genre=item.strip())
                        genre_id = genre.id
                    except:
                        genre = db.Genres(genre=genre_item.strip())
                        genre.save()
                    movies_with_genres = db.MoviesWithGenres(genre_id=genre, movie_id=movie)
                    movies_with_genres.save()
                return Response(
                data = {
                    "message": "Movie added"
                },
                status=status.HTTP_200_OK
                )
            except:
                return Response(
                data = {
                    "message": "Genre must be a list and all others must be a string"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
    except:
        return Response(
        data = {
            "message": "Only admin users can add a movie"
        },
        status=status.HTTP_401_UNAUTHORIZED
        )
    return Response(
    data = {
        "movies": "Add movie"
    },
    status=status.HTTP_200_OK
    )

@api_view(['POST'])
def edit_movie(request):
    current_user = str(request.user)
    try:
        user_obj = User.objects.get(username=current_user)
        if not user_obj.is_staff:
            return Response(
            data = {
                "message": "Only admin users can edit a movie, not " + current_user
            },
            status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            name = request.data.get("name", "")
            director = request.data.get("director", "")
            popularity = request.data.get("popularity", "")
            imdb_score = request.data.get("imdb_score", "")
            genre = request.data.get("genre", [])
            if not name:
                return Response(
                data = {
                    "message": "Please provide name for search criteria"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            try:
                movie = db.Movies.objects.get(name__regex=r'(?i).*?' + name + '.*?')
            except:
                return Response(
                data = {
                    "message": "Multiple objects returned. Refine your search criteria"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            if type(genre) is not list:
                return Response(
                data = {
                    "message": "Genre must be a list and all others must be a string"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            if director and movie.director is not director:
                movie.director = director
            if popularity and movie.popularity is not popularity:
                movie.popularity = float(popularity)
            if imdb_score and movie.imdb_score is not imdb_score:
                movie.imdb_score = float(imdb_score)
            movie.save()
            if genre:
                movies_with_genres = db.MoviesWithGenres.objects.filter(movie_id=movie)
                movies_with_genres.delete()
            for item in genre:
                try:
                    genre = db.Genres.objects.get(genre=item.strip())
                    genre_id = genre.id
                except:
                    genre = db.Genres(genre=genre_item.strip())
                    genre.save()
                movies_with_genres = db.MoviesWithGenres(genre_id=genre, movie_id=movie)
                movies_with_genres.save()
            # getting the return data
            movie_genre_list = db.MoviesWithGenres.objects.filter(movie_id=movie)
            genre_names = []
            try:
                for item in movie_genre_list:
                    genre_names.append(item.genre_id.genre)
            except:
                genre_names.append(movie_genre_list.genre_id.genre)
            return Response(
            data = {
                "name": movie.name,
                "director": movie.director,
                "popularity": movie.popularity,
                "imdb_score": movie.imdb_score,
                "genre": genre_names,
                "message": "Success"
            },
            status=status.HTTP_200_OK
            )
    except:
        return Response(
        data = {
            "message": "Only admin users can edit a movie" + current_user
        },
        status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
def remove_movie(request):
    current_user = str(request.user)
    try:
        user_obj = User.objects.get(username=current_user)
        if not user_obj.is_staff:
            return Response(
            data = {
                "message": "Only admin users can remove a movie, not " + current_user
            },
            status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            name = request.data.get("name", "")
            try:
                movie = db.Movies.objects.get(name__regex=r'(?i).*?' + name + '.*?')
            except:
                return Response(
                data = {
                    "message": "Multiple objects returned. Refine your search criteria"
                },
                status=status.HTTP_400_BAD_REQUEST
                )
            name = movie.name
            movie.delete()
            return Response(
            data = {
                "message": "Movie : " + name + " is deleted."
            },
            status=status.HTTP_400_BAD_REQUEST
            )
    except:
        data = {
            "message": "Only admin users can remove a movie, not " + current_user
        },
        status=status.HTTP_401_UNAUTHORIZED
        )
