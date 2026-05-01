# DANG KY MODEL VAO DJANGO ADMIN

from django.contrib import admin
from .models import (
    TheLoai, Ke, ThuVienLienKet,
    Sach, DocGia, NhanVien, The,
    PhieuMuon, ChiTietMuon, PhieuTra, PhieuNhap
)

# Dang ky model don gian
@admin.register(TheLoai)
class TheLoaiAdmin(admin.ModelAdmin):
    list_display = (
        'ten_the_loai', 
        'mo_ta'
    )
    search_field = ('ten_the_loai',)

@admin.register(Ke)
class KeAdmin(admin.ModelAdmin):
    list_display = (
        'loai_ke',
        'vi_tri',
        'suc_chua_toi_da',
        'so_luong_hien_tai'
    )
    list_filter = ('loai_ke',)

@admin.register(ThuVienLienKet)
class ThuVienLienKetAdmin(admin.ModelAdmin):
    list_display = (
        'ten_thu_vien',
        # 'so_ngay_muon_toi_da',
        'dang_hoat_dong'        
    )

@admin.register(Sach)
class SachAdmin(admin.ModelAdmin):
    list_display = (
        'ten_sach',
        'tac_gia',
        'ma_the_loai',
        'so_luong',
        'loai_sach',
        'ma_ke'
    )
    list_filter = (
        'loai_sach',
        'ma_the_loai'
    )
    search_field = (
        'ten_sach',
        'tac_gia'
    )

@admin.register(DocGia)
class DocGiaAdmin(admin.ModelAdmin):
    list_display = (
        'ho_ten',
        'loai_doc_gia',
        'email',
        'dien_thoai',
        'tien_coc'
    )
    list_filter = ('loai_doc_gia',)

@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = (
        'ho_ten',
        'bo_phan',
        'quyen_han',
        'dang_lam_viec'
    )
    list_filter = (
        'bo_phan',
        'dang_lam_viec'
    )

@admin.register(The)
class TheAdmin(admin.ModelAdmin):
    list_display = (
        'ma_doc_gia',
        'loai_the',
        'ngay_cap',
        'ngay_het_han',
        'trang_thai'
    )
    list_filter = (
        'loai_the',
        'trang_thai'
    )

@admin.register(PhieuMuon)
class PhieuMuonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ma_doc_gia',
        'ngay_muon',
        'ngay_tra_du_kien',
        'trang_thai'
    )
    list_filter = (
        'trang_thai',
        'hinh_thuc_muon'
    )

@admin.register(ChiTietMuon)
class ChiTietMuonAdmin(admin.ModelAdmin):
    list_display = (
        'ma_phieu_muon',
        'ma_sach',
        'so_luong'
    )

@admin.register(PhieuTra)
class PhieuTraAdmin(admin.ModelAdmin):
    list_display = (
        'ma_phieu_muon',
        'ngay_tra',
        'tinh_trang_sach',
        'phi_tre_han',
        'phi_hu_hong'
    )

@admin.register(PhieuNhap)
class PhieuNhapAdmin(admin.ModelAdmin):
    list_display = (
        'ma_sach',
        'so_luong_nhap',
        'hinh_thuc_nhap',
        'ngay_nhap',
        'nha_cung_cap'
    )
