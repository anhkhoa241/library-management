# apps/library/forms/auth_forms.py
from django import forms
from django.contrib.auth.models import User
from ..models import DocGia
from ..services.card_service import CardService

class DangKyDocGiaForm(forms.ModelForm):
    # Trường cho User (không có trong model DocGia)
    username = forms.CharField(max_length=150, label="Tên đăng nhập")
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Xác nhận mật khẩu")

    class Meta:
        model = DocGia
        fields = [
            'ho_ten', 'ngay_sinh', 'dia_chi', 'email',
            'dien_thoai', 'loai_doc_gia'
        ]
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên đăng nhập đã tồn tại.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if pwd and confirm and pwd != confirm:
            raise forms.ValidationError("Mật khẩu xác nhận không khớp.")
        return cleaned_data

    def save(self, commit=True):
        # Tạo User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data.get('email', '')
        )
        # Tạo DocGia
        doc_gia = super().save(commit=False)
        doc_gia.user = user
        if commit:
            doc_gia.save()
            # Tạo thẻ thư viện (dùng service)
            CardService.create_card_for_reader(doc_gia)
        return doc_gia