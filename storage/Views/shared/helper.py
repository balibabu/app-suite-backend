from django.contrib.auth.models import User
from storage.models import  File
from storage.Views.shared.hasher import getHash    
import random

def shareFileHelper(request):
    user = request.user
    fileId=request.data.get('file',None)
    file=File.objects.get(id=fileId, user=user)

    sharedWithUserID=request.data.get('sharedWith',None)
    sharedWith=None
    if sharedWithUserID:
        sharedWith=User.objects.get(id=sharedWithUserID)

    shareWithAnyone=request.data.get('anyone',False)
    anyoneKey=None
    if shareWithAnyone:
        anyoneKey=getHash(user.username+str(random.random)+str(fileId))
    return file,sharedWith,anyoneKey