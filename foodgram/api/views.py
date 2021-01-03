from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
import json

from users.models import Subscription, User


class Subscribe(LoginRequiredMixin, View):
    def post(self, request):
        print(request)
        req_ = json.loads(request.body)
        author_id = req_.get("id", None)
        if author_id is not None:
            author = get_object_or_404(User, id=author_id)
            obj, created = Subscription.objects.get_or_create(
                user=request.user, author=author
            )
            if created:
                return JsonResponse({"success": True})
            return JsonResponse({"success": False})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author_id):
        user = get_object_or_404(
            User, username=request.user.username
        )
        author = get_object_or_404(User, id=author_id)
        obj = get_object_or_404(Subscription, user=user, author=author)
        obj.delete()
        return JsonResponse({"success": True})
