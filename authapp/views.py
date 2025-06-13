from config import user_sheet
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render

# Create your views here.


@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if user_sheet.is_username_exists(username):
            messages.error(request, 'ชื่อผู้ใช้นี้มีอยู่แล้ว ❌')
            return redirect('/auth/register/')

        user_sheet.register_user(username, password)
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

        user = user_sheet.find_user_by_credentials(username, password)
        print("matched user:", user)

        if user:
            request.session['username'] = user['username']
            return redirect('/sheet/list/')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
            return redirect('/auth/login/')

    return render(request, 'login.html')