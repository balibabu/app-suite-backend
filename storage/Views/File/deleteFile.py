from rest_framework.response import Response
from storage.models import File
from git.models import Chunk
from git.extra.chunkManager import ChunkManager


def delete_file(user,file_id):
    file=File.objects.get(id=file_id,user=user)
    if file:
        fileId=file.fileId
        chunks=Chunk.objects.filter(fileId=fileId)
        chm=ChunkManager(user.username)
        for chunk in chunks:
            chm.delete(chunk.id)
        fileId.delete()
        return Response(status=204)
    else:
        return Response(status=401)