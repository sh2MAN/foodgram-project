from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .helpers import get_list_ingredients
from .models import Ingredient, Recipe, RecipeIngredients

User = get_user_model()


def index(request):
    if request.GET.get('tags'):
        tags = request.GET.get('tags')
        recipe_list = Recipe.objects.filter(
            tags__contains=tags
        ).select_related('author').all()
    else:
        recipe_list = Recipe.objects.select_related('author').all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {'page': page, 'paginator': paginator}
    )


def recipe_author(request, author):
    author = get_object_or_404(User, username=author)
    recipe_list = Recipe.objects.filter(author=author).all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'page': page,
        'paginator': paginator
    }
    return render(
        request,
        'authorRecipe.html',
        context=context
    )


def recipe_single_page(request, author, recipe_id):
    author = get_object_or_404(User, username=author)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)
    ingredients = recipe.ingredients.all()
    return render(
        request,
        'recipe_single_page.html',
        {'author': author, 'recipe': recipe, 'ingredients': ingredients}
    )


@login_required
def add_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == "POST" and form.is_valid():
        ingredients = get_list_ingredients(request.POST)

        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        for name, value in ingredients.items():
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(title=name),
                quantity=value
            )
        form.save_m2m()
        return redirect('index')

    return render(request, 'recipe_form.html', {'form': form})


@login_required
def edit_recipe(request, author, recipe_id):
    if request.user.username != author:
        return redirect('recipe', author, recipe_id)

    recipe = get_object_or_404(
        Recipe, pk=recipe_id, author__username=author
    )
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )

    ingredients = get_list_ingredients(request.POST)
    if form.is_valid():
        RecipeIngredients.objects.filter(recipe=recipe).delete()

        recipe = form.save(commit=False)
        recipe.save()

        for name, value in ingredients.items():
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(title=name),
                quantity=value
            )
        form.save_m2m()
        return redirect('recipe', author, recipe_id)

    context = {
        'form': form, 'recipe': recipe
    }

    return render(request, 'recipe_form.html', context=context)


def get_ingredients(request):
    if request.method == 'GET':
        query = request.GET.get("query")
        ingredients = Ingredient.objects.filter(
            title__icontains=query).values('title', 'dimension')
        return JsonResponse(list(ingredients), safe=False)
