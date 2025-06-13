from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.sheet_add, name='sheet_add'),
    path('form/', views.sheet_form, name='sheet_form'),  # 👈 เพิ่มบรรทัดนี้
    path('list/', views.sheet_list_view, name='sheet_list'),
]
