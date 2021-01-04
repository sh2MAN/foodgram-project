from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
import json

from users.models import User
from recipes.models import Recipe, Ingredient


class Subscribe(LoginRequiredMixin, View):
    def post(self, request):
        req_ = json.loads(request.body)
        author_id = req_.get("id", None)
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            _, created = request.user.subscriber.get_or_create(
                author=author
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        author = get_object_or_404(User, id=author_id)
        subscriber = request.user.subscriber.filter(author=author)
        if subscriber:
            subscriber.delete()
        return JsonResponse({"success": True})


class Favorite(LoginRequiredMixin, View):
    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            _, created = request.user.favorites.get_or_create(
                recipe=recipe
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = request.user.favorites.filter(recipe=recipe)
        if favorite:
            favorite.delete()
        return JsonResponse({"success": True})


class Purchase(LoginRequiredMixin, View):
    def post(self, request):
        req_ = json.loads(request.body)
        recipe_id = req_.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id=recipe_id)
            _, created = request.user.basket_recipes.get_or_create(
                recipe=recipe
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        purchase = request.user.basket_recipes.filter(recipe=recipe)
        if purchase:
            purchase.delete()
        return JsonResponse({"success": True})


class Ingredients(LoginRequiredMixin, View):
    def get(self, request):
        text = request.GET['query']
        ingredients = list(Ingredient.objects.filter(
            title__icontains=text).values('title', 'dimension'))
        return JsonResponse(ingredients, safe=False)
