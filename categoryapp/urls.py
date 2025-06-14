from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list_view, name='category_list'),
    path('add/', views.category_create_view, name='category_add'),
    path('update/<int:row_number>/', views.category_update_view, name='category_update'),
    path('delete/<int:row_number>/', views.category_delete_view, name='category_delete'),
]

