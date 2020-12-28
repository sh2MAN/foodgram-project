from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm
from .models import Recipe

User = get_user_model()


def index(request):
    if request.GET.get('tags'):
        tags = request.GET.get('tags')
        recipe_list = Recipe.objects.filter(tag__contains=tags).select_related(
            'author').all()
    else:
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
    ingredients = recipe.ingredients.all()
    return render(
        request,
        'recipe_single_page.html',
        {'author': author, 'recipe': recipe, 'ingredients': ingredients}
    )


@login_required
def recipe_add_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'recipe_add_new.html', {'form': form})

    form = RecipeForm()
    return render(request, 'recipe_add_new.html', {'form': form})
