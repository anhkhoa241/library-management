# apps/library/forms/staff_forms.py
from django import forms
from ..models import Sach, PhieuNhap

class NhapSachForm(forms.Form):
    sach = forms.ModelChoiceField(
        queryset=Sach.objects.all(),
        label="Chọn sách",
        empty_label="-- Chọn sách --"
    )
    so_luong_nhap = forms.IntegerField(min_value=1, label="Số lượng nhập")
    hinh_thuc_nhap = forms.ChoiceField(
        choices=PhieuNhap.HINH_THUC_NHAP_CHOICES,
        label="Hình thức nhập"
    )
    nha_cung_cap = forms.CharField(max_length=200, required=False, label="Nhà cung cấp")
    so_chung_tu = forms.CharField(max_length=200, required=False, label="Số chứng từ")
    ghi_chu = forms.CharField(widget=forms.Textarea, required=False, label="Ghi chú")

class GiaHanTheForm(forms.Form):
    ma_doc_gia = forms.IntegerField(label="Mã độc giả", min_value=1)
    so_thang = forms.IntegerField(label="Số tháng gia hạn", initial=12, min_value=1)