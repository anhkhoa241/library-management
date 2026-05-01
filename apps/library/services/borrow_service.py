from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from .card_service import CardService
from ..models import PhieuMuon, ChiTietMuon, Sach, DocGia, The

class BorrowService:
    
    @staticmethod
    def borrow_book(user, book_id, hinh_thuc_muon='Mang ve'):
        try:
            with transaction.atomic():
                # 1. Lay doc gia
                try:
                    doc_gia = user.docgia
                except DocGia.DoesNotExist:
                    return False, "Tài khoản chưa liên kết với độc giả.", None
                
                # 2. Kiem tra the (su dung CardSevice)
                valid, msg = CardService.check_card_valid(doc_gia)
                if not valid:
                    return False, msg, None
                
                # 3. Lay sach
                try:
                    sach = Sach.objects.get(pk=book_id)
                except Sach.DoesNotExist:
                    return False, "Sách không tồn tại.", None
                
                if sach.so_luong < 1:
                    return False, "Sách đã hết.", None
                
                # 4. Kiem tra da muon cuon nay da tra chua
                if PhieuMuon.objects.filter(
                    ma_doc_gia=doc_gia,
                    chitietmuon__ma_sach=sach,
                    trang_thai__in=['Dang muon', 'Qua han']
                ).exists():
                    return False, f"Bạn đang mượn '{sach.ten_sach}' và chưa trả.", None
                
                # 5. Kiem tra sach dac biet
                the = The.objects.get(ma_doc_gia=doc_gia)
                if sach.loai_sach == 'Dac biet':
                    if the.loai_the != 'VIP' and doc_gia.loai_doc_gia != 'Giang vien':
                        return False, "Sách đặc biệt chỉ dành cho thẻ VIP hoặc Giảng viên.", None
                    
                # 6. Hinh thuc muon cho tai lieu so
                if sach.loai_sach == 'Tai lieu so':
                    hinh_thuc_muon = 'Online'

                # 7. Tinh ngay tra du kien
                if doc_gia.loai_doc_gia == 'Giang vien':
                    ngay_tra = timezone.now().date() + timedelta(days=30)
                elif doc_gia.loai_doc_gia == 'Sinh vien':
                    ngay_tra = timezone.now().date() + timedelta(days=14)
                else:
                    ngay_tra = timezone.now().date() + timedelta(days=7)

                # 8. Tao phieu muon va chi tiet
                phieu = PhieuMuon.objects.create(
                    ma_doc_gia=doc_gia,
                    ngay_muon=timezone.now().date(),
                    ngay_tra_du_kien=ngay_tra,
                    hinh_thuc_muon=hinh_thuc_muon,
                    trang_thai='Dang muon'
                )
                ChiTietMuon.objects.create(
                    ma_phieu_muon=phieu,
                    ma_sach=sach,
                    so_luong=1
                )

                # 9. Giam kho
                sach.so_luong -= 1
                sach.save()

                return True, f"Mượn '{sach.ten_sach}' thành công. Hạn trả: {ngay_tra.strftime('%d/%m/%Y')}", phieu.id
            
        except Exception as e:
            return False, f"Lỗi: {str(e)}", None

                

