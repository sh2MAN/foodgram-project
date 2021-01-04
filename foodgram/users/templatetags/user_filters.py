from django import template

register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def get_color_tag(arg):
    TAGS_COLOR = {
        'breakfast': 'orange',
        'lunch': 'green',
        'dinner': 'purple'
    }
    return TAGS_COLOR.get(arg)


@register.filter
def get_recipe_tags(tags_list):
    tags = ''
    if 'lunch' in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_green">Обед</span></li>')
    if 'breakfast' in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_orange">Завтрак</span></li>')
    if 'dinner' in tags_list:
        tags += str('<li class="card__item"><span class="badge badge_style_purple">Ужин</span></li>')

    return tags


@register.filter(name='is_subscribe')
def is_subscribe(author, user):
    return user.subscriber.filter(author=author).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


# @register.filter(name='is_shop')
# def is_shop(recipe, user):
#     return ShoppingList.objects.filter(user=user, recipe=recipe).exists()

@register.filter
def num_other_recipes(num):
    """Количество оставшихся рецептов"""
    if num < 4:
        return 'Перейти к автору...'

    index = 2
    num_remaining_recipes = (int(num) - 3) % 10

    if num_remaining_recipes == 1:
        index = 0
    elif 2 <= num_remaining_recipes <= 4:
        index = 1
    suffix = ['рецепт', 'рецепта', 'рецептов'][index]

    return f'Ещё {num_remaining_recipes} {suffix}...'
