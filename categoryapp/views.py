from django.http import JsonResponse
from config import category_sheet
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
import uuid
from django.utils.timezone import now
# Create your views here.

# def category_list_view(request):
#     # This is a placeholder for the actual category list logic
#     categories = [
#         {'id': 1, 'name': 'Category 1'},
#         {'id': 2, 'name': 'Category 2'},
#         {'id': 3, 'name': 'Category 3'},
#     ]
#     return render(request, 'category_list.html', {'categories': categories})

from django.core.paginator import Paginator
from django.shortcuts import render, redirect

def category_list_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('/auth/login/')

    raw_data = category_sheet.get_all_data()

    data = [
        {
            'row_number': index + 2,  # +2 เพราะ raw_data ไม่มี header, แถวข้อมูลจริงเริ่มที่ 2
            'id': row.get('id'),
            'name': row.get('name'),
            'is_active': row.get('is_active'),
            'created_by': row.get('created_by'),
            'created': row.get('created'),
            'updated_by': row.get('updated_by'),
            'updated': row.get('updated'),
        }
        for index, row in enumerate(raw_data)  # ต้องใช้ enumerate เพื่อให้ได้ index
    ]

    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(data, per_page)
    categories = paginator.get_page(page)

    edit_name = request.GET.get('edit_name', '')
    edit_row = request.GET.get('edit_row', '')

    return render(request, 'category_list.html', {
        'categories': categories,
        'username': username,
        'per_page': per_page,
        'edit_name': edit_name,
        'edit_row': edit_row,
    })





@csrf_exempt
def category_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        # age = request.POST.get('age')
        
        existing_categories = category_sheet.get_all_data()
        for row in existing_categories:
            if row.get('name', '').strip().lower() == name.lower():
                return JsonResponse({'error': 'Category with this name already exists'}, status=400)
        created_by = now().strftime('%Y-%m-%d %H:%M:%S')
        user_id = str(uuid.uuid4())
        new_row = [user_id, name, True, created_by, request.session.get('username'), None, None]
        category_sheet.add_row(new_row)
        
        messages.success(request, 'เพิ่มข้อมูลสำเร็จแล้ว ✅')
        
        return redirect('/category/')
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

@csrf_exempt
def category_update_view(request, row_number):
    if request.method == "POST":
        new_name = request.POST.get('name')
        username = request.session.get('username')
        
        all_rows = category_sheet.get_all_data()
        row = all_rows[row_number]
        
        row['name'] = new_name
        row['updated_by'] = username
        row['updated'] = now().strftime('%Y-%m-%d %H:%M:%S')
        
        header = ['id', 'name', 'is_active', 'created_by', 'created', 'updated_by', 'updated']
        row_list = [row.get(col, '') for col in header]
        
        category_sheet.update_row(row_number, row_list)

        messages.success(request, 'แก้ไขหมวดหมู่เรียบร้อยแล้ว')
        return redirect('/category/')


@csrf_exempt
def category_delete_view(request, row_number):
    if request.method == "POST":
        category_sheet.delete_row(row_number)
        messages.success(request, 'ลบหมวดหมู่เรียบร้อยแล้ว')
        return redirect('/category/')
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)