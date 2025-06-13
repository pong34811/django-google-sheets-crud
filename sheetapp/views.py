from django.http import JsonResponse
from . import sheets_service
import json

from django.shortcuts import render

def sheet_form(request):
    return render(request, 'sheet_form.html')


# def sheet_list(request):
#     data = sheets_service.get_all_data()
#     return JsonResponse(data, safe=False)

def sheet_list_view(request):
    raw_data = sheets_service.get_all_data()
    # สมมติ raw_data เป็น [{'ชื่อ': 'สมชาย', 'อายุ': 30}, {...}]
    # แปลงเป็น key ภาษาอังกฤษตาม template
    data = [{'name': row.get('ชื่อ'), 'age': row.get('อายุ')} for row in raw_data]
    return render(request, 'sheet_list.html', {'data': data})


def sheet_add(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        name = payload.get('name')
        age = payload.get('age')

        sheets_service.add_row([name, age])
        return JsonResponse({"status": "added"})
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)
