from .auth_views import register
from .reader_views import (
    home, book_list, book_detail, borrow_book, borrow_history, return_book
)
from .staff_views import (
    dashboard, staff_borrow_list, staff_return_book,
    staff_nhap_sach, staff_gia_han_the
)