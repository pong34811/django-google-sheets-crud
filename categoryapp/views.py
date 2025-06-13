from django.http import JsonResponse
from config import category_sheet
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

# Create your views here.

# def category_list_view(request):
#     # This is a placeholder for the actual category list logic
#     categories = [
#         {'id': 1, 'name': 'Category 1'},
#         {'id': 2, 'name': 'Category 2'},
#         {'id': 3, 'name': 'Category 3'},
#     ]
#     return render(request, 'category_list.html', {'categories': categories})

def category_list_view(request):
    # username = request.session.get('username')
    # if not username:
    #     return redirect('/auth/login/') 
    
    raw_data = category_sheet.get_all_data()
    # สมมติ raw_data เป็น [{'ชื่อ': 'สมชาย', 'อายุ': 30}, {...}]
    # แปลงเป็น key ภาษาอังกฤษตาม template
    data = [
    {
        'id': row.get('id'),
        'name': row.get('name'),
        'is_active': row.get('is_active'),
        'created_by': row.get('created_by'),
        'created': row.get('created'),
        'updated_by': row.get('updated_by'),
        'updated': row.get('updated')
    }
    for row in raw_data if row
]
    return render(request, 'category_list.html', {'categories': data})