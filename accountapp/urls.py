from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_list_view, name='account_list_view'),
    path('add/', views.account_create_view, name='account_add'),
    path('update/<int:row_number>/', views.account_update_view, name='account_update'),
    path('delete/<int:row_number>/', views.account_delete_view, name='account_delete'),
]

