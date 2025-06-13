from django.http import JsonResponse
from config import user_sheet ,sheets_service
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

def sheet_form(request):
    return render(request, 'sheet_form.html')


# def sheet_list(request):
#     data = sheets_service.get_all_data()
#     return JsonResponse(data, safe=False)

def sheet_list_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('/sheet/login/') 
    
    raw_data = sheets_service.get_all_data()
    # สมมติ raw_data เป็น [{'ชื่อ': 'สมชาย', 'อายุ': 30}, {...}]
    # แปลงเป็น key ภาษาอังกฤษตาม template
    data = [{'name': row.get('ชื่อ'), 'age': row.get('อายุ')} for row in raw_data]
    return render(request, 'sheet_list.html', {'data': data, 'username': username})

@csrf_exempt
def sheet_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')

        sheets_service.add_row([name, age])
        return render(request, 'sheet_form.html', {
            'message': 'เพิ่มข้อมูลสำเร็จแล้ว ✅'
        })
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)
    
@csrf_exempt
def sheet_update(request, row_number):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')

        sheets_service.update_row(row_number, [name, age])
        
        messages.success(request, f'อัปเดตข้อมูลที่บรรทัด {row_number} สำเร็จแล้ว ✅')
        return redirect('/sheet/list/')  # redirect ไปที่ /sheet/list/
    else:
        messages.error(request, 'เฉพาะ POST method เท่านั้นที่สามารถอัปเดตข้อมูลได้')
        return redirect('/sheet/list/')

@csrf_exempt
def sheet_delete(request, row_number):
    if request.method in ['POST', 'DELETE']:
        try:
            row_num = int(row_number)
        except ValueError:
            messages.error(request, "เลขแถวไม่ถูกต้อง")
            return redirect('/sheet/list/')
        
        sheets_service.delete_row(row_num)  # ลบแถวจริงใน Google Sheets (ข้าม header)

        messages.success(request, f'ลบข้อมูลที่บรรทัด {row_num} สำเร็จแล้ว ✅')
        return redirect('/sheet/list/')
    else:
        messages.error(request, "เฉพาะ POST หรือ DELETE เท่านั้นที่ลบข้อมูลได้")
        return redirect('/sheet/list/')
    
