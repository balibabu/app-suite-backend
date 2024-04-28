from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from storage.serializers import FolderSerializer,  FileSerializer, SharedFileSerializer
from storage.models import Folder, File, SharedFile
from django.contrib.auth.models import User
from collections import defaultdict

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


    all_access = defaultdict(list)
    for i in range(len(file_serializer.data)):
        for row2 in sharedFilesByMe_serializer.data:
            if file_serializer.data[i]['id']==row2['file']:
                item={ 'id':row2['id'] }
                if row2['sharedWith'] : item['sharedWith']=User.objects.get(id=row2['sharedWith']).username
                if row2['anyoneKey'] : item['anyoneKey']=row2['anyoneKey']
                all_access[i].append(item)

    for i in all_access:
        file_serializer.data[i]['access']=all_access[i]


    sharedToMe=[]
    for row in sharedFilesToMe_serializer.data:
        item={}
        file=File.objects.get(id=row['file'])
        item['sharedId']=row['id']
        item['sharedBy']=file.user.username
        item['size']=file.size
        item['title']=file.title
        sharedToMe.append(item)



    return Response({
        'files':file_serializer.data,
        'folders':folder_serializer.data,
        'sharedToMe':sharedToMe,
    })