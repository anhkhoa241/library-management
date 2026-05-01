from django.utils import timezone
from django.db import transaction
from ..models import PhieuMuon, PhieuTra

class ReturnService:

    @staticmethod
    def return_book(user, phieu_id, tinh_trang='Binh thuong', phi_hu_hong=0):
        try:
            with transaction.atomic():
                phieu = PhieuMuon.objects.get(pk=phieu_id)

                # Kiem tra quyen
                if not user.is_staff and phieu.ma_doc_gia.user != user:
                    return False, "Bạn không có quyền trả phiếu này.", None
                
                if phieu.trang_thai == 'Da tra':
                    return False, "Phiếu đã được trả trước đó.", None
                
                today = timezone.now().date()
                phi_tre = 0
                if today > phieu.ngay_tra_du_kien:
                    so_ngay = (today - phieu.ngay_tra_du_kien).days
                    phi_tre = so_ngay * 5000

                # Tao phieu tra
                phieu_tra = PhieuTra.objects.create(
                    ma_phieu_muon=phieu,
                    ngay_tra=today,
                    tinh_trang_sach=tinh_trang,
                    phi_tre_han=phi_tre,
                    phi_hu_hong=phi_hu_hong
                )
                phieu.trang_thai = 'Da tra'
                phieu.save()

                # Hoan kho neu sach khong mat
                if tinh_trang != 'Mat':
                    for ct in phieu.chitietmuon_set.all():
                        sach = ct.ma_sach
                        sach.so_luong += ct.so_luong
                        sach.save()

                tong_phi = phi_tre + phi_hu_hong
                return True, f"Trả sách thành công. Tổng phí: {tong_phi} VND", phieu_tra.id
            
        except PhieuMuon.DoesNotExist:
            return False, "Phiếu mượn không tồn tại.", None
        
        except Exception as e:
            return False, f"Lỗi: {str(e)}", None