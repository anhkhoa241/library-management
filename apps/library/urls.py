# apps/library/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import auth_views as lib_auth_views
from .views import reader_views
from .views import staff_views

urlpatterns = [
    # ---------- TRANG CHỦ ----------
    path('', reader_views.home, name='home'),

    # ---------- SÁCH ----------
    path('sach/', reader_views.book_list, name='book_list'),
    path('sach/<int:pk>/', reader_views.book_detail, name='book_detail'),

    # ---------- MƯỢN / TRẢ (ĐỘC GIẢ) ----------
    path('muon-sach/<int:book_id>/', reader_views.borrow_book, name='borrow_book'),
    path('lich-su-muon/', reader_views.borrow_history, name='borrow_history'),
    path('tra-sach/<int:phieu_id>/', reader_views.return_book, name='return_book'),

    # ---------- XÁC THỰC ----------
    path('dang-ky/', lib_auth_views.register, name='register'),
    path('dang-nhap/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('dang-xuat/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # ---------- NHÂN VIÊN ----------
    path('nhan-vien/dashboard/', staff_views.dashboard, name='dashboard'),
    path('nhan-vien/danh-sach-muon/', staff_views.staff_borrow_list, name='staff_borrow_list'),
    path('nhan-vien/tra-sach/<int:phieu_id>/', staff_views.staff_return_book, name='staff_return_book'),
    path('nhan-vien/nhap-sach/', staff_views.staff_nhap_sach, name='staff_nhap_sach'),
    path('nhan-vien/gia-han-the/', staff_views.staff_gia_han_the, name='staff_gia_han_the'),
]