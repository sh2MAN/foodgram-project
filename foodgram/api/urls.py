from django.urls import path

from . import views

urlpatterns = [
    path('subscriptions/', views.Subscribe.as_view(), name='add_subscription'),
    path(
        'subscriptions/<int:author_id>',
        views.Subscribe.as_view(),
        name='del_subscription'
    ),
    path('favorites/', views.Favorite.as_view(), name='add_favorite'),
    path(
        'favorites/<int:recipe_id>',
        views.Favorite.as_view(),
        name='del_favorite'
    ),
    path('purchases/', views.Purchase.as_view(), name='add_purchase'),
    path(
        'purchases/<int:recipe_id>',
        views.Purchase.as_view(),
        name='del_purchase'
    ),
    path('ingredients/', views.Ingredients.as_view(), name='find_ingredient'),
]
