from functools import reduce

from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Recipe, RecipeIngredients


def get_list_ingredients(obj):
    name_ingridients = [
        obj.get(val) for val in obj if val.startswith('nameIngredien')
    ]
    value_ingredients = [
        obj.get(val) for val in obj if val.startswith('valueIngredien')
    ]
    if len(name_ingridients) != len(value_ingredients):
        return redirect("add_recipe")
    return dict(zip(name_ingridients, value_ingredients))


def get_filter_tags(tags):
    filter = reduce(
        lambda x, y: x | y, [
            Q(tags__contains=tag) for tag in tags.split('|')
        ]
    )
    return filter


def download_basket(request):
    recipes = Recipe.objects.filter(
        basket_users__user=request.user
    )
    ingredients = RecipeIngredients.objects.filter(
        recipe__id__in=recipes
    )

    ingredients = ingredients.values(
        'ingredient__title', 'ingredient__dimension'
    ).annotate(
        total_quantity=Sum('quantity')
    )
    file_text = ""

    for item in ingredients:
        title, dimension, quantity = item.values()
        line = f'{title.capitalize()} ({dimension}) - {quantity}'
        file_text += line + '\n'

    response = HttpResponse(
        file_text, content_type='application/text charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="ShoppingList.txt"'
    return response
