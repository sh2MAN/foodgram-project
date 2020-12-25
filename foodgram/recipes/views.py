from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Recipe, RecipeIngredients

User = get_user_model()


def index(request):
    recipe_list = Recipe.objects.select_related('author').all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {'page': page, 'paginator': paginator}
    )


def recipe_single_page(request, author, recipe_id):
    author = get_object_or_404(User, username=author)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)
    ingredients = RecipeIngredients.objects.filter(recipe=recipe)
    return render(
        request,
        'recipe_single_page.html',
        {'author': author, 'recipe': recipe, 'ingredients': ingredients}
    )
