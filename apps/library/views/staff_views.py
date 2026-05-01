# apps/library/views/staff_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from ..models import PhieuMuon, DocGia
from ..forms import NhapSachForm, GiaHanTheForm
from ..services import ReturnService, CardService, ImportService, StatisticsService


@staff_member_required
def dashboard(request):
    """Bảng điều khiển – thống kê nhanh (tương đương các View SQL)"""
    data = StatisticsService.get_dashboard_data()
    return render(request, 'library/staff/dashboard.html', data)


@staff_member_required
def staff_borrow_list(request):
    """Danh sách tất cả phiếu mượn đang hoạt động (tương đương VW_DanhSachMuon)"""
    phieu_list = PhieuMuon.objects.filter(
        trang_thai__in=['Dang muon', 'Qua han']
    ).select_related('ma_doc_gia').prefetch_related('chitietmuon_set__ma_sach')

    today = timezone.now().date()
    for pm in phieu_list:
        if pm.ngay_tra_du_kien < today:
            pm.so_ngay_qua_han = (today - pm.ngay_tra_du_kien).days
        else:
            pm.so_ngay_qua_han = 0

    return render(request, 'library/staff/borrow_list.html', {'phieu_list': phieu_list})


@staff_member_required
def staff_return_book(request, phieu_id):
    """Trả sách tại quầy (nhân viên chọn tình trạng, nhập phí hư hỏng)"""
    phieu_muon = get_object_or_404(PhieuMuon, pk=phieu_id)

    if request.method == 'POST':
        tinh_trang = request.POST.get('tinh_trang')
        phi_hu_hong = int(request.POST.get('phi_hu_hong', 0))
        success, message, _ = ReturnService.return_book(
            user=request.user,
            phieu_id=phieu_id,
            tinh_trang=tinh_trang,
            phi_hu_hong=phi_hu_hong
        )
        if success:
            messages.success(request, message)
            return redirect('staff_borrow_list')
        else:
            messages.error(request, message)

    return render(request, 'library/staff/return_form.html', {'phieu_muon': phieu_muon})


@staff_member_required
def staff_nhap_sach(request):
    """Nhập sách (tương đương SP_NhapSach)"""
    if request.method == 'POST':
        form = NhapSachForm(request.POST)
        if form.is_valid():
            sach = form.cleaned_data['sach']
            so_luong = form.cleaned_data['so_luong_nhap']
            hinh_thuc = form.cleaned_data['hinh_thuc_nhap']
            nha_cung_cap = form.cleaned_data.get('nha_cung_cap', '')
            so_chung_tu = form.cleaned_data.get('so_chung_tu', '')
            ghi_chu = form.cleaned_data.get('ghi_chu', '')

            if not sach:
                messages.error(request, "Vui lòng chọn sách hiện có.")
                return redirect('staff_nhap_sach')

            success, message = ImportService.import_book(
                nhan_vien_user=request.user,
                ma_sach=sach.id,
                so_luong=so_luong,
                hinh_thuc=hinh_thuc,
                nha_cung_cap=nha_cung_cap,
                so_chung_tu=so_chung_tu,
                ghi_chu=ghi_chu
            )
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect('staff_nhap_sach')
    else:
        form = NhapSachForm()
    return render(request, 'library/staff/nhap_sach.html', {'form': form})


@staff_member_required
def staff_gia_han_the(request):
    """Gia hạn thẻ độc giả (tương đương SP_GiaHanThe)"""
    if request.method == 'POST':
        form = GiaHanTheForm(request.POST)
        if form.is_valid():
            ma_doc_gia = form.cleaned_data['ma_doc_gia']
            so_thang = form.cleaned_data['so_thang']
            success, message, _ = CardService.extend_card(ma_doc_gia, so_thang)
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            return redirect('staff_gia_han_the')
    else:
        form = GiaHanTheForm()
    tat_ca = DocGia.objects.all()
    return render(request, 'library/staff/gia_han_the.html', {
        'form': form,
        'tat_ca_doc_gia': tat_ca
    })