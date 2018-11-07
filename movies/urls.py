from django.urls import path
from .views import call_json_to_db, get_all_movies, add_movie, edit_movie, remove_movie

urlpatterns = [
    path('load-db/', call_json_to_db, name='load_db'),
    path('list/', get_all_movies, name='all_movies'),
    path('add/', add_movie, name='add_movie'),
    path('edit/', edit_movie, name='edit_movie'),
    path('remove/', remove_movie, name='remove_movie'),
]
