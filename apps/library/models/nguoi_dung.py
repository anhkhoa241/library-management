from django.db import models
from django.contrib.auth.models import User

# Doc gia
class DocGia(models.Model):
    LOAI_DOC_GIA_CHOICES = [
        ('Sinh vien', 'Sinh viên'),
        ('Giang vien', 'Giảng viên'),
        ('Khach ben ngoai', 'Khách bên ngoài'),
    ]

    # Lien ket 1 - 1 voi User cua Django de xac thuc
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Tài khoản"
    )

    ho_ten = models.CharField(
        max_length=200,
        verbose_name="Họ tên"
    )

    ngay_sinh = models.DateField(
        blank=True,
        null=True,
        verbose_name="Ngày sinh"
    )

    dia_chi = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Địa chỉ"
    )

    email = models.EmailField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Email"
    )

    dien_thoai = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Điện thoại"
    )

    loai_doc_gia = models.CharField(
        max_length=20,
        choices=LOAI_DOC_GIA_CHOICES,
        verbose_name="Loại độc giả"
    )

    tien_coc = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Tiền cọc"
    )

    ngay_tao = models.DateField(
        auto_now_add=True, 
        verbose_name="Ngày tạo"
    )

    class Meta:
        db_table = 'DocGia'
        verbose_name = 'Độc giả'
        verbose_name_plural = 'Độc giả'

    def __str__(self):
        return self.ho_ten
    

# Nhan vien
class NhanVien(models.Model):
    BO_PHAN_CHOICES = [
        ('Thu thu', 'Thủ thư'),
        ('Nhap sach', 'Nhập sách'),
        ('Quan ly kho', 'Quản lý kho'),
    ]
    QUYEN_HAN_CHOICES = [
        ('Doc', 'Đọc'),
        ('Ghi', 'Ghi'),
        ('Quan tri', 'Quản trị'),
    ]

    # Lien ket voi User de nahn vien co the dang nhap duoc
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Tài khoản"
    )

    ho_ten = models.CharField(
        max_length=200,
        verbose_name="Họ tên"
    )
    
    bo_phan = models.CharField(
        max_length=50,
        choices=BO_PHAN_CHOICES,
        verbose_name="Bộ phận"
    )

    quyen_han = models.CharField(
        max_length=30,
        choices=QUYEN_HAN_CHOICES,
        verbose_name="Quyền hạn"
    )

    email = models.EmailField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Email"
    )

    dien_thoai = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Điện thoại"
    )

    dang_lam_viec = models.BooleanField(
        default=True,
        verbose_name="Đang làm việc"
    )

    class Meta:
        db_table = 'NhanVien'
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'

    def __str__(self):
        return self.ho_ten
    
