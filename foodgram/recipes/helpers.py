from django.shortcuts import redirect


def get_list_ingredients(obj):
    name_ingridients = [
        obj.get(val) for val in obj if val.startswith('nameIngredient')
    ]
    value_ingredients = [
        obj.get(val) for val in obj if val.startswith('valueIngredient')
    ]
    if len(name_ingridients) != len(value_ingredients):
        return redirect("add_recipe")
    return zip(name_ingridients, value_ingredients)
