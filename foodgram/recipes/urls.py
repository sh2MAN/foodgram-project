from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(
        '<str:author>/<int:recipe_id>/',
        views.recipe_single_page,
        name='recipe'
    )
]
