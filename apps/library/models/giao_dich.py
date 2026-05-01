from django.db import models
from .nguoi_dung import DocGia, NhanVien
from .danh_muc import ThuVienLienKet
from .tai_lieu import Sach

# Bao gom Phieu muon, chi tiet muon

# PhieuMuon
class PhieuMuon(models.Model):
    HINH_THUC_MUON_CHOICES = [
        ('Tai cho', 'Tại chỗ'),
        ('Mang ve', 'Mang về'),
        ('Online', 'Online'),
    ]
    TRANG_THAI_CHOICES = [
        ('Dang muon', 'Đang mượn'),
        ('Qua han', 'Quá hạn'),
        ('Da tra', 'Đã trả'),
    ]

    ma_doc_gia = models.ForeignKey(
        DocGia,
        on_delete=models.PROTECT,
        verbose_name="Độc giả"
    )

    ngay_muon = models.DateField(
        auto_now_add=True,
        verbose_name="Ngày mượn"
    )

    ngay_tra_du_kien = models.DateField(
        verbose_name="Ngày trả dự kiến"
    )

    hinh_thuc_muon = models.CharField(
        max_length=20,
        choices=HINH_THUC_MUON_CHOICES,
        verbose_name="Hình thức mượn"
    )
    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default='Dang muon',
        verbose_name="Trạng thái"
    )

    ma_nhan_vien = models.ForeignKey(
        NhanVien,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Nhân viên xử lý"
    )

    ma_lien_ket = models.ForeignKey(
        ThuVienLienKet,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Thư viện liên kết"
    )

    class Meta:
        db_table = 'PhieuMuon'
        verbose_name = 'Phiếu mượn'
        verbose_name_plural = 'Phiếu mượn'

    def __str__(self):
        return f"Phiếu mượn #{self.id} - {self.ma_doc_gia.ho_ten}"
    

# Chi tiet phieu muon
class ChiTietMuon(models.Model):
    ma_phieu_muon = models.ForeignKey(
        PhieuMuon,
        on_delete=models.CASCADE,
        verbose_name="Phiếu mượn"
    )

    ma_sach = models.ForeignKey(
        Sach,
        on_delete=models.PROTECT,
        verbose_name="Sách"
    )

    so_luong = models.PositiveIntegerField(
        default=1,
        verbose_name="Số lượng"
    )

    class Meta:
        db_table = 'ChiTietMuon'
        verbose_name = 'Chi tiết mượn'
        verbose_name_plural = 'Chi tiết mượn'
        unique_together = ('ma_phieu_muon', 'ma_sach')  # Mỗi sách chỉ xuất hiện 1 lần trong 1 phiếu

    def __str__(self):
        return f"{self.ma_sach.ten_sach} (SL: {self.so_luong})"
    

# Phieu Tra
class PhieuTra(models.Model):
    TINH_TRANG_CHOICES = [
        ('Binh thuong', 'Bình thường'),
        ('Hu hong', 'Hư hỏng'),
        ('Mat', 'Mất'),
    ]

    ma_phieu_muon = models.OneToOneField(
        PhieuMuon,
        on_delete=models.PROTECT,
        verbose_name="Phiếu mượn"
    )

    ngay_tra = models.DateField(
        auto_now_add=True,
        verbose_name="Ngày trả"
    )

    tinh_trang_sach = models.CharField(
        max_length=20,
        choices=TINH_TRANG_CHOICES,
        verbose_name="Tình trạng sách"
    )

    phi_tre_han = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Phí trễ hạn"
    )

    phi_hu_hong = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Phí hư hỏng"
    )

    ghi_chu = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ghi chú"
    )

    class Meta:
        db_table = 'PhieuTra'
        verbose_name = 'Phiếu trả'
        verbose_name_plural = 'Phiếu trả'


# Phieu nhap
class PhieuNhap(models.Model):
    HINH_THUC_NHAP_CHOICES = [
        ('Mua', 'Mua'),
        ('Tang', 'Tặng'),
        ('Lien ket', 'Liên kết'),
    ]

    ma_sach = models.ForeignKey(
        Sach,
        on_delete=models.PROTECT,
        verbose_name="Sách"
    )

    hinh_thuc_nhap = models.CharField(
        max_length=20,
        choices=HINH_THUC_NHAP_CHOICES,
        verbose_name="Hình thức nhập"
    )

    ngay_nhap = models.DateField(
        auto_now_add=True,
        verbose_name="Ngày nhập"
    )

    nha_cung_cap = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nhà cung cấp"
    )

    ma_lien_ket = models.ForeignKey(
        ThuVienLienKet,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Thư viện liên kết"
    )

    so_chung_tu = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Số chứng từ"
    )

    so_luong_nhap = models.PositiveIntegerField(
        verbose_name="Số lượng nhập"
    )

    ma_nhan_vien = models.ForeignKey(
        NhanVien,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Nhân viên nhập"
    )

    ghi_chu = models.TextField(
        blank=True,
        null=True,
        verbose_name="Ghi chú"
    )

    class Meta:
        db_table = 'PhieuNhap'
        verbose_name = 'Phiếu nhập'
        verbose_name_plural = 'Phiếu nhập'