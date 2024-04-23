from rest_framework.response import Response
from django.http import HttpResponse
from storage.models import File
from git.models import Chunk
from git.extra.chunkManager import ChunkManager

def get_chunk_list(file_id):
    file=File.objects.get(id=file_id)
    chunks=Chunk.objects.filter(fileId=file.fileId)
    cids=[chunk.id for chunk in chunks]
    return Response(cids)

def download_chunk(user,chunkId):
    ch=ChunkManager(user.username)
    file_content=ch.download(chunkId)
    if not file_content: return Response({'error':'something went wrong'},status=400)
    response = HttpResponse(file_content, content_type='application/octet-stream')
    return response