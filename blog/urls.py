from django.urls import path
from . import views

urlpatterns = [
    path('',views.getBlogs,name='getBlogs'),
    path('create/',views.createBlog,name='createBlog'),
    path('read/<int:id>/',views.readBlog,name='readBlog'),
    path('update/<int:id>/',views.updateBlog,name='updateBlog'),
    path('delete/<int:id>/',views.deleteBlog,name='deleteBlog'),
]