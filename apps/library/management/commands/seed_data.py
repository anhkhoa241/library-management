from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from apps.library.models import (
    TheLoai, Ke, ThuVienLienKet, NhanVien, Sach,
    DocGia, The, PhieuMuon, ChiTietMuon, PhieuTra, PhieuNhap
)

class Command(BaseCommand):
    help = 'Nạp dữ liệu mẫu cho hệ thống thư viện'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Đang nạp dữ liệu mẫu...')

        # ---------- 1. Thể loại (12) ----------
        theloai_data = [
            ('Công nghệ thông tin', 'Lập trình, mạng máy tính, trí tuệ nhân tạo'),
            ('Toán học', 'Giải tích, đại số, xác suất thống kê'),
            ('Vật lý', 'Vật lý đại cương, lý thuyết, ứng dụng'),
            ('Văn học Việt Nam', 'Tiểu thuyết, truyện ngắn, thơ ca'),
            ('Văn học nước ngoài', 'Tác phẩm văn học dịch'),
            ('Kinh tế - Quản trị', 'Kinh tế vi mô, vĩ mô, quản trị'),
            ('Kỹ năng sống', 'Phát triển bản thân, tư duy'),
            ('Lịch sử - Địa lý', 'Lịch sử, địa lý'),
            ('Luật - Chính trị', 'Giáo trình luật, chính trị'),
            ('Khoa học tự nhiên', 'Hóa học, sinh học, môi trường'),
            ('Sách đặc biệt', 'Tài liệu quý hiếm, bách khoa thư'),
            ('Tài liệu số', 'Sách điện tử, tạp chí số'),
        ]
        theloai_objs = []
        for ten, mota in theloai_data:
            obj, created = TheLoai.objects.get_or_create(ten_the_loai=ten, defaults={'mo_ta': mota})
            theloai_objs.append(obj)
            if created: self.stdout.write(f'  + Thể loại: {ten}')

        # ---------- 2. Kệ (5) ----------
        ke_data = [
            ('Thuong', 'Tầng 1 - Khu A', 200),
            ('Thuong', 'Tầng 1 - Khu B', 200),
            ('Thuong', 'Tầng 2 - Khu C', 150),
            ('Dac biet', 'Tầng 2 - Phòng VIP', 50),
            ('Tai lieu so', 'Máy chủ số hóa', 9999),
        ]
        ke_objs = []
        for loai, vitri, succhua in ke_data:
            obj, created = Ke.objects.get_or_create(
                loai_ke=loai, vi_tri=vitri,
                defaults={'suc_chua_toi_da': succhua, 'so_luong_hien_tai': 0}
            )
            ke_objs.append(obj)
            if created: self.stdout.write(f'  + Kệ: {vitri}')

        # ---------- 3. Nhân viên + User (3) ----------
        nv_data = [
            ('Nguyễn Thị Lan', 'Thu thu', 'Ghi', 'lan.nguyen@library.vn', 'thuthu1'),
            ('Trần Văn Minh', 'Nhap sach', 'Ghi', 'minh.tran@library.vn', 'nhap_sach'),
            ('Lê Quốc Hùng', 'Quan ly kho', 'Quan tri', 'hung.le@library.vn', 'quanlykho'),
        ]
        for hoten, bophan, quyen, email, username in nv_data:
            user, created = User.objects.get_or_create(username=username, defaults={
                'is_staff': True,
                'email': email
            })
            if created:
                user.set_password('123456')  # mật khẩu chung dễ test
                user.save()
            nv, created = NhanVien.objects.get_or_create(user=user, defaults={
                'ho_ten': hoten,
                'bo_phan': bophan,
                'quyen_han': quyen,
                'email': email,
                'dang_lam_viec': True
            })
            if created: self.stdout.write(f'  + Nhân viên: {hoten} (user: {username}, pass: 123456)')

        # ---------- 4. Độc giả + User + Thẻ (4) ----------
        dg_data = [
            ('Nguyễn Văn An', '2002-05-15', 'Sinh vien', 'docgia1'),
            ('Trần Thị Bình', '2001-08-20', 'Sinh vien', 'docgia2'),
            ('Lê Văn Cường', '1985-03-10', 'Giang vien', 'giangvien1'),
            ('Phạm Thị Dung', '1990-11-25', 'Khach ben ngoai', 'khach1'),
        ]
        docgia_objs = []
        for hoten, ngaysinh, loai, username in dg_data:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password('123456')
                user.save()
            dg, created = DocGia.objects.get_or_create(user=user, defaults={
                'ho_ten': hoten,
                'ngay_sinh': ngaysinh,
                'loai_doc_gia': loai,
                'email': f'{username}@example.com'
            })
            docgia_objs.append(dg)
            if created:
                # Tạo thẻ thư viện
                The.objects.get_or_create(ma_doc_gia=dg, defaults={
                    'ngay_cap': timezone.now().date(),
                    'ngay_het_han': timezone.now().date() + timedelta(days=365),
                    'loai_the': 'VIP' if loai == 'Giang vien' else 'Thuong',
                    'trang_thai': 'Hop le'
                })
                self.stdout.write(f'  + Độc giả: {hoten} (user: {username}, pass: 123456)')

        # ---------- 5. Sách (7) ----------
        sach_data = [
            ('Lập trình C căn bản', 'Phạm Văn Ất', 0, 2018, 'NXB KHKT', 5, 'Mua', 'Thuong', 0),
            ('Cơ sở dữ liệu', 'Hồ Thuận', 0, 2020, 'NXB ĐHQG', 3, 'Mua', 'Thuong', 0),
            ('Giải tích 1', 'Nguyễn Đình Trí', 1, 2019, 'NXB GD', 2, 'Tang', 'Thuong', 1),
            ('Truyện Kiều', 'Nguyễn Du', 3, 2015, 'NXB Văn học', 4, 'Mua', 'Thuong', 1),
            ('Nhà giả kim', 'Paulo Coelho', 4, 2020, 'NXB Văn học', 5, 'Mua', 'Thuong', 1),
            ('Sách VIP chỉ dành cho giảng viên', 'Tác giả VIP', 10, 2020, 'VIP', 1, 'Mua', 'Dac biet', 3),
            ('Ebook Machine Learning', 'Sebastian Raschka', 11, 2022, 'Packt', 0, 'Mua', 'Tai lieu so', 4),
        ]
        sach_objs = []
        for ten, tacgia, tl_idx, nam, nxb, sl, hinhthuc, loai, ke_idx in sach_data:
            obj, created = Sach.objects.get_or_create(ten_sach=ten, defaults={
                'tac_gia': tacgia,
                'ma_the_loai': theloai_objs[tl_idx],
                'nam_xuat_ban': nam,
                'nha_xuat_ban': nxb,
                'so_luong': sl,
                'hinh_thuc_nhap': hinhthuc,
                'loai_sach': loai,
                'ma_ke': ke_objs[ke_idx],
            })
            sach_objs.append(obj)
            if created: self.stdout.write(f'  + Sách: {ten} (SL:{sl})')

        self.stdout.write(self.style.SUCCESS('✅ Đã nạp dữ liệu mẫu thành công!'))
        self.stdout.write('🔑 Tài khoản test:')
        self.stdout.write('   - Nhân viên (thủ thư): thuthu1 / 123456')
        self.stdout.write('   - Nhân viên (nhập sách): nhap_sach / 123456')
        self.stdout.write('   - Độc giả (sinh viên): docgia1 / 123456')
        self.stdout.write('   - Độc giả (giảng viên): giangvien1 / 123456')