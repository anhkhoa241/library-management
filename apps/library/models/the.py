from django.db import models
from .nguoi_dung import DocGia

class The(models.Model):
    LOAI_THE_CHOICES = [
        ('Thuong', 'Thường'),
        ('VIP', 'VIP'),
        ('Lien ket', 'Liên kết'),
    ]
    TRANG_THAI_CHOICES = [
        ('Hop le', 'Hợp lệ'),
        ('Het han', 'Hết hạn'),
        ('Bi khoa', 'Bị khóa'),
    ]

    ma_doc_gia = models.OneToOneField(
        DocGia,
        on_delete=models.CASCADE,
        verbose_name="Độc giả"
    )

    ngay_cap = models.DateField(
        auto_now_add=True,
        verbose_name="Ngày cấp"
    )

    ngay_het_han = models.DateField(
        verbose_name="Ngày hết hạn"
    )

    loai_the = models.CharField(
        max_length=20,
        choices=LOAI_THE_CHOICES,
        verbose_name="Loại thẻ"
    )

    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default='Hop le',
        verbose_name="Trạng thái"
    )

    class Meta:
        db_table = 'The'
        verbose_name = 'Thẻ'
        verbose_name_plural = 'Thẻ'

    def __str__(self):
        return f"Thẻ {self.loai_the} của {self.ma_doc_gia.ho_ten}"