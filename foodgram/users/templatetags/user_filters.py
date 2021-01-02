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
