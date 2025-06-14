from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.timezone import now
import uuid

from config import account_sheet  # สมมุติว่าเชื่อมต่อ sheet สำเร็จแล้ว
# สมมุติว่าใช้ header แบบนี้:
# ['datetime', 'details', 'amount', 'type', 'category', 'created_by', 'created', 'updated_by', 'updated']


def account_list_view(request):
    username = request.session.get('username')
    if not username:
        return redirect('/auth/login/')

    raw_data = account_sheet.get_all_data()

    data = [
        {
            'row_number': index + 2,
            'datetime': row.get('datetime'),
            'details': row.get('details'),
            'amount': row.get('amount'),
            'type': row.get('type'),
            'category': row.get('category'),
            'created_by': row.get('created_by'),
            'created': row.get('created'),
            'updated_by': row.get('updated_by'),
            'updated': row.get('updated'),
        }
        for index, row in enumerate(raw_data)
    ]

    page = request.GET.get('page', 1)
    per_page = int(request.GET.get('per_page', 10))
    paginator = Paginator(data, per_page)
    accounts = paginator.get_page(page)

    edit_row = request.GET.get('edit_row')

    edit_data = None
    if edit_row:
        try:
            # แปลง edit_row ที่ส่งมา (เลขแถวจริงในชีต) เป็น index ของ list raw_data
            row_index = int(edit_row) - 2  # เพราะ header อยู่แถว 1, data เริ่มแถว 2
            if 0 <= row_index < len(raw_data):
                edit_data = raw_data[row_index]
        except (ValueError, IndexError):
            edit_data = None  # ถ้าเลขแถวผิดพลาด ไม่ต้องแสดง modal หรือ ข้อมูล

    return render(request, 'account_list.html', {
        'accounts': accounts,
        'username': username,
        'per_page': per_page,
        'edit_row': edit_row,
        'edit_data': edit_data,  # ส่งข้อมูลแถวที่จะแก้ไขไปด้วย
        'categories': list(set(row.get('category') for row in raw_data if row.get('category'))),
    })




@csrf_exempt
def account_create_view(request):
    if request.method == 'POST':
        username = request.session.get('username')
        datetime_val = request.POST.get('datetime')
        details = request.POST.get('details')
        amount = request.POST.get('amount')
        type_val = request.POST.get('type')
        category = request.POST.get('category')

        created_at = now().strftime('%Y-%m-%d %H:%M:%S')
        new_row = [
            datetime_val,
            details,
            amount,
            type_val,
            category,
            username,
            created_at,
            '', '',  # updated_by, updated
        ]
        account_sheet.add_row(new_row)

        messages.success(request, 'เพิ่มบัญชีเรียบร้อยแล้ว ✅')
        return redirect('/account/')
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)



@csrf_exempt
def account_update_view(request, row_number):
    if request.method == 'POST':
        username = request.session.get('username')
        datetime_val = request.POST.get('datetime')
        details = request.POST.get('details')
        amount = request.POST.get('amount')
        type_val = request.POST.get('type')
        category = request.POST.get('category')

        all_rows = account_sheet.get_all_data()

        # แปลงเลขแถว Google Sheets เป็น index ของ list
        index = row_number - 2  
        if index < 0 or index >= len(all_rows):
            messages.error(request, 'เลขแถวข้อมูลไม่ถูกต้อง')
            return redirect('/account/')

        row = all_rows[index]
        print(row)

        row['datetime'] = datetime_val
        row['details'] = details
        row['amount'] = amount
        row['type'] = type_val
        row['category'] = category
        row['updated_by'] = username
        row['updated'] = now().strftime('%Y-%m-%d %H:%M:%S')

        header = ['id','datetime', 'details', 'amount', 'type', 'category', 'created_by', 'created', 'updated_by', 'updated']
        row_list = [row.get(col, '') for col in header]

        # เรียก update โดยใช้ row_number เดิม (เลขแถว Google Sheets)
        account_sheet.update_row(row_number, row_list)

        messages.success(request, 'แก้ไขข้อมูลเรียบร้อยแล้ว')
        return redirect('/account/')


@csrf_exempt
def account_delete_view(request, row_number):
    if request.method == 'POST':
        account_sheet.delete_row(row_number)
        messages.success(request, 'ลบข้อมูลเรียบร้อยแล้ว')
        return redirect('/account/')
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
