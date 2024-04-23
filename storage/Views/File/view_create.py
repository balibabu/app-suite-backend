from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .uploadFile import upload, upload_to_git, get_file_instance
from git.extra.fileInProgressManager import incomplete_cleanup
from rest_framework.response import Response

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadFile(request):
    return upload(request)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadToGit(request,id):
    return upload_to_git(chunkId=id)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAndCreateFile(request,id):
    user=request.user
    return get_file_instance(user,fipId=id)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cleanUp(request):
    incomplete_cleanup()
    return Response(status=200)