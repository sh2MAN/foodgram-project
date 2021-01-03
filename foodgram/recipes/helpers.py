from django.shortcuts import redirect
from .models import Ingredient, RecipeIngredients


def get_list_ingredients(obj):
    name_ingridients = [
        obj.get(val) for val in obj if val.startswith('nameIngredient')
    ]
    value_ingredients = [
        obj.get(val) for val in obj if val.startswith('valueIngredient')
    ]
    if len(name_ingridients) != len(value_ingredients):
        return redirect("add_recipe")
    return dict(zip(name_ingridients, value_ingredients))


def ingredients_create_or_delete(recipe, ingredients, new_ingredients):
    cur = set([obj.ingredient.title for obj in ingredients])
    new = set(new_ingredients)
    if cur != new:
        ingredients_delete(recipe, list(cur.difference(new)))
        ingredients_create(
            recipe, [(key, val) for key, val in new_ingredients if k in new]
        )


def ingredients_create(recipe, ingredients):
    for name, value in ingredients:
        RecipeIngredients.objects.create(
            recipe=recipe,
            ingredient=get_ingredient(name),
            quantity=value
        )


def ingredients_delete(recipe, ingredients):
    for ingredient in ingredients:
        RecipeIngredients.objects.get(
            recipe=recipe, ingredient=get_ingredient(ingredient)
        ).delete()


def get_ingredient(ingredient):
    if isinstance(ingredient, Ingredient):
        return ingredient
    return Ingredient.objects.get(title=ingredient)
