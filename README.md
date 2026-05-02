# 📚 Library Management System – Hệ thống Quản lý Thư viện

**Phiên bản:** 2.0
**Nền tảng:** Django + SQL Server (hỗ trợ SQLite)
**Môn học:** Hệ Quản trị Cơ sở Dữ liệu (DBMS)

---

## 📖 Mục lục

1. [Giới thiệu](#1-giới-thiệu)
2. [Danh sách chức năng](#2-danh-sách-chức-năng)
3. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
4. [Cài đặt và chạy](#4-cài-đặt-và-chạy)
5. [Tài khoản test](#5-tài-khoản-test)
6. [Hướng dẫn sử dụng](#6-hướng-dẫn-sử-dụng)
7. [Áp dụng DBMS](#7-áp-dụng-các-khái-niệm-dbms-trong-dự-án)
8. [Xử lý lỗi](#8-xử-lý-lỗi-thường-gặp)
9. [Tài liệu bổ sung](#9-tài-liệu-bổ-sung)

---

## 1. Giới thiệu

Hệ thống Quản lý Thư viện được phát triển bằng **Django**, kết nối với **SQL Server** (có thể dùng SQLite).

Hệ thống giúp số hóa toàn bộ quy trình:

* 📥 Mượn / Trả sách
* 👤 Quản lý độc giả
* 👨‍💼 Quản lý nhân viên
* 📊 Thống kê & báo cáo

### 🌟 Điểm nổi bật

Dự án minh họa đầy đủ các khái niệm DBMS:

* Ràng buộc (Constraints)
* Trigger
* Stored Procedure
* View
* Giao tác (Transaction)

👉 Logic nghiệp vụ được tách khỏi giao diện theo mô hình **3-tier architecture**

---

## 2. Danh sách chức năng

### 🧑‍🎓 A. Độc giả

* Đăng ký tài khoản (tự động tạo thẻ 1 năm)
* Đăng nhập / Đăng xuất
* Tìm kiếm sách theo:

  * Tên
  * Tác giả
  * Thể loại
* Xem chi tiết sách

#### 📚 Mượn sách

* Kiểm tra:

  * Thẻ hợp lệ
  * Chưa hết hạn
  * Số lượng còn
* Quyền mượn đặc biệt (VIP / Giảng viên)
* Tài liệu số → chỉ mượn Online

#### ⏳ Thời gian mượn

* Sinh viên: 14 ngày
* Giảng viên: 30 ngày
* Khách: 7 ngày

#### 🔁 Trả sách

* Tính phí trễ: **5.000 VND/ngày**
* Không cho trả lại phiếu đã trả

---

### 👩‍💼 B. Nhân viên

#### 📊 Dashboard

* Phiếu đang mượn
* Phiếu quá hạn
* Tổng phí phạt tháng
* Top 5 thể loại
* Sách sắp hết (< 5 cuốn)

#### 📄 Quản lý phiếu

* Xem danh sách phiếu
* Trả sách tại quầy
* Trạng thái:

  * Bình thường
  * Hư hỏng
  * Mất

#### 📦 Nhập sách

* Chọn sách
* Nhập số lượng
* Tạo phiếu nhập

#### ⏱ Gia hạn thẻ

* Nhập mã độc giả
* Chọn số tháng

#### 📈 Báo cáo

* Tồn kho
* Phí phạt

---

### 👑 C. Admin

* Truy cập `/admin/`
* Quản lý toàn bộ dữ liệu
* Phân quyền nhân viên

---

## 3. Kiến trúc hệ thống

Mô hình **3-tier architecture**

| Layer           | Mô tả             |
| --------------- | ----------------- |
| 🎨 Presentation | HTML, Bootstrap 5 |
| ⚙️ Business     | Services, Views   |
| 🗄 Data          | ORM / SQL Server  |

### 📁 Cấu trúc thư mục

```bash
library_management_system/
├── config/
│   └── settings/
│       ├── base.py
│       ├── local.py
│       └── production.py
├── apps/
│   └── library/
│       ├── models/
│       ├── views/
│       ├── services/
│       ├── forms/
│       ├── signals.py
│       ├── templates/
│       ├── management/
│       └── tests/
├── static/
├── .env
├── .env.example
├── manage.py
├── requirements.txt
└── README.md
```

## 4. Cài đặt và chạy

### 4.1 Yêu cầu hệ thống

* Python 3.8+
* Git
* SQL Server (đã cài đặt và đang chạy) **hoặc** dùng SQLite (không cần cài thêm).
* (Nếu dùng SQL Server) ODBC Driver 18 for SQL Server (hoặc 17).

---

### 4.2 Clone dự án

git clone https://github.com/your-username/QuanLyThuVien.git
cd QuanLyThuVien

---

### 4.3 Tạo môi trường ảo

python -m venv venv

# Windows:

venv\Scripts\activate

# macOS/Linux:

source venv/bin/activate

---

### 4.4 Cài đặt thư viện

pip install -r requirements.txt

---

### 4.5 Tạo bảng và tài khoản quản trị

python manage.py migrate
python manage.py createsuperuser

---

### 4.6 Nạp dữ liệu mẫu (Tùy chọn)

python manage.py seed_data

---

### 4.7 Chạy server

python manage.py runserver

Truy cập: http://127.0.0.1:8000

---


## 5. Áp dụng các khái niệm DBMS trong dự án

* Constraints
* Trigger
* Stored Procedure
* View
* Transaction
