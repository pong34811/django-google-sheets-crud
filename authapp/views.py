from config import user_sheet
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
import uuid
from django.utils.timezone import now
# Create your views here.


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        id = str(uuid.uuid4())
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_active = True
        created_by = now().strftime('%Y-%m-%d %H:%M:%S')
        created = username

        if user_sheet.is_username_exists(username):
            messages.error(request, 'ชื่อผู้ใช้นี้มีอยู่แล้ว ❌')
            return redirect('/auth/register/')

        user_sheet.register_user(id, username, password, is_active, created_by, created)
        messages.success(request, 'สมัครสมาชิกสำเร็จแล้ว ✅ กรุณาเข้าสู่ระบบ')
        return redirect('/auth/login/')

    return render(request, 'register.html')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print("username:", username)
        print("password:", password)

        user = user_sheet.find_user_by_credentials(username, password)  # เรียกฟังก์ชันจากโมดูล

        print("matched user:", user)

        if user:
            # อัปเดต last_join
            last_join_time = now().strftime('%Y-%m-%d %H:%M:%S')
            user_sheet.update_last_join(username, last_join_time)

            request.session['username'] = user['username']
            return redirect('/sheet/list/')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
            return redirect('/auth/login/')

    return render(request, 'login.html')

@csrf_exempt
def logout_view(request):
    if 'username' in request.session:
        del request.session['username']
        messages.success(request, 'ออกจากระบบสำเร็จแล้ว ✅')
    else:
        messages.error(request, 'คุณยังไม่ได้เข้าสู่ระบบ ❌')
    return redirect('/auth/login/')