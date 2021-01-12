from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.contrib.flatpages import views
from django.conf.urls.static import static

handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa

urlpatterns = [
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(
        'about-author/',
        views.flatpage,
        {'url': '/about-author/'},
        name='about_author',
    ),
    path(
        'about-spec/',
        views.flatpage,
        {'url': '/about-spec/'},
        name='about_spec',
    ),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
