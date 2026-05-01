from django.db import models
from .danh_muc import TheLoai, Ke

# Sach
class Sach(models.Model):
    HINH_THUC_NHAP_CHOICES = [
        ('Mua', 'Mua'),
        ('Tang', 'Tặng'),
        ('Lien ket', 'Liên kết'),
    ]
    LOAI_SACH_CHOICES = [
        ('Thuong', 'Thường'),
        ('Dac biet', 'Đặc biệt'),
        ('Tai lieu so', 'Tài liệu số'),
    ]

    ten_sach = models.CharField(
        max_length=300,
        verbose_name="Tên sách"
    )

    tac_gia = models.CharField(
        max_length=200,
        verbose_name="Tác giả"
    )

    # Khoa ngoai den TheLoai
    ma_the_loai = models.ForeignKey(
        TheLoai,
        on_delete=models.PROTECT, # Khong duoc phep xoa the loai neu dang co sach
        verbose_name="Thể loại"
    )

    nam_xuat_ban = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Năm xuất bản"
    )

    nha_xuat_ban = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nhà xuất bản"     
    )

    so_luong = models.PositiveIntegerField(
        default=0,
        verbose_name="Số lượng"
    )

    hinh_thuc_nhap = models.CharField(
        max_length=20,
        choices=HINH_THUC_NHAP_CHOICES, 
        verbose_name="Hình thức nhập"
    )

    loai_sach = models.CharField(
        max_length=20,
        choices=LOAI_SACH_CHOICES, 
        verbose_name="Loại sách"
    )

    # Khoa ngoai den Ke, co the trong
    ma_ke = models.ForeignKey(
        Ke,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Kệ"
    )

    co_the_duoc_in = models.BooleanField(
        default=False,
        verbose_name="Có thể được in"
    )

    ngay_tao = models.DateField(
        auto_now_add=True,
        verbose_name="Ngày tạo"
    )

    class Meta:
        db_table = 'Sach'
        verbose_name = 'Sách'
        verbose_name_plural = 'Sách'
    
    def __str__(self):
        return self.ten_sach

