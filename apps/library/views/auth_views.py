# apps/library/views/auth_views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from ..forms import DangKyDocGiaForm

def register(request):
    if request.method == 'POST':
        form = DangKyDocGiaForm(request.POST)
        if form.is_valid():
            # Lưu form – bên trong form.save() sẽ tạo User, DocGia và The
            doc_gia = form.save()
            # Đăng nhập luôn cho người dùng mới
            login(request, doc_gia.user)
            messages.success(request, f"Chào mừng {doc_gia.ho_ten}! Đăng ký thành công.")
            return redirect('home')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin đăng ký.")
    else:
        form = DangKyDocGiaForm()
    return render(request, 'registration/register.html', {'form': form})