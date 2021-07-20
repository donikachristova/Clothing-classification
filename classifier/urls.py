from django.urls import path
from . import views
from  .views import home, upload, result


urlpatterns = [
    path('', home , name='home'),
    path('file-upload', upload , name='upload'),
    path('classification', result , name='result')
]
