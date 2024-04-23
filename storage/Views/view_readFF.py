from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from storage.serializers import FolderSerializer,  FileSerializer, SharedFileSerializer
from storage.models import Folder, File, SharedFile

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getFilesAndFolders(request):
    user = request.user

    files=File.objects.filter(user=user).order_by('-timestamp')
    file_serializer=FileSerializer(files,many=True)

    folders=Folder.objects.filter(user=user)
    folder_serializer=FolderSerializer(folders,many=True)

    sharedFilesToMe=SharedFile.objects.filter(sharedWith=user)
    sharedFilesToMe_serializer=SharedFileSerializer(sharedFilesToMe, many=True)

    sharedFilesByMe=SharedFile.objects.filter(file__user=user)
    sharedFilesByMe_serializer=SharedFileSerializer(sharedFilesByMe, many=True)


    return Response({
        'files':file_serializer.data,
        'folders':folder_serializer.data,
        'sharedToMe':sharedFilesToMe_serializer.data,
        'sharedByMe':sharedFilesByMe_serializer.data
    })