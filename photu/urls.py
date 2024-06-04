from django.urls import path
from . import views

urlpatterns = [
    path('',views.getPhotos,name='get-photos'),
    path('get/',views.getSomePhotos,name='get-photos'),
    path('upload/',views.upload,name='upload-photos'),
    path('download/<int:id>/<int:typ>/',views.download,name='upload-photos'),
    path('delete/<int:id>/',views.deletePhoto,name='delete-photo'),
]
