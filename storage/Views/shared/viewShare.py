from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from storage.serializers import SharedFileSerializer
from storage.models import SharedFile, File
from git.extra.config import Configurations
from git.extra.fileManager import FileManager
from .helper import shareFileHelper
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shareFile(request):
    file,sharedWith,anyoneKey=shareFileHelper(request)
    serializer=SharedFileSerializer(data={'anyoneKey':anyoneKey})
    if serializer.is_valid():
        serializer.save(sharedWith=sharedWith,file=file)
    return Response(serializer.data)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def removePermission(request,id):
    user = request.user

    try:
        sharedFileByMe=SharedFile.objects.get(file__user=user, id=id)
        sharedFileByMe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadSharedFile(request,id):
    user = request.user
    if id.isnumeric():
        sharedFileToMe=SharedFile.objects.get(sharedWith=user, file__id=id)
    else:
        sharedFileToMe=SharedFile.objects.get(anyoneKey=id)
        
    file=sharedFileToMe.file
    fm=FileManager(file.user.username)
    file_content=fm.download(file.fileId)
    if not file_content: return Response({'error':'something went wrong'},status=400)
    response = HttpResponse(file_content, content_type='application/octet-stream')
    return response

