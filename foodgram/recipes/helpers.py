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
    return dict(zip(name_ingridients, value_ingredients))


def tags(tag, new_tag):
    list_tags = set(tag.split('&')).symmetric_difference([new_tag])
    return '&'.join(list_tags)
