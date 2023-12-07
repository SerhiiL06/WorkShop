from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as swagger_url


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("accounts/", include("users.urls")),
    path("", include("orders.urls")),
]


urlpatterns += swagger_url
