from rest_framework.response import Response
from storage.serializers import FileSerializer
from git.extra.fileInProgressManager import create_fip, store_chunk, upload_chunk, complete_cleanup
from storage.models import File
from git.extra.config import Configurations


def upload(request):
    file = request.FILES.get('file')
    if file:
        content=file.read()
        fipId=request.data.get('key')
        index=request.data.get('index') 
        return receive_chunk(content,fipId,index)
    else:
        return receive_file_info(request)


def receive_file_info(request):
    user=request.user
    size=int(request.data.get('size'))
    filename=request.data.get('filename')
    inside=None if request.data.get('inside')=='null' else request.data.get('inside')

    fip=create_fip(size,user)
    File.objects.create(
        title=filename,
        size=size,
        inside=inside,
        fileId=fip.fileId,
        user=user
    )
    return Response({'key':fip.id,'max-chunk-size':Configurations.MAX_GIT_FILE_SIZE})


def receive_chunk(content,fipId,index):
    chunkId=store_chunk(content,fipId)
    return Response({'chunkId':chunkId})


def upload_to_git(chunkId):
    upload_chunk(chunkId)
    return Response('chunk-uploaded-to-git')


def get_file_instance(user,fipId):
    fileId=complete_cleanup(fipId)
    file=File.objects.get(user=user,fileId=fileId)
    if file:
        serializer = FileSerializer(file)
        return Response(serializer.data)
    return Response(status=404)
