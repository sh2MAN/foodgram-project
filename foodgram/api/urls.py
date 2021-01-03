from django.urls import path

from . import views

urlpatterns = [
    path("subscriptions", views.Subscribe.as_view()),
    path("subscriptions/<int:author_id>", views.Subscribe.as_view()),
]
