from django.urls import path

from . import views, utils

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.add_recipe, name='add_recipe'),
    path('favorite/', views.favorite, name='favorite'),
    path('subscribe/', views.my_subscribe, name='subscribe'),
    path('shopping/', views.shopping_list, name='cart'),
    path('download_basket', utils.download_basket, name='download_basket'),
    path('<str:author>/', views.recipe_author, name='profile'),
    path(
        '<str:author>/<int:recipe_id>/edit/',
        views.edit_recipe,
        name='edit_recipe'
    ),
    path(
        '<str:author>/<int:recipe_id>/delete/',
        views.delete_recipe,
        name='delete_recipe'
    ),
    path(
        '<str:author>/<int:recipe_id>/',
        views.recipe_single_page,
        name='recipe'
    ),
]
