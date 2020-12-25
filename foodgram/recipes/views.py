from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Recipe

User = get_user_model()


def index(request):
    recipe_list = Recipe.objects.select_related('author').all()
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {'page': page, 'paginator': paginator}
    )
