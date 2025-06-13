from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list_view),
    # path('add/', views.sheet_add, name='sheet_add'),
    # path('form/', views.sheet_form, name='sheet_form'),
    # path('list/', views.sheet_list_view, name='sheet_list'),

    # # ✅ ต้องมี 2 บรรทัดนี้
    # path('update/<int:row_number>/', views.sheet_update, name='sheet_update'),
    # path('delete/<int:row_number>/', views.sheet_delete, name='sheet_delete'),


]
