# apps/library/views/reader_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..models import Sach, PhieuMuon
from ..services import BorrowService, ReturnService

# Trang chủ: hiển thị 8 cuốn sách mới nhất
def home(request):
    sach_moi = Sach.objects.order_by('-ngay_tao')[:8]
    return render(request, 'library/home.html', {'sach_moi': sach_moi})

# Danh sách sách (có tìm kiếm)
def book_list(request):
    query = request.GET.get('q', '')
    sach_list = Sach.objects.all()
    if query:
        sach_list = sach_list.filter(
            Q(ten_sach__icontains=query) |
            Q(tac_gia__icontains=query) |
            Q(ma_the_loai__ten_the_loai__icontains=query)
        ).distinct()
    return render(request, 'library/book_list.html', {
        'sach_list': sach_list,
        'query': query
    })

# Chi tiết một cuốn sách
def book_detail(request, pk):
    sach = get_object_or_404(Sach, pk=pk)
    return render(request, 'library/book_detail.html', {'sach': sach})

# Mượn sách
@login_required
def borrow_book(request, book_id):
    success, message, _ = BorrowService.borrow_book(request.user, book_id)
    if success:
        messages.success(request, message)
        return redirect('borrow_history')
    else:
        messages.error(request, message)
        return redirect('book_detail', pk=book_id)

# Lịch sử mượn của độc giả đang đăng nhập
@login_required
def borrow_history(request):
    try:
        doc_gia = request.user.docgia
    except:
        messages.error(request, "Không tìm thấy thông tin độc giả.")
        return redirect('home')
    phieu_list = PhieuMuon.objects.filter(ma_doc_gia=doc_gia).order_by('-ngay_muon')
    return render(request, 'library/borrow_history.html', {'phieu_muon': phieu_list})

# Trả sách
@login_required
def return_book(request, phieu_id):
    success, message, _ = ReturnService.return_book(request.user, phieu_id)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    return redirect('borrow_history')