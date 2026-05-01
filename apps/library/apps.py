from django.apps import AppConfig

class LibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.library'  # <-- Phải ghi đầy đủ đường dẫn thư mục thế này
    label = 'library_app'  # <-- (Mẹo) Thêm dòng này nếu vẫn bị báo trùng tên