from django.db.models import Count, Sum, F, Q
from django.utils import timezone
from ..models import Sach, TheLoai, PhieuMuon, PhieuTra

class StatisticsService:

    @staticmethod
    def get_dashboard_data():
        today = timezone.now().date()
        dang_muon = PhieuMuon.objects.filter(trang_thai='Dang muon').count()
        qua_han = PhieuMuon.objects.filter(trang_thai='Qua han').count()

        phi_thang = PhieuTra.objects.filter(
            ngay_tra__month=today.month,
            ngay_tra__year=today.year
        ).aggregate(total=Sum(F('phi_tre_han') + F('phi_hu_hong')))['total'] or 0

        theloai_top = TheLoai.objects.annotate(
            so_tua=Count('sach'),
            tong_ban=Sum('sach__so_luong')
        ).order_by('-so_tua')[:5]

        sach_sap_het = Sach.objects.filter(so_luong__lt=5).order_by('so_luong')[:10]

        return {
            'dang_muon': dang_muon,
            'qua_han': qua_han,
            'phi_thang': phi_thang,
            'theloai_top': theloai_top,
            'sach_sap_het': sach_sap_het
        }