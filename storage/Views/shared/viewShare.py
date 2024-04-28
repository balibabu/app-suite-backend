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
from git.models import Chunk
from git.extra.chunkManager import ChunkManager


@api_view(['GET'])
def getFileInfo(request,key):
    try:
        sharedFile=SharedFile.objects.get(anyoneKey=key)
        data={'title':sharedFile.file.title}
        data['size']=sharedFile.file.size
        data['owner']=sharedFile.file.user.username
        data['id']=sharedFile.id
        return Response(data)
    except Exception as e:
        print(e)
        return Response('file doesnt exist', status=404)
    
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shareFile(request):
    file,sharedWith,anyoneKey=shareFileHelper(request)
    try:
        sharedFile=SharedFile.objects.create(
            file=file,
            sharedWith=sharedWith,
            anyoneKey=anyoneKey
        )
        data={'id':sharedFile.id}
        if sharedWith: data['sharedWith']=sharedWith.username
        if anyoneKey: data['anyoneKey']=anyoneKey
        return Response(data)
    except:
        return Response(status=409)

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
def downloadSharedFileChunkList(request,id):
    try:
        if id.isnumeric():
            user = request.user
            sharedFile=SharedFile.objects.get(sharedWith=user,id=id)
        else:
            sharedFile=SharedFile.objects.get(anyoneKey=id)
        file=File.objects.get(id=sharedFile.file.id)
        chunks=Chunk.objects.filter(fileId=file.fileId)
        cids=[chunk.id for chunk in chunks]
        return Response(cids)
    except Exception as e:
        print(e)
        return Response('file doesnt exist', status=404)
    


@api_view(['GET'])
def downloadSharedFileChunk(request,id,cid):
    try:
        if id.isnumeric():
            user = request.user
            sharedFile=SharedFile.objects.get(sharedWith=user,id=id)
        else:
            sharedFile=SharedFile.objects.get(anyoneKey=id)
        ch=ChunkManager(sharedFile.file.user.username)
        file_content=ch.download(cid)
        if not file_content: return Response({'error':'something went wrong'},status=400)
        response = HttpResponse(file_content, content_type='application/octet-stream')
        return response
    except Exception as e:
        print(e)
        return Response('file doesnt exist, or you might not have permission', status=404)

    

# def download_chunk(user,chunkId):
#     ch=ChunkManager(user.username)
#     file_content=ch.download(chunkId)
#     if not file_content: return Response({'error':'something went wrong'},status=400)
#     response = HttpResponse(file_content, content_type='application/octet-stream')
#     return response