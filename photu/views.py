from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import PhotoSerializer
from .models import Photo
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from git.extra.fileManager import FileManager
from .utility.thumbnail import Thumbnail


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getPhotos(request):
    user=request.user
    photos=Photo.objects.filter(user=user).order_by('-id')
    serializer=PhotoSerializer(photos,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload(request):
    user=request.user
    file = request.FILES.get('file')
    fileContent=file.read()
    fm=FileManager(user.username)
    compressed=Thumbnail(fileContent,size=(4000,4000))
    original=fm.upload([compressed.thumbnail()])
    img=Thumbnail(fileContent)
    thumbnail=fm.upload([img.thumbnail()])
    width,height=compressed.resolution()
    serializer=PhotoSerializer(data={'title':file.name,'size':len(compressed.thumbnail()),'width':width,'height':height})
    if serializer.is_valid():
        serializer.save(user=user,original=original,thumbnail=thumbnail)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def download(request,id,typ):
    user=request.user
    photo=Photo.objects.get(id=id)
    if typ==1:
        fileId=photo.original
    else:
        fileId=photo.thumbnail
    fm=FileManager(user.username)
    file_content=fm.download(fileId)
    response = HttpResponse(file_content, content_type='application/octet-stream')
    return response


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deletePhoto(request,id): 
    user=request.user
    photo=Photo.objects.get(id=id)
    fm=FileManager(user.username)
    fm.delete(photo.original) # photo cascade w.r.t original/thumbnail
    fm.delete(photo.thumbnail)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSomePhotos(request):
    user=request.user
    ids=request.data.get('ids')
    photos=Photo.objects.filter(user=user).order_by('-id')
    serializer=PhotoSerializer(photos,many=True)
    filteredList=[]
    for photo in serializer.data:
        if photo['id'] not in ids:
            filteredList.append(photo)
    return Response(filteredList)