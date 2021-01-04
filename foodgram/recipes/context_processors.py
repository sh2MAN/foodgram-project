from .models import Basket


def counter(request):
    if request.user.is_authenticated:
        count = Basket.objects.filter(user=request.user).count()
    else:
        count = None
    return {'count': count}
