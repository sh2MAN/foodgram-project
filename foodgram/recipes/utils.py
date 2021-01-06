from django.shortcuts import redirect
from django.db.models import Q
from functools import reduce


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


def get_filter_tags(tags):
    filter = reduce(
        lambda x, y: x | y, [
            Q(tags__contains=tag) for tag in tags.split('|')
        ]
    )
    return filter
