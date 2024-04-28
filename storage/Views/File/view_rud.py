from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from storage.serializers import FileSerializer
from rest_framework import generics
from storage.models import File

from .downloadFile import get_chunk_list, download_chunk, download_small_file
from .deleteFile import delete_file


############################### DOWNLOAD ###################################### r

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getChunksOfaFile(request,id):
    user=request.user
    return get_chunk_list(user,id)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadChunk(request,id):
    user = request.user
    return download_chunk(user,id)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def downloadSmallFile(request,id):
    user = request.user
    return download_small_file(user,id)



############################### UPDATE ###################################### u

class UpdateFileView(generics.UpdateAPIView):
    serializer_class=FileSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return File.objects.filter(user=self.request.user)
    


############################### DELETE ###################################### d

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteFile(request,id):  # here if fileId is deleted, file will automatically delete
    user = request.user
    return delete_file(user,id)