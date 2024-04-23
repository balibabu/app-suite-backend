from git.models import FileId, Chunk, FileInProgress
from git.extra.repoSizeManager import RepoSizeManager
from git.extra.githubManager import GithubManager
from git.extra.chunkManager import ChunkManager
from git.extra.config import Configurations
from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import time


def create_fip(size,user):
    fileId=FileId.objects.create()
    fip=FileInProgress.objects.create(
        user=user,
        fileId=fileId,
        chunkCount=-(-size//Configurations.MAX_GIT_FILE_SIZE), # math.ceil(size/mcs)
    )
    return fip

def store_chunk(content,fipId):
    fip=FileInProgress.objects.get(id=fipId)
    repo=RepoSizeManager.get_free_repo()
    chunkObject=Chunk.objects.create(fileId=fip.fileId,repo=repo,uname=str(int(time.time())),size=len(content))
    cache.set(f'chunkId_{chunkObject.id}', content)
    RepoSizeManager.add_size(repo,size=len(content))
    return chunkObject.id

def upload_chunk(chunkId):
    chunkObj=Chunk.objects.get(id=chunkId)
    fileContent = cache.get(f'chunkId_{chunkId}')
    user=FileInProgress.objects.get(fileId=chunkObj.fileId).user
    git=GithubManager(user.username)
    git.upload_file(fileContent,chunkObj.uname,chunkObj.repo)
    cache.delete(f'chunkId_{chunkId}')

def complete_cleanup(fipId):
    fip=FileInProgress.objects.get(id=fipId)
    fileId=fip.fileId
    chunks=Chunk.objects.filter(fileId=fileId)
    if len(chunks)==fip.chunkCount:
        fip.delete()
        return fileId
    raise Exception()  # make it missing file exception

def incomplete_cleanup():
    expiredTime = timezone.now() - timedelta(minutes=45)
    fips = FileInProgress.objects.filter(timestamp__lte=expiredTime)
    for fip in fips:
        delete(fip)

def delete(fip):
    fileId=fip.fileId
    chunks=Chunk.objects.filter(fileId=fileId)
    chm=ChunkManager(fip.user.username)
    for chunk in chunks:
        try:
            chm.delete(chunk.id)
            if cache.has_key(f'chunkId_{chunk.id}'): cache.delete(f'chunkId_{chunk.id}')
        except:
            pass
    fileId.delete()

