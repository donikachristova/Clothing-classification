from django.urls import path
from . import views
from  .views import home, upload, result
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home , name='home'),
    path('file-upload', upload , name='upload'),
    path('classification', result , name='result')
]

# urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)