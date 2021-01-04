from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.add_recipe, name='add_recipe'),
    path('favorite/', views.favorite, name='favorite'),
    path('subscribe/', views.my_subscribe, name='subscribe'),
    path('<str:author>/', views.recipe_author, name='profile'),
    path('<str:author>/<int:recipe_id>/edit/',
         views.edit_recipe, name='edit_recipe'),
    path(
        '<str:author>/<int:recipe_id>/',
        views.recipe_single_page,
        name='recipe'
    ),
]
