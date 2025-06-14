from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sheet/", include("sheetapp.urls")),
    path("category/", include("categoryapp.urls")),
    path("auth/", include("authapp.urls")),
    path("account/", include("accountapp.urls")),
]
