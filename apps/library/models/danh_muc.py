# CAC BANG THE LOAI, KE, THU VIEN LIEN KET

from django.db import models

# The loai
class TheLoai(models.Model):
    # Ten the loai khong duoc phep trung voi nhau
    ten_the_loai = models.CharField(
        max_length= 100,
        unique=True, # Dam bao khong co the loai nao trung nhau
        verbose_name="Tên thể loại"
    )
    # Mo ta them, co the de trong
    mo_ta = models.TextField(
        blank=True, # Cho phep de trong
        null=True,
        verbose_name="Mô tả"
    )

    class Meta:
        db_table = 'TheLoai'    # Ten bang trong DATABASE
        verbose_name = 'Thể loại'   # Ten so it
        verbose_name_plural = 'Thể loại'    # Ten so nhieu
    
    def __str__(self):
        return self.ten_the_loai
    
# Ke sach
class Ke(models.Model):
    LOAI_KE_CHOICES = [
        ('Thuong', 'Thường'),
        ('Dac biet', 'Đặc biệt'),
        ('Tai lieu so', 'Tài liệu số'),
    ]

    loai_ke = models.CharField(
        max_length=30,
        choices=LOAI_KE_CHOICES,
        default='Thuong',
        verbose_name="Loại kệ" 
    )
    vi_tri = models.CharField(
        max_length=100,
        verbose_name="Vị trí"
    )
    suc_chua_toi_da = models.PositiveIntegerField(
        verbose_name="Sức chứa tối đa"
    )
    so_luong_hien_tai = models.PositiveIntegerField(
        default=0,
        verbose_name="Số lượng hiện tại"
    )

    class Meta:
        db_table = 'Ke'
        verbose_name = 'Kệ'
        verbose_name_plural = 'Kệ'

    def __str__(self):
        return f"{self.loai_ke} - {self.vi_tri}"
    
# Thu vien lien ket
class ThuVienLienKet(models.Model):
    ten_thu_vien = models.CharField(
        max_length=200,
        verbose_name="Tên thư viện"
    )
    dia_chi = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Địa chỉ"
    )
    chinh_sach_muon = models.TextField(
        blank=True,
        null=True,
        verbose_name="Chính sách mượn"
    )
    dang_hoat_dong = models.BooleanField(
        default=True,
        verbose_name="Đang hoạt động"
    )

    class Meta:
        db_table = 'ThuVienLienKet'
        verbose_name = 'Thư viện liên kết'
        verbose_name_plural = 'Thư viện liên kết'

    def __str__(self):
        return self.ten_thu_vien



