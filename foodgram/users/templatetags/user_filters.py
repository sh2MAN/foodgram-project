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


@register.filter(name='is_basket')
def is_basket(recipe, user):
    if user.is_authenticated:
        return user.basket_recipes.filter(recipe=recipe).exists()


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


@register.simple_tag
def tags_filter(request, new_tag):
    tags = ''
    url = request.GET.copy()
    if url.get('tags', None):
        tags = set(
            url.get('tags').split('|')
        ).symmetric_difference([new_tag])
        if not tags:
            return request.path
    url['tags'] = '|'.join(tags) or new_tag
    return f'?{url.urlencode()}'


@register.simple_tag
def set_page(request, value):
    request_object = request.GET.copy()
    request_object["page"] = value
    return request_object.urlencode()
