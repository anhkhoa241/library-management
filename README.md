# 📚 Library Management System – Hệ thống Quản lý Thư viện

**Phiên bản:** 2.0
**Nền tảng:** Django + SQL Server (hỗ trợ SQLite)
**Môn học:** Quản trị Cơ sở Dữ liệu (DBMS)

---

## 📖 Mục lục

- [1. Giới thiệu](#1-giới-thiệu)
- [2. Danh sách chức năng](#2-danh-sách-chức-năng)
- [3. Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
- [4. Cài đặt và chạy](#4-cài-đặt-và-chạy)
- [5. Tài khoản test](#5-tài-khoản-test)
- [6. Hướng dẫn sử dụng](#6-hướng-dẫn-sử-dụng)
- [7. Áp dụng các khái niệm DBMS trong dự án](#7-áp-dụng-các-khái-niệm-dbms-trong-dự-án)
- [8. Xử lý lỗi thường gặp](#8-xử-lý-lỗi-thường-gặp)
- [9. Tài liệu bổ sung](#9-tài-liệu-bổ-sung)

---

## 1. Giới thiệu

Hệ thống Quản lý Thư viện được phát triển bằng Django framework, kết nối với cơ sở dữ liệu SQL Server (có thể chạy với SQLite).  
Hệ thống giúp số hóa toàn bộ quy trình mượn/trả sách, quản lý độc giả, nhân viên, nhập sách, thống kê và báo cáo.  
**Điểm nổi bật:** Dự án minh họa đầy đủ các khái niệm cốt lõi của môn Quản trị Cơ sở Dữ liệu (DBMS) như **ràng buộc, trigger, stored procedure, view, giao tác**. Toàn bộ logic nghiệp vụ được tách biệt khỏi giao diện, tuân thủ kiến trúc 3 lớp (three-tier architecture).

---

## 2. Danh sách chức năng

### 🧑‍🎓 A. Độc giả
- Đăng ký tài khoản (tự động tạo thẻ thư viện 1 năm).
- Đăng nhập / Đăng xuất.
- Xem danh sách sách, tìm kiếm theo tên, tác giả, thể loại.
- Xem chi tiết sách (vị trí kệ, số lượng còn).
- **Mượn sách:** Hệ thống tự kiểm tra thẻ thư viện (hợp lệ, chưa hết hạn), số lượng sách, quyền mượn sách đặc biệt (chỉ VIP/Giảng viên), tài liệu số chỉ được mượn Online.
- Tính ngày trả dự kiến theo loại độc giả (SV: 14 ngày, GV: 30 ngày, Khách: 7 ngày).
- Xem lịch sử mượn/trả cá nhân.
- **Trả sách:** Tự động tính phí trễ hạn (5.000 VND/ngày). Không cho phép trả lại phiếu đã trả.

### 👩‍💼 B. Nhân viên (phân quyền theo bộ phận)
- **Dashboard thống kê:** số phiếu đang mượn, quá hạn, tổng phí phạt trong tháng, top 5 thể loại nhiều sách nhất, danh sách sách sắp hết (< 5 cuốn).
- **Quản lý phiếu mượn:** Xem tất cả phiếu đang mượn/quá hạn, có thể trả sách tại quầy (chọn tình trạng: Bình thường / Hư hỏng / Mất, nhập phí hư hỏng).
- **Nhập sách:** Chọn sách hiện có, nhập số lượng, tạo phiếu nhập.
- **Gia hạn thẻ:** Nhập mã độc giả và số tháng gia hạn.
- **Báo cáo tồn kho:** Xem toàn bộ sách trong thư viện kèm số lượng và vị trí kệ.
- **Báo cáo phí phạt:** Liệt kê chi tiết các phiếu trả có phí, tổng phí.

### 👑 C. Quản trị viên (Admin)
- Truy cập Django Admin (`/admin/`) để quản lý toàn bộ dữ liệu (thêm/sửa/xóa sách, độc giả, nhân viên...).
- Phân quyền nhân viên (gán `Staff status`, phân bộ phận).

---

## 3. Kiến trúc hệ thống

Dự án được tổ chức theo **mô hình 3 lớp (3-tier)**:
- **Presentation Layer:** Templates HTML, Bootstrap 5, Font Awesome.
- **Business Layer:** Django Services (chứa toàn bộ logic tương đương Stored Procedure), Views, Forms.
- **Data Access Layer:** Django ORM hoặc raw SQL (tùy chọn), SQL Server/SQLite.

Cấu trúc thư mục chính:

library_management_system/
├── config/ # Cấu hình Django (settings, urls, wsgi)
│ └── settings/
│ ├── base.py # Cấu hình chung
│ ├── local.py # Cấu hình cho môi trường local (đọc .env)
│ └── production.py # Cấu hình production
├── apps/ # Chứa ứng dụng Django
│ └── library/
│ ├── models/ # Models chia theo chức năng (danh_muc.py, sach.py, docgia.py...)
│ ├── views/ # Views (auth, reader, staff)
│ ├── services/ # Lớp Business Logic (xem phần DBMS)
│ ├── forms/ # Form nhập liệu
│ ├── signals.py # Django Signal (tương đương Trigger)
│ ├── templates/ # Giao diện HTML
│ ├── management/ # Custom commands (seed_data, update_overdue)
│ └── tests/
├── static/ # File tĩnh chung
├── .env # Biến môi trường (KHÔNG commit)
├── .env.example # File mẫu cho người dùng
├── manage.py
├── requirements.txt
└── README.md


---

## 4. Cài đặt và chạy

### 4.1 Yêu cầu hệ thống
- Python 3.8+
- Git
- SQL Server (đã cài đặt và đang chạy) **hoặc** dùng SQLite (không cần cài thêm).
- (Nếu dùng SQL Server) ODBC Driver 18 for SQL Server (hoặc 17).

### 4.2 Clone dự án
```bash
git clone https://github.com/your-username/QuanLyThuVien.git
cd QuanLyThuVien


### 4.3 Tạo môi trường ảo
Tạo và kích hoạt môi trường ảo (virtual environment) để cài đặt các thư viện độc lập cho dự án:
```bash
python -m venv venv

# Kích hoạt trên Windows:
venv\Scripts\activate

# Kích hoạt trên macOS/Linux:
source venv/bin/activate
```

### 4.4 Cài đặt thư viện
Tiến hành cài đặt các gói phụ thuộc (dependencies) cần thiết đã được liệt kê trong file `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4.5 Tạo bảng và tài khoản quản trị
Khởi tạo cấu trúc cơ sở dữ liệu và tạo tài khoản Admin (Superuser) để truy cập trang quản trị:
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4.6 Nạp dữ liệu mẫu (Tùy chọn)
Chạy lệnh sau nếu bạn muốn nạp sẵn một số dữ liệu mẫu (thể loại, kệ sách, danh sách sách...) để test thử hệ thống:
```bash
python manage.py seed_data
```

### 4.7 Chạy server
Cuối cùng, khởi động server Django để bắt đầu trải nghiệm ứng dụng:
```bash
python manage.py runserver
```
