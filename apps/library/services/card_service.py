from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from ..models import DocGia, The

class CardService:
    """
    LOP DICH VU QUAN LY THE
    - Vai tro: thay the cho cac Stored Procedure (SP_GiaHanThe) va Triggers trong Database
    - Giup tap trung logic vao mot cho, de bao tri va nang cap
    """
    @staticmethod
    def check_card_valid(doc_gia):
        """
        - Kiem tra xem the co du dieu kien de muon sach hay khong,
        (Tuong duong voi logic kiem tra dieu kien trong SP_MuonSach)
        """
        try:
            # Tim the dua tren thong tin Doc Gia truyen vao
            the = The.objects.get(ma_doc_gia=doc_gia)
        except The.DoesNotExist:
            return False, "Độc giả chưa có thẻ thư viện."
        
        # Kiem tra the neu the dang bi khoa (Vi du do vi pham noi quy)
        if the.trang_thai == 'Bi khoa':
            return False, "Thẻ đang bị khóa."
        
        # Kiem tra han su dung cua The
        if the.trang_thai == 'Het han' or the.ngay_het_han < timezone.now().date():
            return False, "Thẻ đã hết hạn."

        return True, "Thẻ hợp lệ."
    
    @staticmethod
    def extend_card(doc_gia_id, months=12):
        """
        - Gia han them thoi gian su dung cho the.
        (Tuong duong hoan toan voi Stored Procedure: SP_GiaHanThe)
        """
        try:
            # transaction.atomic() giup dam bao tinh toan ven
            # Neu dang gia han ma mat dien hay loi thi du lieu se quay lai luc chua sua (Rollback)
            with transaction.atomic():
                # Tim doc gia va the tuong ung
                doc_gia = DocGia.objects.get(pk=doc_gia_id)
                the = The.objects.get(ma_doc_gia=doc_gia)

                if the.trang_thai == 'Bi khoa':
                    return "Thẻ đang bị khóa, không thể gia hạn.", None
                
                # Tinh ngay het han moi
                if the.ngay_het_han < timezone.now().date():
                    base_date = timezone.now().date()
                else:
                    base_date = the.ngay_het_han
                
                # Cong thuc: Ngay cu + (30 ngay + so thang muon gia han)
                new_expiry = base_date + timedelta(days=30 * months)

                # Cap nhap thong tin moi vao Database
                the.ngay_het_han = new_expiry
                the.trang_thai = 'Hop le' # Sau khi gia han thanh con the se la Hop le
                # the.save() # Luu lai thay doi
                The.objects.filter(pk=the.pk).update(
                    ngay_het_han=new_expiry,
                    trang_thai='Hop le'
                )
                # the.save(update_fields=['ngay_het_han', 'trang_thai'])


                return True, f"Đã gia hạn thẻ đến {new_expiry.strftime('%d/%m/%Y')}", new_expiry
            
        except DocGia.DoesNotExist:
            return False, "Không tìm thấy độc giả.", None
        except The.DoesNotExist:
            return False, "Độc giả chưa có thẻ.", None

    @staticmethod
    def create_card_for_reader(doc_gia, loai_the='Thuong',days_valid=365):
        """
        - Tu dong tao the moi khi co doc gia dang ky
        """
        # Ngay het han mac dinh la 1 nam (365 ngay) ke tu luc tao
        ngay_het_han = timezone.now().date() + timedelta(days=days_valid)
        
        # Tao moi mot dong trong bang The
        the = The.objects.create(
            ma_doc_gia=doc_gia,
            ngay_cap=timezone.now().date(),
            ngay_het_han=ngay_het_han,
            loai_the=loai_the,
            trang_thai='Hop le'
        )
        return the