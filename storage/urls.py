from django.urls import path
from .Views.File.view_create import uploadFile,uploadToGit,getAndCreateFile,cleanUp
from .Views.File.view_rud import getChunksOfaFile, downloadChunk, UpdateFileView, deleteFile
from .Views.view_readFF import getFilesAndFolders
from .Views.Folder.views import FolderListCreateView, FolderUpdateDeleteView
from .Views.shared import viewShare


urlpatterns = [
## Upload File
    path('upload/',uploadFile,name='uploadFile'),
    path('upload/<int:id>/',uploadToGit,name='uploadToGit'),
    path('get/file/<int:id>/',getAndCreateFile,name='getAndCreateFile'),
    path('cleanup/',cleanUp,name='cleanUp'),

## Update, Delete File
    path('file/<int:pk>/',UpdateFileView.as_view(),name='file-update'),
    path('delete/<int:id>/',deleteFile,name='deleteFile'),

## Download File
    path('chunks/<int:id>/',getChunksOfaFile,name='getChunksOfaFile'),
    path('download/chunk/<int:id>/',downloadChunk,name='downloadChunk'),

## CRUD Folder
    path('folder/',FolderListCreateView.as_view(),name='folder-create-list'),
    path('folder/<int:pk>/',FolderUpdateDeleteView.as_view(),name='folder-update-delete'),

## Get Files and Folders
    path('filesAndFolders/',getFilesAndFolders,name='getFilesAndFolders'),

## file sharing
    path('share/',viewShare.shareFile,name='shareFile'),
    path('revoke/<int:id>/',viewShare.removePermission,name='removePermission'),
    path('dsf/<str:id>/',viewShare.downloadSharedFile,name='downloadSharedFile'),
]