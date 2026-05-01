from django.db import transaction
from ..models import Sach, PhieuNhap, NhanVien

class ImportService:

    @ staticmethod
    def import_book(nhan_vien_user, ma_sach, so_luong, hinh_thuc, nha_cung_cap='', so_chung_tu='', ghi_chu=''):
        try:
            with transaction.atomic():
                sach = Sach.objects.get(pk=ma_sach)
                sach.so_luong += so_luong
                sach.save()

                # nv = NhanVien.objects.filter(user=nhan_vien_user).filter()
                nv = NhanVien.objects.get(user=nhan_vien_user)
                PhieuNhap.objects.create(
                    ma_sach=sach,
                    hinh_thuc_nhap=hinh_thuc,
                    so_luong_nhap=so_luong,
                    nha_cung_cap=nha_cung_cap,
                    so_chung_tu=so_chung_tu,
                    ghi_chu=ghi_chu,
                    ma_nhan_vien=nv
                )
                return True, f"Nhập {so_luong} cuốn '{sach.ten_sach}' thành công."
            
        except Sach.DoesNotExist:
            return False, "Sách không tồn tại."
        except Exception as e:
            return False, f"Lỗi: {str(e)}"